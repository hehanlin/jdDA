# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from datetime import datetime
from spider.items import BrandGoodListItem, PageBrandGoodListItem
from spider.consts import MAX_PAGES


class BrandGoodlistSpider(scrapy.Spider):
    """
    根据品牌筛选商品
    """
    name = 'brandGoodList'
    allowed_domains = ['list.jd.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'spider.pipelines.BrandGoodListPipeline': 1
        }
    }

    def __init__(self, cat_id=None, brand_id=None, brand_name=None, *args, **kwargs):
        super(BrandGoodlistSpider, self).__init__(*args, **kwargs)
        self.start_url_templete = f"http://list.jd.com/list.html?cat={cat_id}&ev=exbrand_{brand_id}&page=%d" \
                                  f"&delivery=1&delivery_daofu=3&stock=1&sort=sort_commentcount_desc&trans=1"
        self.start_url = self.start_url_templete % 1
        self.brand_name = brand_name
        self._id = cat_id+"_"+brand_id

    def start_requests(self):
        yield SplashRequest(self.start_url, args={
            "images": 0,
            "wait": 3
        })

    def parse(self, response):
        good_num = response.xpath("//div[@class='s-title']//span/text()").get()
        page_num = response.xpath("//div[@id='J_topPage']//i/text()").get()
        page_num = int(page_num)
        good_list_node = response.xpath("//div[@id='plist']//div[contains(@class, 'j-sku-item')]")
        good_list = [
            {
                'title': each.xpath("div[contains(@class, 'p-name')]//em/text()").get().strip(),
                'url': each.xpath("div[contains(@class, 'p-name')]/a/@href").get(),
                'price': each.xpath("div[@class='p-price']/strong[@class='J_price']/i/text()").get(),
                'commit_num': each.xpath("div[@class='p-commit']/strong/a/text()").get(),
                'shop_name': each.xpath("div[@class='p-shop']//a/@title").get(),
                'shop_url': each.xpath("div[@class='p-shop']//a/@href").get()
            } for each in good_list_node
        ]
        update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        yield BrandGoodListItem(
            _id=self._id,
            url=self.start_url,
            good_num=good_num,
            page_num=page_num,
            good_list=good_list,
            update_time=update_time
        )
        if page_num > 1:
            page_num = page_num if page_num <= MAX_PAGES else MAX_PAGES
            for each in range(2, page_num+1):
                yield SplashRequest(url=self.start_url_templete % each,
                                    callback=self.next_pages,
                                    args={"images": 0},
                                    meta={'_id': self._id})

    def next_pages(self, response):
        good_list_node = response.xpath("//div[@id='plist']//div[contains(@class, 'j-sku-item')]")
        good_list = [
            {
                'title': each.xpath("div[contains(@class, 'p-name')]//em/text()").get().strip(),
                'url': each.xpath("div[contains(@class, 'p-name')]/a/@href").get(),
                'price': each.xpath("div[@class='p-price']/strong[@class='J_price']/i/text()").get(),
                'commit_num': each.xpath("div[@class='p-commit']/strong/a/text()").get(),
                'shop_name': each.xpath("div[@class='p-shop']//a/@title").get(),
                'shop_url': each.xpath("div[@class='p-shop']//a/@href").get()
            } for each in good_list_node
        ]
        yield PageBrandGoodListItem(
            _id=response.meta['_id'],
            good_list=good_list
        )
