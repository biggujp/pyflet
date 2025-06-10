import flet as ft
import MetaTrader5 as mt5
import threading
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


# --- MT5 Connection Config ---
MT5_SERVER = "Eightcap-Demo"
MT5_LOGIN = 7902118
MT5_PASSWORD = "Biggu1303@"
SYMBOL = "BTCUSD"
LOT = 0.01

def connect_mt5():
    if not mt5.initialize(server=MT5_SERVER, login=MT5_LOGIN, password=MT5_PASSWORD):
        return False
    return True

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

def get_rates(timeframe, count=100):
    tf = {
        "M5": mt5.TIMEFRAME_M5,
        "M15": mt5.TIMEFRAME_M15
    }[timeframe]
    rates = mt5.copy_rates_from_pos(SYMBOL, tf, 0, count)
    return pd.DataFrame(rates) if rates is not None else pd.DataFrame()

def calc_rsi(df, period=14):
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calc_ema(df, period):
    return df['close'].ewm(span=period, adjust=False).mean()

def send_order(action, price, sl, tp):
    order_type = mt5.ORDER_TYPE_BUY if action == "buy" else mt5.ORDER_TYPE_SELL
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": SYMBOL,
        "volume": LOT,
        "type": order_type,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": 20,
        "magic": 234000,
        "comment": "FletBot",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    return mt5.order_send(request)

def close_all_orders():
    positions = mt5.positions_get(symbol=SYMBOL)
    for pos in positions:
        order_type = mt5.ORDER_TYPE_SELL if pos.type == 0 else mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(SYMBOL).bid if pos.type == 0 else mt5.symbol_info_tick(SYMBOL).ask
        close_request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": SYMBOL,
            "volume": pos.volume,
            "type": order_type,
            "position": pos.ticket,
            "price": price,
            "deviation": 20,
            "magic": 234000,
            "comment": "FletBot Close",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        mt5.order_send(close_request)

class MT5FletApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.auto_mode = False
        self.trade_log = []
        self.lock = threading.Lock()
        self.init_ui()
        self.start_update_thread()

    def init_ui(self):
        self.page.title = "MT5 BTCUSD Dashboard"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.account_info = ft.Text("Account: -")
        self.balance_info = ft.Text("Balance: - Equity: - Margin Free: - Profit: -")
        self.price_info = ft.Text("Open: - High: - Low: - Close: - Bid: - Ask: -")
        self.rsi_info = ft.Text("RSI: -", color=ft.colors.YELLOW)
        self.ema_info = ft.Text("EMA: -", color=ft.colors.YELLOW)
        self.auto_mode_btn = ft.ElevatedButton("Auto Mode OFF", on_click=self.toggle_auto_mode, bgcolor=ft.colors.GREY_800)
        self.buy_btn = ft.ElevatedButton("Buy", on_click=self.buy_action, bgcolor=ft.colors.GREEN)
        self.sell_btn = ft.ElevatedButton("Sell", on_click=self.sell_action, bgcolor=ft.colors.RED)
        self.close_btn = ft.ElevatedButton("Close All", on_click=self.close_all_action, bgcolor=ft.colors.BLUE)
        self.trade_list = ft.ListView(expand=True, spacing=5, height=200)
        self.page.add(
            self.account_info,
            self.balance_info,
            self.price_info,
            self.rsi_info,
            self.ema_info,
            ft.Row([self.buy_btn, self.sell_btn, self.close_btn, self.auto_mode_btn]),
            ft.Text("Trade Log:"),
            self.trade_list
        )

    def update_ui(self):
        if not mt5.initialize():
            self.account_info.value = "MT5 not connected"
            self.page.update()
            return
        acc = get_account_info()
        if acc:
            self.account_info.value = f"Server: {acc['server']} | Account: {acc['login']}"
            self.balance_info.value = f"Balance: {acc['balance']} | Equity: {acc['equity']} | Margin Free: {acc['margin_free']} | Profit: {acc['profit']}"
        rates5 = get_rates("M5", 100)
        rates15 = get_rates("M15", 100)
        if not rates5.empty:
            last = rates5.iloc[-1]
            tick = mt5.symbol_info_tick(SYMBOL)
            self.price_info.value = f"Open: {last['open']} High: {last['high']} Low: {last['low']} Close: {last['close']} Bid: {tick.bid} Ask: {tick.ask}"
            # EMA
            ema20 = calc_ema(rates5, 20)
            ema50 = calc_ema(rates5, 50)
            if ema20.iloc[-1] > ema50.iloc[-1] and ema20.iloc[-2] <= ema50.iloc[-2]:
                self.ema_info.value = "Crossover"
                self.ema_info.color = ft.colors.GREEN
            elif ema20.iloc[-1] < ema50.iloc[-1] and ema20.iloc[-2] >= ema50.iloc[-2]:
                self.ema_info.value = "Crossunder"
                self.ema_info.color = ft.colors.RED
            else:
                self.ema_info.value = "Signal Waiting"
                self.ema_info.color = ft.colors.YELLOW
        if not rates15.empty:
            rsi = calc_rsi(rates15, 14)
            rsi_val = rsi.iloc[-1]
            if rsi_val > 50:
                self.rsi_info.value = f"RSI: {rsi_val:.2f} Trend Up"
                self.rsi_info.color = ft.colors.GREEN
            else:
                self.rsi_info.value = f"RSI: {rsi_val:.2f} Trend Down"
                self.rsi_info.color = ft.colors.RED
        self.trade_list.controls.clear()
        with self.lock:
            for log in self.trade_log[-20:]:
                self.trade_list.controls.append(ft.Text(log))
        self.page.update()

    def buy_action(self, e):
        tick = mt5.symbol_info_tick(SYMBOL)
        price = tick.ask
        sl = price - 100  # Example SL
        tp = price + 100  # Example TP
        result = send_order("buy", price, sl, tp)
        with self.lock:
            self.trade_log.append(f"{datetime.now()} BUY @ {price} SL:{sl} TP:{tp} Result:{result.retcode}")
        self.update_ui()

    def sell_action(self, e):
        tick = mt5.symbol_info_tick(SYMBOL)
        price = tick.bid
        sl = price + 100  # Example SL
        tp = price - 100  # Example TP
        result = send_order("sell", price, sl, tp)
        with self.lock:
            self.trade_log.append(f"{datetime.now()} SELL @ {price} SL:{sl} TP:{tp} Result:{result.retcode}")
        self.update_ui()

    def close_all_action(self, e):
        close_all_orders()
        with self.lock:
            self.trade_log.append(f"{datetime.now()} CLOSE ALL")
        self.update_ui()

    def toggle_auto_mode(self, e):
        self.auto_mode = not self.auto_mode
        self.auto_mode_btn.text = "Auto Mode ON" if self.auto_mode else "Auto Mode OFF"
        self.auto_mode_btn.bgcolor = ft.colors.GREEN if self.auto_mode else ft.colors.GREY_800
        self.page.update()
        if self.auto_mode:
            threading.Thread(target=self.auto_mode_loop, daemon=True).start()

    def auto_mode_loop(self):
        while self.auto_mode:
            # Check for open positions before sending new orders
            positions = mt5.positions_get(symbol=SYMBOL)
            if positions and len(positions) > 0:
                with self.lock:
                    self.trade_log.append(f"{datetime.now()} มีออเดอร์ค้างอยู่ ไม่สามารถส่งคำสั่งใหม่ได้")
                self.update_ui()
                time.sleep(10)
                continue
            rates5 = get_rates("M5", 100)
            rates15 = get_rates("M15", 100)
            if not rates5.empty and not rates15.empty:
                ema20 = calc_ema(rates5, 20)
                ema50 = calc_ema(rates5, 50)
                close = rates5['close'].iloc[-1]
                high = rates5['high'].iloc[-2]
                low = rates5['low'].iloc[-2]
                rsi = calc_rsi(rates15, 14).iloc[-1]
                tick = mt5.symbol_info_tick(SYMBOL)
                if ema20.iloc[-1] > ema50.iloc[-1] and ema20.iloc[-2] <= ema50.iloc[-2] and rsi > 50:
                    price = close
                    sl = ema20.iloc[-1] - 50
                    tp = high
                    result = send_order("buy", price, sl, tp)
                    with self.lock:
                        self.trade_log.append(f"{datetime.now()} AUTO BUY @ {price} SL:{sl} TP:{tp} Result:{result.retcode}")
                elif ema20.iloc[-1] < ema50.iloc[-1] and ema20.iloc[-2] >= ema50.iloc[-2] and rsi < 50:
                    price = close
                    sl = ema50.iloc[-1] + 50
                    tp = low
                    result = send_order("sell", price, sl, tp)
                    with self.lock:
                        self.trade_log.append(f"{datetime.now()} AUTO SELL @ {price} SL:{sl} TP:{tp} Result:{result.retcode}")
            self.update_ui()
            time.sleep(10)

    def start_update_thread(self):
        def update_loop():
            while True:
                self.update_ui()
                time.sleep(2)
        threading.Thread(target=update_loop, daemon=True).start()

def main(page: ft.Page):
    if not connect_mt5():
        page.add(ft.Text("MT5 Connection Failed", color=ft.colors.RED))
        return
    MT5FletApp(page)

ft.app(target=main)