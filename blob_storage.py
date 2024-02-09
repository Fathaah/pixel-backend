from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient


class az_blob_storage:
    def __init__(self, account_url="https://pixelperfectstorage.blob.core.windows.net/", default_credential=DefaultAzureCredential()):
        self.account_url = account_url
        self.default_credential = default_credential
        self.blob_service_client = BlobServiceClient(account_url, credential=default_credential)

    # Add an Image to the Blob Storage
    def add_image(self, blob_name, image_data, container_name="images"):
        blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_client.upload_blob(image_data, overwrite=True)
