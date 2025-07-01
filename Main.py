import flet as ft
import MetaTrader5 as mt5
import threading
import time

# MT5 connection settings
MT5_LOGIN = 7902118      # ใส่ MT5 login ของคุณ
MT5_PASSWORD = "Biggu1303@" # ใส่รหัสผ่าน MT5 ของคุณ
MT5_SERVER = "Eightcap-Demo" # ใส่ชื่อ server MT5 ของคุณ

SYMBOLS = ["XAUUSD", "BTCUSD"]

def connect_mt5():
    if not mt5.initialize(login=MT5_LOGIN, password=MT5_PASSWORD, server=MT5_SERVER):
        raise Exception("MT5 connection failed: " + mt5.last_error()[1])

def get_symbol_info(symbol):
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 20)
    if rates is None or len(rates) < 2:
        return {"trend": "N/A", "entry": "N/A"}
    last = rates[-1]['close']
    prev = rates[-2]['close']
    trend = "Up" if last > prev else "Down" if last < prev else "Sideways"
    entry = "Buy" if trend == "Up" else "Sell" if trend == "Down" else "Wait"
    return {"trend": trend, "entry": entry, "price": last}

def send_order(symbol, action):
    price = mt5.symbol_info_tick(symbol).ask if action == "buy" else mt5.symbol_info_tick(symbol).bid
    order_type = mt5.ORDER_TYPE_BUY if action == "buy" else mt5.ORDER_TYPE_SELL
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": 0.01,
        "type": order_type,
        "price": price,
        "deviation": 10,
        "magic": 234000,
        "comment": "Flet Order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    result = mt5.order_send(request)
    return result

def close_all_orders():
    positions = mt5.positions_get()
    for pos in positions:
        symbol = pos.symbol
        volume = pos.volume
        order_type = mt5.ORDER_TYPE_SELL if pos.type == mt5.POSITION_TYPE_BUY else mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(symbol).bid if order_type == mt5.ORDER_TYPE_SELL else mt5.symbol_info_tick(symbol).ask
        close_request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": order_type,
            "position": pos.ticket,
            "price": price,
            "deviation": 10,
            "magic": 234000,
            "comment": "Flet Close All",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        mt5.order_send(close_request)

class Dashboard(ft.Control):
    def build(self):
        self.rows = []
        for sym in SYMBOLS:
            self.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(sym)),
                        ft.DataCell(ft.Text("...")),
                        ft.DataCell(ft.Text("...")),
                        ft.DataCell(ft.Text("...")),
                        ft.DataCell(
                            ft.Row([
                                ft.ElevatedButton("Buy", on_click=lambda s=sym: self.buy(s)),
                                ft.ElevatedButton("Sell", on_click=lambda s=sym: self.sell(s)),
                            ])
                        ),
                    ]
                )
            )
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Symbol")),
                ft.DataColumn(ft.Text("Trend")),
                ft.DataColumn(ft.Text("Entry Signal")),
                ft.DataColumn(ft.Text("Price")),
                ft.DataColumn(ft.Text("Actions")),
            ],
            rows=self.rows,
        )
        self.close_all_btn = ft.ElevatedButton("Close All Orders", on_click=self.close_all)
        return ft.Column([self.table, self.close_all_btn])

    def update_data(self, data):
        for i, sym in enumerate(SYMBOLS):
            self.rows[i].cells[1].content.value = data[sym]["trend"]
            self.rows[i].cells[2].content.value = data[sym]["entry"]
            self.rows[i].cells[3].content.value = str(data[sym]["price"])
        self.table.update()

    def buy(self, symbol):
        send_order(symbol, "buy")

    def sell(self, symbol):
        send_order(symbol, "sell")

    def close_all(self, e):
        close_all_orders()

def main(page: ft.Page):
    page.title = "MT5 Dashboard"
    dashboard = Dashboard()
    page.add(dashboard)

    def refresh():
        while True:
            data = {}
            for sym in SYMBOLS:
                data[sym] = get_symbol_info(sym)
            page.run_on_main(lambda: dashboard.update_data(data))
            time.sleep(2)

    connect_mt5()
    threading.Thread(target=refresh, daemon=True).start()

ft.app(target=main)