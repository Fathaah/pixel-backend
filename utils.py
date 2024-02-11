import json
from PIL import Image
from io import BytesIO
from blob_storage import az_blob_storage
import cachetools

# @cachetools.cached(cachetools.TTLCache(maxsize=1024, ttl=900000))
def load_json_from_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def get_gen_img_urls(images, prompt_id):
    store = az_blob_storage()
    # convert the binary data to image png
    img_base_url = "https://pixelperfectstorage.blob.core.windows.net/images/"
    image_urls = []
    for node_id in images:
        for i, image_data in enumerate(images[node_id]):
            img = Image.open(BytesIO(image_data))
            # save the image to the blob storage
            store.add_image(f"{prompt_id}_{node_id}_{i}.png", image_data)
            image_urls.append(f"{img_base_url}{prompt_id}_{node_id}_{i}.png")
    return image_urls
