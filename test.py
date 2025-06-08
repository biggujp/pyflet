import flet as ft
import MetaTrader5 as mt5
import threading
import time
import pandas as pd
import numpy as np

# --- CONFIG ---
SYMBOL = "BTCUSD"
TIMEFRAME = mt5.TIMEFRAME_M15
EMA_FAST = 20
EMA_SLOW = 50
RSI_PERIOD = 14

# --- GLOBALS ---
running = False
prev_open = None

def get_account_info():
    acc = mt5.account_info()
    if acc:
        return {
            "server": acc.server,
            "login": acc.login,
            "balance": acc.balance,
            "equity": acc.equity,
            "margin_free": acc.margin_free,
            "profit": acc.profit
        }
    return {}

def get_rates(symbol, timeframe, count=100):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
    if rates is not None and len(rates) > 0:
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        return df
    return pd.DataFrame()

def calc_indicators(df):
    df['ema_fast'] = df['close'].ewm(span=EMA_FAST, adjust=False).mean()
    df['ema_slow'] = df['close'].ewm(span=EMA_SLOW, adjust=False).mean()
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(RSI_PERIOD).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(RSI_PERIOD).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    return df

def trading_logic(df, acc_info):
    last = df.iloc[-1]
    prev = df.iloc[-2]
    # Conditions
    cond1 = last['close'] > last['ema_fast']
    cond2 = prev['close'] < prev['ema_slow'] and last['close'] > last['ema_slow']
    cond3 = last['rsi'] > 50
    if cond1 and cond2 and cond3:
        price = last['close']
        sl = last['ema_slow'] - 10  # adjust as needed
        tp = prev['high']
        lot = 0.01  # adjust as needed
        request = {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": SYMBOL,
            "volume": lot,
            "type": mt5.ORDER_TYPE_BUY_LIMIT,
            "price": price,
            "sl": sl,
            "tp": tp,
            "deviation": 20,
            "magic": 123456,
            "comment": "FletBot",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request)
        return result
    return None

def main(page: ft.Page):
    global running, prev_open

    # --- UI Elements ---
    server_text = ft.Text("Server: -")
    account_text = ft.Text("Account: -")
    balance_text = ft.Text("Balance: -")
    equity_text = ft.Text("Equity: -")
    margin_free_text = ft.Text("Margin Free: -")
    profit_text = ft.Text("Profit: -")

    ohlc_text = ft.Text("Open: -  High: -  Low: -")
    close_bid_ask_text = ft.Text("Close: -  Bid: -  Ask: -")

    bal_eq_margin_profit = ft.Text("Balance: -  Equity: -  Margin Free: -  Profit: -")

    rsi_status = ft.Text("RSI: -", color=ft.colors.BLACK)
    ema_status = ft.Text("EMA: -", color=ft.colors.BLACK)

    start_btn = ft.ElevatedButton("Start", on_click=lambda e: start())
    stop_btn = ft.ElevatedButton("Stop", on_click=lambda e: stop())

    # --- Layout ---
    page.add(
        ft.Row([server_text, account_text]),
        ft.Row([balance_text, equity_text, margin_free_text, profit_text]),
        ft.Divider(),
        ohlc_text,
        close_bid_ask_text,
        bal_eq_margin_profit,
        rsi_status,
        ema_status,
        ft.Row([start_btn, stop_btn])
    )

    # --- MT5 Connect ---
    if not mt5.initialize():
        page.snack_bar = ft.SnackBar(ft.Text("MT5 connection failed!"))
        page.snack_bar.open = True
        page.update()
        return

    def update_ui():
        acc = get_account_info()
        if acc:
            server_text.value = f"Server: {acc['server']}"
            account_text.value = f"Account: {acc['login']}"
            balance_text.value = f"Balance: {acc['balance']:.2f}"
            equity_text.value = f"Equity: {acc['equity']:.2f}"
            margin_free_text.value = f"Margin Free: {acc['margin_free']:.2f}"
            profit_text.value = f"Profit: {acc['profit']:.2f}"
            bal_eq_margin_profit.value = f"Balance: {acc['balance']:.2f}  Equity: {acc['equity']:.2f}  Margin Free: {acc['margin_free']:.2f}  Profit: {acc['profit']:.2f}"
        df = get_rates(SYMBOL, TIMEFRAME, 100)
        if not df.empty:
            df = calc_indicators(df)
            last = df.iloc[-1]
            prev = df.iloc[-2]
            global prev_open
            # OHLC
            ohlc_text.value = f"Open: {last['open']:.2f}  High: {last['high']:.2f}  Low: {last['low']:.2f}"
            # Close/Bid/Ask
            tick = mt5.symbol_info_tick(SYMBOL)
            close_bid_ask_text.value = f"Close: {last['close']:.2f}  Bid: {tick.bid if tick else '-'}  Ask: {tick.ask if tick else '-'}"
            # RSI
            if last['rsi'] > 50:
                rsi_status.value = "Trend Up"
                rsi_status.color = ft.colors.GREEN
            else:
                rsi_status.value = "Trend Down"
                rsi_status.color = ft.colors.RED
            # EMA
            if prev['ema_fast'] < prev['ema_slow'] and last['ema_fast'] > last['ema_slow']:
                ema_status.value = "Crossup"
                ema_status.color = ft.colors.GREEN
            elif prev['ema_fast'] > prev['ema_slow'] and last['ema_fast'] < last['ema_slow']:
                ema_status.value = "Crossunder"
                ema_status.color = ft.colors.RED
            else:
                ema_status.value = "Waiting"
                ema_status.color = ft.colors.YELLOW
            # Update only if open price changed
            if prev_open is None or prev_open != last['open']:
                prev_open = last['open']
                page.update()
            else:
                # Still update other fields
                page.update()

    def loop():
        while running:
            update_ui()
            # Trading logic
            df = get_rates(SYMBOL, TIMEFRAME, 100)
            if not df.empty:
                df = calc_indicators(df)
                acc = get_account_info()
                trading_logic(df, acc)
            time.sleep(2)

    def start():
        global running
        if not running:
            running = True
            threading.Thread(target=loop, daemon=True).start()

    def stop():
        global running
        running = False

    update_ui()

ft.app(target=main)