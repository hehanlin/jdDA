# -*- coding: utf-8 -*-
import scrapy
import json
from json import JSONDecodeError
import chardet
from spider.items import CategoryItem
from spider.consts import CATEGORY
import hashlib


class CategorySpider(scrapy.Spider):
    """
    抓取分类
    """
    name = 'category'
    allowed_domains = ['www.jd.com']
    start_urls = [
        'https://www.jd.com/allSort.aspx'
    ]
    custom_settings = {
        'ITEM_PIPELINES': {
            'spider.pipelines.CategoryPipeline': 1
        }
    }

    def parse(self, response):
        level_one_cates = response.xpath(
            "//div[contains(@class, 'category-items')]//div[contains(@class, 'category-item')]"
        )
        for each in level_one_cates:
            level = CATEGORY.LEVEL_ONE
            name = each.xpath("//div[@class, 'mt']//span/text()").extract()
            url = ''
            m = hashlib.md5()
            m.update(
                str(level)+name+url
            )
            hash_str = m.hexdigest()
            yield CategoryItem(
                level=CATEGORY.LEVEL_ONE,
                name=name,
                url=url,
                hash_str=hash_str
            )




