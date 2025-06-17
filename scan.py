import yfinance as yf
import time
from discord_webhook import DiscordWebhook

# ตั้งค่า Discord webhook URL
DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/1384171755467178135/Szx_jssc8k0PjLSbDhfxPYUaJHzLLRSoX6V4PWaEzjxkRAw8pdy2wmJmWK2MbIsIVRxu"

# ตัวอย่างรายชื่อหุ้นอเมริกา 100 ตัว (ควรแทนที่ด้วยหุ้นที่ต้องการ)
TICKERS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "BRK-B", "JPM", "V",
    "UNH", "HD", "MA", "PG", "LLY", "XOM", "MRK", "ABBV", "AVGO", "PEP",
    "COST", "KO", "WMT", "ADBE", "CSCO", "MCD", "BAC", "CRM", "TMO", "DIS",
    "ABT", "CVX", "ACN", "DHR", "NKE", "LIN", "TXN", "NEE", "WFC", "QCOM",
    "PM", "HON", "AMGN", "UNP", "MDT", "MS", "INTC", "LOW", "BMY", "SBUX",
    "RTX", "AMAT", "GS", "CAT", "ISRG", "BLK", "LMT", "GE", "NOW", "DE",
    "SPGI", "PLD", "SYK", "TGT", "ZTS", "CB", "C", "SCHW", "MU", "USB",
    "GILD", "MDLZ", "ADI", "MO", "BKNG", "MMC", "CI", "REGN", "ADP", "ELV",
    "SO", "PNC", "BDX", "DUK", "TFC", "AON", "ITW", "SHW", "CSX", "PGR",
    "APD", "ICE", "EW", "CL", "FISV", "FDX", "GM", "HUM", "MET", "PSA"
]

def get_macd(df):
    exp12 = df['Close'].ewm(span=12, adjust=False).mean()
    exp26 = df['Close'].ewm(span=26, adjust=False).mean()
    macd = exp12 - exp26
    return macd

def check_breakout(df):
    # breakout = ราคาปิดล่าสุด > high 20 วันก่อนหน้า
    last_close = df['Close'].iloc[-1]
    prev_high = df['High'].iloc[-21:-1].max()
    return last_close > prev_high

def notify_discord(message):
    webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL, content=message)
    webhook.execute()

def scan_stocks():
    breakout_stocks = []
    for ticker in TICKERS:
        try:
            df = yf.download(ticker, period="2mo", interval="1d", progress=False)
            if len(df) < 30:
                continue
            macd = get_macd(df)
            if check_breakout(df) and macd.iloc[-1] > 0:
                breakout_stocks.append(ticker)
        except Exception as e:
            print(f"Error for {ticker}: {e}")
        time.sleep(0.5)

    if breakout_stocks:
        message = f"หุ้น breakout + MACD > 0: {', '.join(breakout_stocks)}"
        notify_discord(message)
    else:
        print("No breakout stocks found.")

if __name__ == "__main__":
        message = f"หุ้น breakout + MACD > 0:"
        notify_discord(message)
