import json
import websocket
import time

# Coinbase WebSocket endpoint
SOCKET_URL = "wss://ws-feed.exchange.coinbase.com"

# Counter for messages
msg_count = 0
start_time = None

def on_message(ws, message):
    global msg_count
    msg_count += 1
    data = json.loads(message)
    print(json.dumps(data, indent=2))


def on_open(ws):
    global start_time
    start_time = time.time()
    print("[Connected] Subscribing to BTC-USD ticker...")
    sub_msg = {
        "type": "subscribe",
        "product_ids": [
  "BTC-USD",
],
        "channels": ["ticker"]
    }
    ws.send(json.dumps(sub_msg))

def on_close(ws, close_status_code, close_msg):
    print(f"[Closed] Received {msg_count} messages in {time.time() - start_time:.2f} seconds")
    print(f"Average rate: {msg_count / (time.time() - start_time):.2f} messages/sec")

def main():
    ws = websocket.WebSocketApp(
        SOCKET_URL,
        on_open=on_open,
        on_message=on_message,
        on_close=on_close
    )

    # Run connection for 5 seconds
    def run_for_duration():
        ws.run_forever(dispatcher=None)
    import threading
    thread = threading.Thread(target=run_for_duration)
    thread.start()
    time.sleep(5)
    ws.close()

if __name__ == "__main__":
    main()