# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from spider.items import GoodListItem
from datetime import datetime


class GoodListSpider(scrapy.Spider):
    name = 'goodList'
    allowed_domains = ['list.jd.com']

    def __init__(self, start_url=None, *args, **kwargs):
        super(GoodListSpider, self).__init__(*args, **kwargs)
        self.start_url = start_url+"&page=1&sort=sort_commentcount_desc&trans=1"

    def start_requests(self):
        yield SplashRequest(self.start_url, args={
            'images': 0
        })

    def parse(self, response):
        good_num = response.xpath("//div[@class='s-title']//span/text()").get()
        brand_list_node = response.xpath("//ul[@id='brandsArea']//a")
        brand_list = [
            {
                'title': each.xpath("@title").get(),
                'url': each.xpath("@href").get()
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
            good_num=good_num,
            brand_list=brand_list,
            top_good_list=top_good_list,
            update_time=update_time
        )

        




