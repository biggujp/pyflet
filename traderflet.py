import flet as ft
import MetaTrader5 as mt5
import threading
import time
from datetime import datetime, timedelta

MT5_SYMBOL = "BTCUSD"
TIMEFRAME = mt5.TIMEFRAME_M15

def connect_mt5():
    if not mt5.initialize():
        raise Exception("MT5 initialize() failed")
    if not mt5.symbol_select(MT5_SYMBOL, True):
        raise Exception(f"Failed to select symbol {MT5_SYMBOL}")

def get_latest_candle():
    utc_from = datetime.now() - timedelta(days=1)
    rates = mt5.copy_rates_from(MT5_SYMBOL, TIMEFRAME, utc_from, 1)
    if rates is not None and len(rates) > 0:
        rate = rates[-1]
        return {
            "open": rate['open'],
            "high": rate['high'],
            "low": rate['low'],
            "close": rate['close'],
            "time": datetime.fromtimestamp(rate['time']),
        }
    return None

def get_current_price():
    tick = mt5.symbol_info_tick(MT5_SYMBOL)
    if tick:
        return tick.ask
    return None

def send_order(action):
    price = get_current_price()
    if price is None:
        return False, "No price"
    order_type = mt5.ORDER_TYPE_BUY if action == "buy" else mt5.ORDER_TYPE_SELL
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": MT5_SYMBOL,
        "volume": 0.01,
        "type": order_type,
        "price": price,
        "deviation": 10,
        "magic": 234000,
        "comment": f"Flet {action}",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    result = mt5.order_send(request)
    if result.retcode == mt5.TRADE_RETCODE_DONE:
        return True, "Order sent"
    else:
        return False, f"Order failed: {result.comment}"

class PriceUpdater(threading.Thread):
    def __init__(self, update_callback):
        super().__init__(daemon=True)
        self.update_callback = update_callback
        self.running = True

    def run(self):
        while self.running:
            self.update_callback()
            time.sleep(900)  # 15 minutes

    def stop(self):
        self.running = False


class CurrentPriceUpdater(threading.Thread):
    def __init__(self, update_callback):
        super().__init__(daemon=True)
        self.update_callback = update_callback
        self.running = True

    def run(self):
        while self.running:
            self.update_callback()
            time.sleep(1)  # Update every second

    def stop(self):
        self.running = False

# Modify main to use the new CurrentPriceUpdater
def main(page: ft.Page):
    page.title = "BTCUSD MT5 Trader"
    connect_mt5()

    open_text = ft.Text("Open: -")
    high_text = ft.Text("High: -")
    low_text = ft.Text("Low: -")
    close_text = ft.Text("Close: -")
    current_text = ft.Text("Current: -")
    status_text = ft.Text("Status: Ready")

    def update_candle():
        candle = get_latest_candle()
        if candle:
            open_text.value = f"Open: {candle['open']}"
            high_text.value = f"High: {candle['high']}"
            low_text.value = f"Low: {candle['low']}"
            close_text.value = f"Close: {candle['close']}"
            page.update()

    def update_current():
        current = get_current_price()
        if current:
            current_text.value = f"Current: {current}"
            page.update()

    def on_buy(e):
        ok, msg = send_order("buy")
        status_text.value = msg
        page.update()

    def on_sell(e):
        ok, msg = send_order("sell")
        status_text.value = msg
        page.update()

    update_candle()
    update_current()
    candle_updater = PriceUpdater(update_candle)
    current_updater = CurrentPriceUpdater(update_current)
    candle_updater.start()
    current_updater.start()

    page.add(
        ft.Column([
            open_text,
            high_text,
            low_text,
            close_text,
            current_text,
            ft.Row([
                ft.ElevatedButton("Buy", on_click=on_buy),
                ft.ElevatedButton("Sell", on_click=on_sell),
            ]),
            status_text,
        ])
    )

    def on_close(e):
        candle_updater.stop()
        current_updater.stop()
        mt5.shutdown()

    page.on_close = on_close

ft.app(target=main)