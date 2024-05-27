from azure.cosmos import exceptions, CosmosClient, PartitionKey
import json
import os

class az_cosmos_db:
    def __init__(self, container_name, database_name="pixel-web" , endpoint="https://pixel-docdb.documents.azure.com:443/"):
        self.endpoint = endpoint
        self.database_name = database_name
        self.container_name = container_name
        self.client = CosmosClient(endpoint, os.environ.get("COSMOS_KEY"))
        self.database = self.client.get_database_client(database_name)
        self.container = self.database.get_container_client(container_name)

    def add_item(self, item):
        self.container.upsert_item(item)

    def query_items(self, query):
        items = list(self.container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        return items

    def get_item(self, item_id, partition_key):
        item = self.container.read_item(item=item_id, partition_key=partition_key)
        return item
    
    def strip_meta(self, doc):

        meta_props = ["_rid", "_ts", "_self", "_etag", "_attachments"]
        new_doc = {}
        for prop in doc:
            if prop not in meta_props:
                new_doc[prop] = doc[prop]
        
        return new_doc
