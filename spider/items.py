# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CategoryItem(scrapy.Item):
    level = scrapy.Field()  # 分类级别 consts.py
    name = scrapy.Field()
    url = scrapy.Field()
    path = scrapy.Field()   # 路径，例如: 礼品箱包-->功能箱包-->电脑包
    is_list = scrapy.Field()
    cat_id = scrapy.Field()
