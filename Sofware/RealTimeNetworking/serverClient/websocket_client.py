import asyncio
import websockets

async def send_message_over_websocket(message):
    uri = "ws://192.168.30.156:81"                      # Replace with the correct IP address of the ESP32
    async with websockets.connect(uri) as websocket:
        await websocket.send(message)
        response = await websocket.recv()
        print(f"Received response: {response}")

async def main():
    while True:
        user_input = input("Enter 1 to turn on the LED or 0 to turn it off: ")
        if user_input == "1" or user_input == "0":
            await send_message_over_websocket(user_input)
        else:
            print("Invalid input. Please enter 1 or 0.")

asyncio.get_event_loop().run_until_complete(main())
