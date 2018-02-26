# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from re import search, S
from spider.items import GoodDetailItem, CommentListItem
from spider.consts import GOODDETAIL
from chardet import detect
from json import loads
from math import ceil
from spider.settings import DOWNLOADER_MIDDLEWARES


class GoodDetailSpider(scrapy.Spider):
    name = 'goodDetail'
    allowed_domains = ['item.jd.com', 'sclub.jd.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'spider.pipelines.GoodDetailPipeline': 1
        }
    }

    def __init__(self, start_url=None, *args, **kwargs):
        super(GoodDetailSpider, self).__init__(*args, **kwargs)
        self.start_url = start_url
        self._id = search(r"(\d+).html", start_url).group(1)

    def start_requests(self):
        yield SplashRequest(url=self.start_url, args={
            "images": 0,
            "wait": 3
        })

    def parse(self, response):
        ids = response.xpath("//div[@class='dd']/div/@data-sku").extract()
        img = response.xpath("//img[@id='spec-img']/@src").get()
        name = response.xpath("//div[@class='sku-name']/text()").get().strip()
        desc = response.xpath("//div[@class='news']/div[@id='p-ad']/@title").get()
        price = response.xpath("//div[contains(@class, 'J-summary-price')]//span[@class='p-price']/"
                               "span[contains(@class, 'price')]/text()").get()
        comment_count = response.xpath("//div[@id='comment-count']/a/text()").get()
        attr_node_list = response.xpath("//div[@id='choose-attrs']/div[contains(@class, 'p-choose')]")
        attr_list = [
            {
                'name': each.xpath("@data-type").get(),
                'values': each.xpath("div[@class='dd']/div/@data-value").extract()
            } for each in attr_node_list
        ]
        self.comment_version = search(r"commentVersion:\'(\d+)\'", response.text, S).group(1)
        item = GoodDetailItem(
            _id=self._id,
            url=self.start_url,
            ids=ids,
            name=name,
            img=img,
            desc=desc,
            price=price,
            comment_count=comment_count,
            attr_list=attr_list
        )
        comment_url = GOODDETAIL.COMMENT_URL.format(
            comment_version=self.comment_version,
            productId=self._id,
            score=GOODDETAIL.ALL_COMMENT,
            page=0
        )
        yield scrapy.Request(
            url=comment_url,
            headers={
                "Referer": self.start_url
            },
            meta={
                'item': item
            },
            callback=self.get_comment_summary
        )

    def get_comment_summary(self, response):
        try:
            body = response.body.decode("GB2312", 'ignore')
        except:
            gass_charset = detect(response.body)
            encoding = gass_charset.get('encoding', '')
            body = response.body.decode(encoding, 'ignore')
        comment_json = search(r"\((.*)\)", body, S)
        if comment_json and comment_json.group(1):
            data = loads(comment_json.group(1))
            good_detail_item = response.meta.get('item')
            good_detail_item['comment_desc'] = data
            good_detail_item['comment_desc']['after_comments'] = list()
            good_detail_item['comment_desc']['img_comments'] = list()
            good_detail_item['comment_desc']['general_comments'] = list()
            good_detail_item['comment_desc']['poor_comments'] = list()
            yield good_detail_item
            # 所有评论
            max_page = data.get('maxPage', 1)

            yield from self.get_diff_comment(GOODDETAIL.ALL_COMMENT, max_page)
            # 追评
            after_count = data['productCommentSummary']['afterCount']
            after_page = ceil(after_count/GOODDETAIL.COMMENT_PAGE_NUM)
            yield from self.get_diff_comment(GOODDETAIL.AFTER_COMMENT, after_page)
            # 有图
            img_count = data['imageListCount']
            img_page = ceil(img_count/GOODDETAIL.COMMENT_PAGE_NUM)
            yield from self.get_diff_comment(GOODDETAIL.IMG_COMMENT, img_page)
            # 中评
            general_count = data['productCommentSummary']['generalCount']
            general_page = ceil(general_count/GOODDETAIL.COMMENT_PAGE_NUM)
            yield from self.get_diff_comment(GOODDETAIL.GENERAL_COMMENT, general_page)
            # 差评
            poor_count = data['productCommentSummary']['poorCount']
            poor_page = ceil(poor_count/GOODDETAIL.COMMENT_PAGE_NUM)
            yield from self.get_diff_comment(GOODDETAIL.POOR_COMMENT, poor_page)

    def get_diff_comment(self, score, max_page):
        start_page = 1 if score == 0 else 0
        max_page = max_page if max_page < GOODDETAIL.COMMENT_MAX_PAGES else GOODDETAIL.COMMENT_MAX_PAGES
        for i in range(start_page, int(max_page+1)):
            yield scrapy.Request(
                url=GOODDETAIL.COMMENT_URL.format(
                    comment_version=self.comment_version,
                    productId=self._id,
                    score=score,
                    page=i
                ),
                headers={
                    "Referer": self.start_url
                },
                meta={
                    'score': score
                },
                callback=self.get_all_comment
            )

    def get_all_comment(self, response):
        try:
            body = response.body.decode("GB2312", 'ignore')
        except:
            gass_charset = detect(response.body)
            encoding = gass_charset.get('encoding', '')
            body = response.body.decode(encoding, 'ignore')
        comment_json = search(r"\((.*)\)", body, S)
        if comment_json and comment_json.group(1):
            data = loads(comment_json.group(1))
            comments = data.get('comments')
            yield CommentListItem(
                _id=self._id,
                comment_list=comments,
                score=response.meta.get('score')
            )






