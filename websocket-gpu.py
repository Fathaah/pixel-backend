import asyncio
import websockets
import json
import requests
import threading


async def handle_message(websocket, path):
    async for message in websocket:
        # All messages are expected to be JSONs
        print(f"Received message: {message} from {path}")
        await decode_message(websocket, message)

async def decode_message(websocket, message):
    try:
        json_data = json.loads(message)

        print("Prompt received")
        # Send a response
        response = {
            "type": "response",
            "message": "Response to prompt"
        }

        # Make a POST request to localhost:8188
        payload = json_data
        headers = {'Content-Type': 'application/json'}
        await read_log_file(websocket)
        response = requests.post(comfy_url, json=payload, headers=headers)
        print(response)

        # Check the response status code
        if response.status_code == 200:
            print(f"POST request successful with message {response.content}")
        else:
            print("POST request failed")

        # await websocket.send(json.dumps(response))  # Send the response to the client


    except json.JSONDecodeError:
        print("Invalid JSON format")

async def read_log_file(websocket):
    log_file_path = './../ComfyUI/comfyui_18188.log'  # Replace with the actual path to the log file
    current_line = None

    def read_last_line():
        with open(log_file_path, 'r') as file:
            lines = file.readlines()
            if lines:
                last_line = lines[-1].strip()
        return last_line

    async def read_new_lines():
        current_line = read_last_line()
        with open(log_file_path, 'r') as file:
            file.seek(0, 2)  # Move the file pointer to the end of the file
            while True:
                print(current_line)
                line = file.readline()
                if line and line[-1] != current_line:
                    new_lines = file.readlines()[current_line.index(line[-1]) + 1:]
                    if new_lines:
                        for new_line in new_lines:
                            print(new_line.strip())
                            await websocket.send(new_line.strip())
                    current_line = line[-1]
    
    threading.Thread(target=lambda: asyncio.run(read_new_lines())).start()
    return


comfy_url = 'http://localhost:8188/prompt'
start_server = websockets.serve(handle_message, "0.0.0.0", 8083)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
