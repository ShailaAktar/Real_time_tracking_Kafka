import websocket
import json
import time
from dotenv import load_dotenv
import os


load_dotenv()
API_KEY = os.getenv("MASSIVE_API_KEY")
SOCKET_URL = "wss://socket.massive.com/stocks"  # Real-time WebSocket endpoint

def on_open(ws):
    print("[+] Connected. Authenticating...")
    auth_msg = {
        "action": "auth",
        "params": API_KEY
    }
    ws.send(json.dumps(auth_msg))

def on_message(ws, message):
    try:
        data = json.loads(message)
        for msg in data:
            if msg.get("ev") == "status":
                print(f"STATUS: {msg}")
                if msg["status"] == "auth_success":
                    print("[+] Authenticated. Subscribing to AAPL + MSFT (per-minute aggregates)...")
                    sub_msg = {
                        "action": "subscribe",
                        "params": "AM.AAPL,AM.MSFT"
                    }
                    ws.send(json.dumps(sub_msg))
            elif msg.get("ev") == "AM":  # Aggregate Minute data
                print(f"[DATA] {msg['sym']}: Open {msg['o']} → Close {msg['c']} Vol: {msg['v']}")
            else:
                print("[Other Event]", msg)
    except Exception as e:
        print("Error parsing:", e)

def on_close(ws, code, msg):
    print(f"[-] Disconnected. Code: {code}, Msg: {msg}")

def on_error(ws, error):
    print("Error:", error)

if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        SOCKET_URL,
        on_open=on_open,
        on_message=on_message,
        on_close=on_close,
        on_error=on_error
    )
    ws.run_forever()