import websocket
import json
import time
import threading

# Replace these with your actual values
API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_API_SECRET"

# NOTE: adjust endpoint if needed
WS_URL = "wss://api.ndax.io/WSGateway/"

msg_count = 0
start_time = None


def on_open(ws):
    global start_time
    start_time = time.time()
    print("[+] Connected — sending subscription request")

    # Example payload: subscribe to trades for instrument id 74 (BT CUSD) – adjust as needed
    payload = {
        "OMSId": 1,
        "InstrumentId": 74
    }
    message = {
        "m": 0,
        "i": 1,
        "n": "SubscribeTrades",
        "o": json.dumps(payload)
    }
    ws.send(json.dumps(message))


def on_message(ws, message, start_time=None):
    global msg_count
    msg_count += 1
    # If you like: print(message)

    elapsed = time.time() - start_time
    if elapsed >= 5:
        rps = msg_count / elapsed
        print(f"[Stats] {msg_count} messages in {elapsed:.2f}s → {rps:.2f} msg/sec")
        msg_count = 0
        start_time = time.time()


def on_error(ws, error):
    print("❌ Error:", error)


def on_close(ws, close_status_code, close_msg):
    print("🔒 Closed:", close_status_code, close_msg)


if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        WS_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()