import asyncio
import websockets
async def send_message_over_websocket(message,IP):  # Replace with the correct IP address of the ESP32
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
        await send_message_over_websocket(message,"ws://192.168.156:81")
        #await asyncio.sleep(1)

asyncio.get_event_loop().run_until_complete(main())