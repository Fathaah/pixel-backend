import websocket
import json
from tests.test_prompt import load_test_workflow

def on_open(ws):
    print("WebSocket connection established")
    workflow = load_test_workflow()
    ws.send(json.dumps(workflow))

def on_message(ws, message):
    print("Received message:", message)

def on_close(ws):
    print("WebSocket connection closed")

if __name__ == "__main__":
    ip_address = "localhost:8083" #"85.167.36.7:40071"  # Replace with the desired IP address
    ws = websocket.WebSocketApp(f"ws://{ip_address}",
                                on_open=on_open,
                                on_message=on_message,
                                on_close=on_close)
    ws.run_forever()