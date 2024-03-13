from azure.storage.blob import BlobServiceClient


class az_blob_storage:
    def __init__(self, account_url="https://pixelperfectstorage.blob.core.windows.net/"):
        self.account_url = account_url
        self.blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=pixelperfectstorage;AccountKey=DPdTiZIGHzTU46lTGlrnHoL6EAyihSzmDGCpNXQnpDtdarmnhkv6XvDXaBE1FMuB/1SxC7P7vurK+AStIQoaGg==;EndpointSuffix=core.windows.net")

    # Add an Image to the Blob Storage
    def add_image(self, blob_name, image_data, container_name="images"):
        blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_client.upload_blob(image_data, overwrite=True)