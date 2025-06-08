import flet as ft
import MetaTrader5 as mt5
import threading
import time
import pandas as pd
import numpy as np

# --- MT5 Connection ---
MT5_SERVER = "Eightcap-Demo"
MT5_LOGIN = 7902118
MT5_PASSWORD = "Biggu1303@"
MT5_SYMBOL = "BTCUSD"
MT5_TIMEFRAME = mt5.TIMEFRAME_M15

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

def get_btcusd_data():
    rates = mt5.copy_rates_from_pos(MT5_SYMBOL, MT5_TIMEFRAME, 0, 100)
    df = pd.DataFrame(rates)
    return df

def get_current_price():
    tick = mt5.symbol_info_tick(MT5_SYMBOL)
    return tick

def calculate_rsi(df, period=14):
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_ema(df, period):
    return df['close'].ewm(span=period, adjust=False).mean()

# --- Flet UI ---
class MT5App:
    def __init__(self):
        self.running = False
        self.thread = None
        self.prev_open = None

        self.server_text = ft.Text("Server: -")
        self.account_text = ft.Text("Account ID: -")
        self.balance_text = ft.Text("Balance: -")
        self.equity_text = ft.Text("Equity: -")
        self.margin_free_text = ft.Text("Margin Free: -")
        self.profit_text = ft.Text("Profit: -")

        self.ohlc_text = ft.Text("BTCUSD O/H/L: - / - / -")
        self.close_bid_ask_text = ft.Text("Close/Bid/Ask: - / - / -")
        self.bal_eq_margin_profit_text = ft.Text("Balance/Equity/Margin Free/Profit: - / - / - / -")

        self.rsi_status = ft.Text("RSI: -", color=ft.colors.ON_SURFACE)
        self.ema_status = ft.Text("EMA: -", color=ft.colors.ON_SURFACE)

        self.start_btn = ft.ElevatedButton("Start", on_click=self.start)
        self.stop_btn = ft.ElevatedButton("Stop", on_click=self.stop, disabled=True)

        self.controls = ft.Column([
            ft.Row([self.server_text, self.account_text]),
            ft.Row([self.balance_text, self.equity_text, self.margin_free_text]),
            ft.Row([self.profit_text]),
            ft.Divider(),
            self.ohlc_text,
            self.close_bid_ask_text,
            self.bal_eq_margin_profit_text,
            ft.Row([self.rsi_status, self.ema_status]),
            ft.Row([self.start_btn, self.stop_btn])
        ])

    def update_ui(self, acc_info, df, tick):
        # Account
        self.server_text.value = f"Server: {acc_info.get('server', '-')}"
        self.account_text.value = f"Account ID: {acc_info.get('login', '-')}"
        self.balance_text.value = f"Balance: {acc_info.get('balance', '-'):.2f}"
        self.equity_text.value = f"Equity: {acc_info.get('equity', '-'):.2f}"
        self.margin_free_text.value = f"Margin Free: {acc_info.get('margin_free', '-'):.2f}"
        self.profit_text.value = f"Profit: {acc_info.get('profit', '-'):.2f}"
        self.bal_eq_margin_profit_text.value = (
            f"Balance/Equity/Margin Free/Profit: "
            f"{acc_info.get('balance', '-'):.2f} / "
            f"{acc_info.get('equity', '-'):.2f} / "
            f"{acc_info.get('margin_free', '-'):.2f} / "
            f"{acc_info.get('profit', '-'):.2f}"
        )

        # OHLC
        if not df.empty:
            o = df.iloc[-1]['open']
            h = df.iloc[-1]['high']
            l = df.iloc[-1]['low']
            self.ohlc_text.value = f"BTCUSD O/H/L: {o:.2f} / {h:.2f} / {l:.2f}"

            # Update only if open changed
            if self.prev_open != o:
                self.prev_open = o
                self.ohlc_text.value = f"BTCUSD O/H/L: {o:.2f} / {h:.2f} / {l:.2f}"

            c = df.iloc[-1]['close']
            close = c
        else:
            close = 0

        # Close/Bid/Ask
        if tick:
            self.close_bid_ask_text.value = f"Close/Bid/Ask: {close:.2f} / {tick.bid:.2f} / {tick.ask:.2f}"

        # RSI
        rsi = calculate_rsi(df).iloc[-1] if not df.empty else 0
        if rsi > 50:
            self.rsi_status.value = "Trend Up"
            self.rsi_status.color = ft.colors.GREEN
        else:
            self.rsi_status.value = "Trend Down"
            self.rsi_status.color = ft.colors.RED

        # EMA
        ema20 = calculate_ema(df, 20).iloc[-1] if not df.empty else 0
        ema50 = calculate_ema(df, 50).iloc[-1] if not df.empty else 0
        prev_ema20 = calculate_ema(df, 20).iloc[-2] if len(df) > 1 else 0
        prev_ema50 = calculate_ema(df, 50).iloc[-2] if len(df) > 1 else 0

        if prev_ema20 < prev_ema50 and ema20 > ema50:
            self.ema_status.value = "Crossup"
            self.ema_status.color = ft.colors.GREEN
        elif prev_ema20 > prev_ema50 and ema20 < ema50:
            self.ema_status.value = "Crossunder"
            self.ema_status.color = ft.colors.RED
        else:
            self.ema_status.value = "Waiting"
            self.ema_status.color = ft.colors.YELLOW

        self.update()

    def trading_logic(self):
        while self.running:
            acc_info = get_account_info()
            df = get_btcusd_data()
            tick = get_current_price()

            # --- Trading Logic ---
            if not df.empty:
                close = df.iloc[-1]['close']
                high = df.iloc[-2]['high']
                low = df.iloc[-2]['low']
                ema20 = calculate_ema(df, 20).iloc[-1]
                ema50 = calculate_ema(df, 50).iloc[-1]
                prev_ema20 = calculate_ema(df, 20).iloc[-2]
                prev_ema50 = calculate_ema(df, 50).iloc[-2]
                rsi = calculate_rsi(df).iloc[-1]

                # Buy Condition
                if close > ema20 and prev_ema50 < prev_ema20 and ema50 < ema20 and rsi > 50:
                    price = close
                    sl = ema50 - 20  # adjust as needed
                    tp = high
                    # Place buy limit order
                    # mt5.order_send(...)
                # Sell Condition
                elif close < ema20 and prev_ema50 > prev_ema20 and ema50 > ema20 and rsi < 50:
                    price = close
                    sl = ema50 + 20  # adjust as needed
                    tp = low
                    # Place sell limit order
                    # mt5.order_send(...)

            # --- Update UI ---
            self.page.run_on_main(lambda: self.update_ui(acc_info, df, tick))
            time.sleep(2)

    def start(self, e):
        if not connect_mt5():
            self.page.snack_bar = ft.SnackBar(ft.Text("MT5 Connection Failed!"))
            self.page.snack_bar.open = True
            self.page.update()
            return
        self.running = True
        self.start_btn.disabled = True
        self.stop_btn.disabled = False
        self.update()
        self.thread = threading.Thread(target=self.trading_logic, daemon=True)
        self.thread.start()

    def stop(self, e):
        self.running = False
        self.start_btn.disabled = False
        self.stop_btn.disabled = True
        self.update()

def main(page: ft.Page):
    page.title = "MT5 BTCUSD Monitor"
def main(page: ft.Page):
    page.title = "MT5 BTCUSD Monitor"
    page.theme_mode = ft.ThemeMode.DARK
    app = MT5App()
    app.page = page
    page.add(app.controls)

if __name__ == "__main__":
    ft.app(target=main)