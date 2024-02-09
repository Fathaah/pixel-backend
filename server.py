import uuid
import json
import urllib.request
import urllib.parse
from utils import get_gen_img_urls
from docdb import az_cosmos_db
import asyncio
import websockets
from websockets.server import serve
from websockets.sync.client import connect
from build_prompt import build_prompt
import cachetools

server_address = "127.0.0.1"
gpu_server_address = "141.195.16.189:40261"
client_id = str(uuid.uuid4())

def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req =  urllib.request.Request("http://{}/prompt".format(gpu_server_address), data=data)
    return json.loads(urllib.request.urlopen(req).read())

def build_and_queue_prompt(mini_prompt):
    prompt = build_prompt(mini_prompt)
    return queue_prompt(prompt)

def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen("http://{}/view?{}".format(gpu_server_address, url_values)) as response:
        return response.read()

def get_history(prompt_id):
    with urllib.request.urlopen("http://{}/history/{}".format(gpu_server_address, prompt_id)) as response:
        return json.loads(response.read())

def get_images(ws, prompt, ws_fe):
    prompt_id = build_and_queue_prompt(prompt)['prompt_id']
    print("Prompt id: ", prompt_id)
    output_images = {}
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            print(message)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break #Execution is done
        else:
            continue #previews are binary data
    
    print("collecting images")
    history = get_history(prompt_id)[prompt_id]
    for o in history['outputs']:
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            if 'images' in node_output:
                images_output = []
                for image in node_output['images']:
                    image_data = get_image(image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)
            output_images[node_id] = images_output

    return prompt_id, output_images

async def run_job(prompt, ws_fe):
    
    img_urls = None

    # connect to the gpu server websocket
    print("connecting to ws://{}/ws?clientId={}".format(gpu_server_address, client_id))
    with connect("ws://{}/ws?clientId={}".format(gpu_server_address, client_id)) as ws:
        # send the prompt to the gpu server
        print("sending prompt to the gpu server")
        prompt_id, images = get_images(ws, prompt, ws_fe)
        # get the images from the gpu server
        print("Run completed")
        # send the images to the frontend
        print("uploading images to the cloud updated")
        img_urls = get_gen_img_urls(images, prompt_id)
        print(img_urls)
        # close the websocket connection
        ws.close()

    print("out images ready")
    return img_urls

# move to utils
@cachetools.cached(cachetools.TTLCache(maxsize=1024, ttl=30000))
def fetch_gpu_ws():
    db_client = az_cosmos_db("config") # not good, use singleton class later
    query = "SELECT * FROM c WHERE c.id = 'gpu_server_address'"
    items = db_client.query_items(query)
    return items[0]['value']

async def on_message(ws):
    prompt = await ws.recv()
    print(f"Received prompt: {prompt}")

    # spin up the job to act on the prompt
    response = await run_job(prompt, ws)

    await ws.send(json.dumps(response))

async def main():
    async with serve(on_message, "localhost", 8083):
        print("Server started")
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())


# Spawn two threads, 1 for gpu server and 1 for the fe