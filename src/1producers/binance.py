import json
import time
import threading
import websocket

# Binance base WebSocket endpoint for combined streams
BINANCE_SOCKET_URL = "wss://stream.binance.com:9443/stream?streams="

# 10 popular symbols (trading pairs), all lowercase with 'usdt' (Binance format)
symbols = [
    "btcusdt", "ethusdt", "solusdt", "bnbusdt", "xrpusdt",
    "adausdt", "dogeusdt", "maticusdt", "ltcusdt", "linkusdt"
]

# Combine them into a single stream of 'trade' data
streams = "/".join([f"{symbol}@trade" for symbol in symbols])
FULL_SOCKET_URL = BINANCE_SOCKET_URL + streams

msg_count = 0
start_time = None

def on_message(ws, message):
    global msg_count
    msg_count += 1

    if msg_count % 100 == 0:
        print(json.dumps(json.loads(message), indent=2))
    # Uncomment to see messages:
    # print(json.dumps(json.loads(message), indent=2))

def on_open(ws):
    global start_time
    start_time = time.time()
    print(f"[Connected] Listening to trades for: {', '.join(symbols)}")

def on_close(ws, close_status_code, close_msg):
    duration = time.time() - start_time
    print(f"[Closed] Received {msg_count} messages in {duration:.2f} seconds")
    print(f"Average rate: {msg_count / duration:.2f} messages/sec")

def main():
    ws = websocket.WebSocketApp(
        FULL_SOCKET_URL,
        on_open=on_open,
    on_message=on_message,
        on_close=on_close
    )

    def run_ws():
        ws.run_forever()

    thread = threading.Thread(target=run_ws)
    thread.start()

    # Let it run for 10 seconds
    time.sleep(1)
    ws.close()

if __name__ == "__main__":
    main()