import flet as ft
import MetaTrader5 as mt5
import threading
import time
import pandas as pd
import numpy as np

# --- MT5 Connection ---
MT5_SYMBOL = "BTCUSD"
MT5_TIMEFRAME = mt5.TIMEFRAME_M15

def connect_mt5():
    if not mt5.initialize():
        raise Exception("MT5 initialize() failed")
    account_info = mt5.account_info()
    if account_info is None:
        raise Exception("MT5 account_info() failed")
    return account_info

def get_account_info():
    info = mt5.account_info()
    if info:
        return info.server, info.login, info.balance, info.equity, info.margin_free
    return "-", "-", "-", "-", "-"

def get_ohlc():
    rates = mt5.copy_rates_from_pos(MT5_SYMBOL, MT5_TIMEFRAME, 0, 2)
    if rates is not None and len(rates) >= 2:
        last = rates[-1]
        return last['close'], last['open'], last['high'], last['low']
    return "-", "-", "-", "-"

def get_bid_ask():
    tick = mt5.symbol_info_tick(MT5_SYMBOL)
    if tick:
        return tick.bid, tick.ask
    return "-", "-"

def get_rsi():
    rates = mt5.copy_rates_from_pos(MT5_SYMBOL, MT5_TIMEFRAME, 0, 100)
    if rates is not None and len(rates) >= 15:
        close = pd.Series([x['close'] for x in rates])
        delta = close.diff()
        up = delta.clip(lower=0)
        down = -1 * delta.clip(upper=0)
        avg_gain = up.rolling(window=14, min_periods=14).mean()
        avg_loss = down.rolling(window=14, min_periods=14).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1]
    return None

def get_ema_cross():
    rates = mt5.copy_rates_from_pos(MT5_SYMBOL, MT5_TIMEFRAME, 0, 60)
    if rates is not None and len(rates) >= 50:
        close = pd.Series([x['close'] for x in rates])
        ema20 = close.ewm(span=20, adjust=False).mean()
        ema50 = close.ewm(span=50, adjust=False).mean()
        if ema20.iloc[-2] < ema50.iloc[-2] and ema20.iloc[-1] > ema50.iloc[-1]:
            return "CROSSUP"
        elif ema20.iloc[-2] > ema50.iloc[-2] and ema20.iloc[-1] < ema50.iloc[-1]:
            return "CROSSDOWN"
        else:
            return "WAIT"
    return "WAIT"

def send_order(action):
    symbol_info = mt5.symbol_info(MT5_SYMBOL)
    if symbol_info is None or not symbol_info.visible:
        mt5.symbol_select(MT5_SYMBOL, True)
    price = mt5.symbol_info_tick(MT5_SYMBOL).ask if action == "buy" else mt5.symbol_info_tick(MT5_SYMBOL).bid
    order_type = mt5.ORDER_TYPE_BUY if action == "buy" else mt5.ORDER_TYPE_SELL
    lot = 0.01
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": MT5_SYMBOL,
        "volume": lot,
        "type": order_type,
        "price": price,
        "deviation": 10,
        "magic": 234000,
        "comment": "Flet order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    result = mt5.order_send(request)
    return result

# --- Flet UI ---
def main(page: ft.Page):
    page.title = "Bitcoin Trader"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.START

    # UI Elements
    broker_text = ft.Text("Server: - | Account: - | Balance: - | Equity: - | Margin_free: -")
    ohlc_text = ft.Text("Close: - | Open: - | High: - | Low: -")
    bidask_text = ft.Text("Bid: - | Ask: -")
    rsi_text = ft.Text("RSI: -")
    ema_text = ft.Text("EMA: -")
    status_text = ft.Text("Status: -")
    buy_btn = ft.ElevatedButton("BUY", bgcolor=ft.colors.GREEN, on_click=lambda e: order_action("buy"))
    sell_btn = ft.ElevatedButton("SELL", bgcolor=ft.colors.RED, on_click=lambda e: order_action("sell"))

    def update_ui():
        try:
            name, login, balance, equity, marginfree = get_account_info()
            broker_text.value = f"Server: {name} | Account: {login} | Balance: {balance:.2f} | Equity: {equity:.2f} | Margin_free: {marginfree:.2f}"
            page.title = f"Bitcoin Trader: {broker_text.value}"
            close, open_, high, low = get_ohlc()
            ohlc_text.value = f"Close: {close} | Open: {open_} | High: {high} | Low: {low}"
            bid, ask = get_bid_ask()
            bidask_text.value = f"Bid: {bid} | Ask: {ask}"
            rsi = get_rsi()
            if rsi is not None:
                if rsi > 50:
                    rsi_text.value = "RSI: Uptrend"
                    rsi_text.color = ft.colors.GREEN
                else:
                    rsi_text.value = "RSI: Downtrend"
                    rsi_text.color = ft.colors.RED
            else:
                rsi_text.value = "RSI: -"
                rsi_text.color = ft.colors.WHITE
            cross = get_ema_cross()
            if cross == "CROSSUP":
                ema_text.value = "EMA: Crossover"
                ema_text.color = ft.colors.GREEN
            elif cross == "CROSSDOWN":
                ema_text.value = "EMA: Crossunder"
                ema_text.color = ft.colors.RED
            else:
                ema_text.value = "EMA: Waiting"
                ema_text.color = ft.colors.YELLOW
            page.update()
        except Exception as ex:
            status_text.value = f"Error: {ex}"
            page.update()

    def order_action(action):
        result = send_order(action)
        if result and result.retcode == mt5.TRADE_RETCODE_DONE:
            status_text.value = f"{action.upper()} order sent!"
        else:
            status_text.value = f"Order failed: {getattr(result, 'comment', 'Unknown error')}"
        page.update()

    # Layout
    page.add(
        ohlc_text,
        bidask_text,
        ft.Row([rsi_text, ema_text], alignment=ft.MainAxisAlignment.START),
        ft.Row([buy_btn, sell_btn], alignment=ft.MainAxisAlignment.START),
        status_text
    )

    # Background update thread
    def bg_update():
        while True:
            update_ui()
            time.sleep(3)

    threading.Thread(target=bg_update, daemon=True).start()

if __name__ == "__main__":
    connect_mt5()
    ft.app(target=main)