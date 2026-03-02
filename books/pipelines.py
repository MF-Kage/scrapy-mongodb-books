# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib
import pymongo
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class BooksPipeline:
    def process_item(self, item, spider):
        return item


class MongoPipeline:
    def __init__(self, mongo_uri: str, mongo_db: str, mongo_collection: str):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection
        self.client = None
        self.db = None
        self.collection = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE"),
            mongo_collection=crawler.settings.get("MONGO_COLLECTION", "books"),
        )


    # spider argument kept optional to avoid Scrapy deprecation warnings
    def open_spider(self, spider=None):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.mongo_collection]

    def close_spider(self, spider=None):
        if self.client:
            self.client.close()

    def process_item(self, item, spider=None):
        item_id = self.compute_item_id(item)
        item_dict = ItemAdapter(item).asdict()

        self.collection.update_one(
            {"_id": item_id},
            {"$set": item_dict},
            upsert=True,
        )
        return item

    @staticmethod
    def compute_item_id(item) -> str:
        url = item["url"]
        return hashlib.sha256(url.encode("utf-8")).hexdigest()
