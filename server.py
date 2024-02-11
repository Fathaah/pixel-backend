import uuid
import json
import urllib.request
import urllib.parse
from utils import get_gen_img_urls
from docdb import az_cosmos_db
import asyncio
from websockets.server import serve
from websockets.sync.client import connect
from build_prompt import build_prompt
import cachetools
from flask import Flask, jsonify
from flask_sock import Sock
from product_handler import ProductHandler

server_address = "0.0.0.0"
global gpu_server_address
client_id = str(uuid.uuid4())
app = Flask(__name__)
sock = Sock(app)

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

def run_job(prompt, ws_fe):
    
    img_urls = None
    gpu_server_address = fetch_gpu_address()
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

# a get api request to fetch the gpu server address
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(ProductHandler().get_all_products())

@sock.route('/ws')
def fe_ws(sock):
    while True:
        data = sock.receive()
        print("Received data: ", data)
        response = run_job(data, sock)
        sock.send(json.dumps(response))

# move to utils
@cachetools.cached(cachetools.TTLCache(maxsize=1024, ttl=30000))
def fetch_gpu_address():
    db_client = az_cosmos_db("config") # not good, use singleton class later
    query = "SELECT * FROM c WHERE c.id = 'gpu_server_address'"
    items = db_client.query_items(query)
    return items[0]['value']

def spawn_app():
    gpu_server_address = fetch_gpu_address()
    print("GPU server address: ", gpu_server_address)
    app.run(host="localhost", port=8000, debug=True)

