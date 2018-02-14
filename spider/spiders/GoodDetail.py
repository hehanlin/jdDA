# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class GoodDetailSpider(scrapy.Spider):
    name = 'GoodDetail'
    allowed_domains = ['item.jd.com']

    def __init__(self, start_url=None, *args, **kwargs):
        super(GoodDetailSpider, self).__init__(*args, **kwargs)
        self.url = start_url

    def start_requests(self):
        yield SplashRequest(url=self.url, args={
            'images': 0
        })

    def parse(self, response):
        pass