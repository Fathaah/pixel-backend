from docdb import az_cosmos_db
from pixel_models.product import Product
import dataclasses

class ProductHandler:
    def __init__(self):
        self.db = az_cosmos_db("products")

    def get_all_products(self):
        query = "SELECT * FROM c"
        items = self.db.query_items(query)
        # filter _rfid, _etag, _ts, _attachments, _self
        items = [self.db.strip_meta(item) for item in items]
        products = [Product(**item) for item in items]
        return products

    def get_product(self, product_id):
        query = f"SELECT * FROM c WHERE c.id = '{product_id}'"
        return self.db.query_items(query)

    def add_product(self, product: Product):
        # add product to the database
        data = (dataclasses.asdict(product))
        self.db.add_item(data)

    def update_product(self, product):
        self.db.add_item(product)
        return product

    def delete_product(self, product_id):
        product = self.get_product(product_id)
        self.db.container.delete_item(item=product, partition_key=product_id)
        return product