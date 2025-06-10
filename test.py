import flet as ft
import MetaTrader5 as mt5
import threading
import time
import pandas as pd

# --- MT5 Connection Config ---
MT5_SERVER = "Eightcap-Demo"
MT5_LOGIN = 7902118
MT5_PASSWORD = "Biggu1303@"
MT5_SYMBOL = "BTCUSD"

# --- Helper Functions ---
def connect_mt5():
    if not mt5.initialize(server=MT5_SERVER, login=MT5_LOGIN, password=MT5_PASSWORD):
        return False
    return True

def get_account_info():
    acc = mt5.account_info()
    if acc:
        return acc.server, acc.login, acc.balance, acc.equity, acc.margin_free
    return "-", "-", "-", "-", "-"

def get_ohlc(symbol, timeframe, count=2):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
    if rates is not None and len(rates) > 0:
        return rates[-1]
    return None

def get_tick(symbol):
    tick = mt5.symbol_info_tick(symbol)
    return tick

def get_rsi(symbol, timeframe, period=14):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, period+1)
    if rates is not None and len(rates) > period:
        close = pd.Series([x['close'] for x in rates])
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1]
    return None

def get_ema(symbol, timeframe, period, count=60):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
    if rates is not None and len(rates) >= period:
        close = pd.Series([x['close'] for x in rates])
        ema = close.ewm(span=period, adjust=False).mean()
        return ema.iloc[-1], ema.iloc[-2]
    return None, None

def send_order(symbol, action, lot=0.01):
    price = mt5.symbol_info_tick(symbol)
    if not price:
        return False
    if action == "buy":
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_BUY,
            "price": price.ask,
            "deviation": 20,
            "magic": 234000,
            "comment": "Flet Buy",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
    else:
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_SELL,
            "price": price.bid,
            "deviation": 20,
            "magic": 234000,
            "comment": "Flet Sell",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
    result = mt5.order_send(request)
    return result.retcode == mt5.TRADE_RETCODE_DONE

# --- Flet App ---
def main(page: ft.Page):
    page.title = "MT5 BTCUSD Monitor"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.START

    # UI Controls
    server_text = ft.Text("Server: -")
    account_text = ft.Text("Account ID: -")
    balance_text = ft.Text("Balance: -")
    equity_text = ft.Text("Equity: -")
    margin_free_text = ft.Text("Margin Free: -")

    ohlc_text = ft.Text("Open: -  High: -  Low: -")
    close_bid_ask_text = ft.Text("Close: -  Bid: -  Ask: -")

    rsi_text = ft.Text("RSI: -", size=20)
    rsi_status = ft.Text("Trend: -", size=20)

    ema_text = ft.Text("EMA20: -  EMA50: -")
    ema_status = ft.Text("Signal: -", size=20)

    buy_btn = ft.ElevatedButton("Buy", bgcolor=ft.colors.GREEN, on_click=lambda e: send_order_btn("buy"))
    sell_btn = ft.ElevatedButton("Sell", bgcolor=ft.colors.RED, on_click=lambda e: send_order_btn("sell"))

    # Layout
    page.add(
        ft.Column([
            server_text, account_text, balance_text, equity_text, margin_free_text,
            ft.Divider(),
            ohlc_text,
            close_bid_ask_text,
            ft.Divider(),
            rsi_text,
            rsi_status,
            ft.Divider(),
            ema_text,
            ema_status,
            ft.Row([buy_btn, sell_btn])
        ])
    )

    # Button Handlers
    def send_order_btn(action):
        success = send_order(MT5_SYMBOL, action)
        if success:
            page.snack_bar = ft.SnackBar(ft.Text(f"{action.capitalize()} order sent!"), bgcolor=ft.colors.GREEN)
        else:
            page.snack_bar = ft.SnackBar(ft.Text(f"{action.capitalize()} order failed!"), bgcolor=ft.colors.RED)
        page.snack_bar.open = True
        page.update()

    # Data Update Thread
    def update_data():
        while True:
            # Account Info
            server, acc_id, balance, equity, margin_free = get_account_info()
            server_text.value = f"Server: {server}"
            account_text.value = f"Account ID: {acc_id}"
            balance_text.value = f"Balance: {balance}"
            equity_text.value = f"Equity: {equity}"
            margin_free_text.value = f"Margin Free: {margin_free}"

            # OHLC 5m
            ohlc = get_ohlc(MT5_SYMBOL, mt5.TIMEFRAME_M5)
            if ohlc:
                ohlc_text.value = f"Open: {ohlc['open']}  High: {ohlc['high']}  Low: {ohlc['low']}"
                close_bid_ask_text.value = f"Close: {ohlc['close']}  Bid: {get_tick(MT5_SYMBOL).bid}  Ask: {get_tick(MT5_SYMBOL).ask}"

            # RSI 15m
            rsi = get_rsi(MT5_SYMBOL, mt5.TIMEFRAME_M15)
            if rsi is not None:
                rsi_text.value = f"RSI: {rsi:.2f}"
                if rsi > 50:
                    rsi_status.value = "Trend Up"
                    rsi_status.color = ft.colors.GREEN
                else:
                    rsi_status.value = "Trend Down"
                    rsi_status.color = ft.colors.RED

            # EMA 5m
            ema20_now, ema20_prev = get_ema(MT5_SYMBOL, mt5.TIMEFRAME_M5, 20)
            ema50_now, ema50_prev = get_ema(MT5_SYMBOL, mt5.TIMEFRAME_M5, 50)
            if ema20_now and ema50_now and ema20_prev and ema50_prev:
                ema_text.value = f"EMA20: {ema20_now:.2f}  EMA50: {ema50_now:.2f}"
                # Crossover logic
                if ema20_prev < ema50_prev and ema20_now > ema50_now:
                    ema_status.value = "Crossover"
                    ema_status.color = ft.colors.GREEN
                elif ema20_prev > ema50_prev and ema20_now < ema50_now:
                    ema_status.value = "Crossunder"
                    ema_status.color = ft.colors.RED
                else:
                    ema_status.value = "Signal Waiting"
                    ema_status.color = ft.colors.YELLOW

            page.update()
            time.sleep(2)

    # Start
    if connect_mt5():
        threading.Thread(target=update_data, daemon=True).start()
    else:
        page.add(ft.Text("MT5 Connection Failed!", color=ft.colors.RED))

ft.app(target=main)