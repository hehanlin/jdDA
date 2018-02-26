# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from spider.items import GoodListItem
from datetime import datetime
from re import search


class GoodListSpider(scrapy.Spider):
    name = 'goodList'
    allowed_domains = ['list.jd.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'spider.pipelines.GoodListPipeline': 1
        }
    }

    def __init__(self, start_url=None, *args, **kwargs):
        super(GoodListSpider, self).__init__(*args, **kwargs)
        self.url = start_url
        self._id = self.url.split("=")[1]
        self.start_url = start_url+"&page=1&sort=sort_commentcount_desc&trans=1"

    def start_requests(self):
        yield SplashRequest(self.start_url, args={
            "images": 0,
            "wait": 3
        })

    def parse(self, response):
        good_num = response.xpath("//div[@class='s-title']//span/text()").get()
        page_num = response.xpath("//div[@id='J_topPage']//i/text()").get()
        brand_list_node = response.xpath("//ul[@id='brandsArea']//a")
        brand_list = [
            {
                'title': each.xpath("@title").get(),
                'url': each.xpath("@href").get(),
                'brand_id': search(r"exbrand%5F(\d+)&", each.xpath("@href").get()).group(1)
            } for each in brand_list_node
        ]
        top_good_list_node = response.xpath("//div[@id='plist']//div[contains(@class, 'j-sku-item')]")
        top_good_list = [
            {
                'title': each.xpath("div[contains(@class, 'p-name')]//em/text()").get().strip(),
                'url': each.xpath("div[contains(@class, 'p-name')]/a/@href").get(),
                'price': each.xpath("div[@class='p-price']/strong[@class='J_price']/i/text()").get(),
                'commit_num': each.xpath("div[@class='p-commit']/strong/a/text()").get(),
                'shop_name': each.xpath("div[@class='p-shop']//a/@title").get(),
                'shop_url': each.xpath("div[@class='p-shop']//a/@href").get()
            } for each in top_good_list_node
        ]
        update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        yield GoodListItem(
            _id=self._id,
            url=self.url,
            good_num=good_num,
            page_num=page_num,
            brand_list=brand_list,
            top_good_list=top_good_list,
            update_time=update_time
        )

        




