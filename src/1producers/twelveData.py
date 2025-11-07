import json
import time
import websocket
import threading

# ✅ Your TwelveData WebSocket API key
API_KEY = ""

msg_count = 0
start_time = time.time()

def on_message(ws, message):
    global msg_count
    msg_count += 1
    print(message)

def on_error(ws, error):
    print("❌ Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("🔒 Connection closed:", close_status_code, close_msg)

def on_open(ws):
    print("[+] WebSocket open — subscribing to AAPL")
    subscribe_msg = {
        "action": "subscribe",
        "params": {
            "symbols": "AAPL"
        }
    }
    ws.send(json.dumps(subscribe_msg))

    # Auto-close after 5 seconds
    def close_after_delay():
        time.sleep(5)
        ws.close()

    threading.Thread(target=close_after_delay).start()

if __name__ == "__main__":
    socket_url = f"wss://ws.twelvedata.com/v1/quotes/price?apikey={API_KEY}"
    ws = websocket.WebSocketApp(
        socket_url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    print("[*] Connecting to TwelveData WebSocket...")
    ws.run_forever()

    # After close, print summary
    elapsed = time.time() - start_time
    if elapsed > 0:
        rps = msg_count / elapsed
        print(f"\n📊 Final Stats: {msg_count} messages in {elapsed:.2f}s → {rps:.2f} msg/sec")