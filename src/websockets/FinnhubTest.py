import json, time, websocket, threading, os
from dotenv import load_dotenv

load_dotenv()
FINNHUB_TOKEN = os.getenv("FINNHUB_TOKEN")  # reads from your environment
TICKERS = [
    "BINANCE:BTCUSDT", "BINANCE:ETHUSDT", "BINANCE:SOLUSDT",
    "BINANCE:BNBUSDT", "BINANCE:ADAUSDT", "BINANCE:XRPUSDT",
    "AAPL", "MSFT", "TSLA", "AMZN"
]

count = 0
start_time = None

def on_message(ws, message):
    global count
    data = json.loads(message)
    if data.get("type") == "trade":
        count += len(data["data"])

def on_open(ws):
    for t in TICKERS:
        ws.send(json.dumps({"type": "subscribe", "symbol": t}))
    print(f"Subscribed to {len(TICKERS)} symbols.")
    global start_time
    start_time = time.time()
    threading.Thread(target=stop_after_delay, args=(ws, 5)).start()

def stop_after_delay(ws, delay):
    time.sleep(delay)
    ws.close()
    duration = time.time() - start_time
    print(f"\n⏱ Test duration: {duration:.2f}s")
    print(f"📈 Total messages: {count}")
    print(f"⚡ Avg rate: {count / duration:.2f} messages/sec")

def on_error(ws, error): print("Error:", error)
def on_close(ws, close_status_code, close_msg): print("WebSocket closed")

if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        f"wss://ws.finnhub.io?token={FINNHUB_TOKEN}",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()