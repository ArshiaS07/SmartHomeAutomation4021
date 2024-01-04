import asyncio
import websockets

async def send_message_over_websocket(message):
    uri = "ws://192.168.127.156:81"  # Replace with the correct IP address of the ESP32

    async with websockets.connect(uri) as websocket:
        await websocket.send(message)
        response = await websocket.recv()
        print(f"Received response: {response}")

# Call the function with the message you want to send
message_to_send = "Hello, ESP32!"
asyncio.get_event_loop().run_until_complete(send_message_over_websocket(message_to_send))
