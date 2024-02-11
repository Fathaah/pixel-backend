from azure.storage.blob import BlobServiceClient


class az_blob_storage:
    def __init__(self, account_url="https://pixelperfectstorage.blob.core.windows.net/"):
        self.account_url = account_url
        self.blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=pixelperfectstorage;AccountKey=jap64tPNR04+hMtLUionN1ENv/sv+Bmj1DDrpEEOqWjFdqnE3I//LK9a23t20Ki7x0SLUswXsw4w+AStVLjn1w==;EndpointSuffix=core.windows.net")

    # Add an Image to the Blob Storage
    def add_image(self, blob_name, image_data, container_name="images"):
        blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_client.upload_blob(image_data, overwrite=True)