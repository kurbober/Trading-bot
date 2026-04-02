import requests
import time
import pandas as pd

API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_API_SECRET"

BASE_URL = "https://api.coinbase.com/v2/prices/BTC-GBP/spot"

def get_price():
    res = requests.get(BASE_URL).json()
    return float(res['data']['amount'])

prices = []

def strategy(price):
    prices.append(price)

    if len(prices) < 30:
        return None

    df = pd.DataFrame(prices, columns=['price'])
    df['ma_fast'] = df['price'].rolling(5).mean()
    df['ma_slow'] = df['price'].rolling(20).mean()

    if df['ma_fast'].iloc[-1] > df['ma_slow'].iloc[-1]:
        return "buy"
    elif df['ma_fast'].iloc[-1] < df['ma_slow'].iloc[-1]:
        return "sell"
    return None

def execute(signal):
    print("Signal:", signal)

while True:
    try:
        price = get_price()
        print("Price:", price)

        signal = strategy(price)
        execute(signal)

    except Exception as e:
        print("Error:", e)

    time.sleep(60)
