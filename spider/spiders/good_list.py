# -*- coding: utf-8 -*-
import scrapy
from spider.pipelines import CategoryPipeline


class GoodListSpider(scrapy.Spider):
    name = 'good_list'
    allowed_domains = ['*.jd.com']

    def start_requests(self):
        cate_items = CategoryPipeline.from_crawler(self.crawler).select_list()
        for cate in cate_items:
            yield scrapy.Request(url=cate.url)

    def parse(self, response):
        pass
