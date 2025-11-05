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

    #TODO: SEND TO KAFKA BASED ON product_ids



def on_open(ws):
    global start_time
    start_time = time.time()
    print("[Connected] Subscribing to BTC-USD ticker...")
    sub_msg = {
        "type": "subscribe",
        "product_ids": ["BTC-USD",],
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


    '''
    EXAMPLE JSON
    {
  "type": "ticker",
  "sequence": 114989267563,
  "product_id": "BTC-USD",
  "price": "103990.55",
  "open_24h": "101299.99",
  "volume_24h": "12854.56989307",
  "low_24h": "98892.97",
  "high_24h": "104125.84",
  "volume_30d": "247570.92521318",
  "best_bid": "103990.54",
  "best_bid_size": "0.09439525",
  "best_ask": "103990.55",
  "best_ask_size": "0.03974584",
  "side": "buy",
  "time": "2025-11-05T18:23:44.707176Z",
  "trade_id": 897115815,
  "last_size": "0.01904019"
}
'''