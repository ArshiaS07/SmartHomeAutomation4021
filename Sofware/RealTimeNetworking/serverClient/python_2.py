import asyncio
import websockets
from flask import Flask
import threading

app = Flask(__name__)

async def send_message_over_websocket(message, IP):
    try:
        async with websockets.connect(IP) as websocket:
            print("Connected to WebSocket server")
            await websocket.send(str(message))
            print(f"Sent message: {message}")
            response = await websocket.recv()
            print(f"Received response: {response}")
    except Exception as e:
        print(f"Error: {e}")

async def main():
    while True:
        message = 0
        await send_message_over_websocket(message, "ws://192.168.168.49:81")
        await asyncio.sleep(1)

def send_data():
    asyncio.run(main())

@app.route("/send")
def send():
    # Start a new thread to run the asyncio event loop
    thread = threading.Thread(target=send_data)
    thread.start()
    return "Sending data..."

if __name__ == "__main__":
    app.run()
