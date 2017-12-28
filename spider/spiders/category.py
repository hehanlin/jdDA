# -*- coding: utf-8 -*-
import scrapy
import json
import chardet

class CategorySpider(scrapy.Spider):
    name = 'category'
    allowed_domains = ['www.jd.com', 'dc.3.cn']
    start_urls = ['https://dc.3.cn/category/get?callback=getCategoryCallback']

    def parse(self, response):
        json_bytes = response.body
        json_encode = chardet.detect(json_bytes).get('encoding', 'utf-8')
        json_str = json_bytes.decode(json_encode, errors="ignore")[28:-4]




