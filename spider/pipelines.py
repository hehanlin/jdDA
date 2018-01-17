# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo


class SpiderPipeline(object):

    def process_item(self, item, spider):
        return item


class MongoPipeline(object):

    collection_name = None

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DB")
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if not self.collection_name:
            raise NotImplementedError
        self.db[self.collection_name].insert(dict(item))
        return item


class CategoryPipeline(MongoPipeline):

    collection_name = "category"

    def open_spider(self, spider):
        super().open_spider(spider)
        self.db[self.collection_name].remove()
