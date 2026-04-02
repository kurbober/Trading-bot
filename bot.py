import coinbase_pro as cbpro
import time
import pandas as pd

# --- COINBASE API SETUP ---
API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_API_SECRET"
API_PASSPHRASE = "YOUR_API_PASSPHRASE"

auth_client = cbpro.AuthenticatedClient(API_KEY, API_SECRET, API_PASSPHRASE)

# --- Multi-Coin Setup ---
SYMBOLS = ["BTC-GBP", "ETH-GBP", "ADA-GBP"]  # Add more if desired
TRADE_SIZE_PERCENT = 0.3  # Aggressive but controlled
STOP_LOSS_PERCENT = 0.03  # 3% max loss per trade

# --- STRATEGY LOGIC ---
price_history = {symbol: [] for symbol in SYMBOLS}

def get_price(symbol):
    ticker = auth_client.get_product_ticker(product_id=symbol)
    return float(ticker['price'])

def strategy(symbol, price):
    price_history[symbol].append(price)
    if len(price_history[symbol]) < 30:
        return None

    df = pd.DataFrame(price_history[symbol], columns=['price'])
    df['ma_fast'] = df['price'].rolling(5).mean()
    df['ma_slow'] = df['price'].rolling(20).mean()

    if df['ma_fast'].iloc[-1] > df['ma_slow'].iloc[-1]:
        return "buy"
    elif df['ma_fast'].iloc[-1] < df['ma_slow'].iloc[-1]:
        return "sell"
    return None

# --- EXECUTION LOGIC (TEST MODE) ---
def execute_trade(symbol, signal):
    # TEST MODE: do not place real trades yet
    print(f"[TEST MODE] Signal for {symbol}: {signal}")

# --- MAIN LOOP ---
while True:
    try:
        for symbol in SYMBOLS:
            price = get_price(symbol)
            signal = strategy(symbol, price)
            if signal:
                execute_trade(symbol, signal)
            else:
                print(f"[TEST MODE] No signal for {symbol}, price: £{price:.2f}")
    except Exception as e:
        print("Error:", e)
    
    time.sleep(60)
