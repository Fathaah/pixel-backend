from docdb import az_cosmos_db

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

if __name__ == "__main__":
    test = TestCosmosDB()
    test.test_query_items()