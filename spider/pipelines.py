# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from spider.items import BrandGoodListItem, PageBrandGoodListItem, GoodDetailItem, CommentListItem
from spider.consts import GOODDETAIL


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
        self.db[self.collection_name].drop()
        self.db.create_collection(self.collection_name)
        self.db.get_collection(self.collection_name).create_index([("path", pymongo.TEXT)])

    def select_list(self):
        """
        查询出是list的category
        :return: list
        """
        super().open_spider(None)
        return self.db[self.collection_name].find({"is_list": True})


class GoodListPipeline(MongoPipeline):

    collection_name = "good_list"

    def process_item(self, item, spider):
        self.db[self.collection_name].update(
            spec={"_id": item["_id"]},
            document=item,
            upsert=True
        )


class BrandGoodListPipeline(MongoPipeline):

    collection_name = "brand_good_list"

    def process_item(self, item, spider):
        if isinstance(item, BrandGoodListItem):
            self.db[self.collection_name].save(item)
        elif isinstance(item, PageBrandGoodListItem):
            self.db[self.collection_name].update(
                spec={"_id": item['_id']},
                document={"$push": {"good_list": {"$each": item['good_list']}}}
            )


class GoodDetailPipeline(MongoPipeline):

    collection_name = "good_detail"

    def process_item(self, item, spider):
        if isinstance(item, GoodDetailItem):
            self.db[self.collection_name].save(item)
        elif isinstance(item, CommentListItem):
            score = item['score']
            comment_name = GOODDETAIL.DIFF_COMMENTS_NAME[score]
            self.db[self.collection_name].update(
                spec={"_id": item['_id']},
                document={"$push": {comment_name: {"$each": item['comment_list']}}}
            )



