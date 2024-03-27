from docdb import az_cosmos_db
from pixel_models.demo_dao import demo_dao
import dataclasses

class DemoDaoHandler:
    def __init__(self):
        self.db = az_cosmos_db("demo_request")

    def get_all_demo(self):
        query = "SELECT * FROM c"
        items = self.db.query_items(query)
        # filter _rfid, _etag, _ts, _attachments, _self
        items = [self.db.strip_meta(item) for item in items]
        demo = [demo_dao(**item) for item in items]
        return demo

    def get_demo(self, demo_id):
        query = f"SELECT * FROM c WHERE c.id = '{demo_id}'"
        return self.db.query_items(query)

    def add_demo(self, demo_request: demo_dao):
        # add demo to the database
        data = (dataclasses.asdict(demo_request))
        self.db.add_item(data)

    def update_demo(self, demo):
        self.db.add_item(demo)
        return demo

    def delete_demo(self, demo_id):
        demo = self.get_demo(demo_id)
        self.db.container.delete_item(item=demo, partition_key=demo_id)
        return demo