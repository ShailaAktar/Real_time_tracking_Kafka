import websocket
import json
import time
import threading
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TRADIER_TOKEN")
SYMBOLS = ["AAPL", "MSFT", "TSLA", "NVDA"]  # You can adjust

count = 0
start_time = None

def on_message(ws, message):
    global count
    try:
        data = json.loads(message)
        if data.get("type") == "trade":
            count += 1
    except Exception as e:
        print("Parse error:", e)

def on_open(ws):
    global start_time
    start_time = time.time()
    print("WebSocket connection opened.")

    # Send subscription message
    request = {
        "symbols": ",".join(SYMBOLS),
        "sessionid": TOKEN,
        "linebreak": True,
        "type": "trade"
    }
    ws.send(json.dumps(request))

    # Stop after 60 seconds
    threading.Thread(target=stop_after_delay, args=(ws, 60)).start()

def stop_after_delay(ws, delay):
    time.sleep(delay)
    ws.close()
    duration = time.time() - start_time
    print(f"\n⏱ Test duration: {duration:.2f}s")
    print(f"📈 Total messages: {count}")
    print(f"⚡ Avg rate: {count / duration:.2f} messages/sec")

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, code, msg):
    print("WebSocket closed")

if __name__ == "__main__":
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }

    ws = websocket.WebSocketApp(
        "wss://ws.tradier.com/v1/",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        header=headers
    )
    ws.run_forever()