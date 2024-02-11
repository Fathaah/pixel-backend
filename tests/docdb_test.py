from docdb import az_cosmos_db
from product_handler import ProductHandler
from pixel_models.product import Product
import uuid

class TestCosmosDB:
    def test_add_item(self):
        cosmos = az_cosmos_db("pixel-web", "config")
        item = {
            "id": "1",
            "name": "Test Item"
        }
        cosmos.add_item(item)
        assert cosmos.get_item("1", "Test Item") == item

    def test_query_items(self):
        cosmos = az_cosmos_db("pixel-web", "config")
        query = "SELECT * FROM c"
        items = cosmos.query_items(query)
        print(items)

    def add_product(self, product):
        productHandler = ProductHandler()
        productHandler.add_product(product)
    
    def get_all_products(self):
        productHandler = ProductHandler()
        products = productHandler.get_all_products()
        print(products)

if __name__ == "__main__":
    test = TestCosmosDB()
    test.get_all_products()
    # test.add_product(
    #     Product(str(uuid.uuid4()),"Test Product", "Test Type", "Test Thumbnail", "Test Lora Model", "Test Trigger Word"))