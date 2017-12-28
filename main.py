# -*- coding: utf-8 -*-

"""
项目入口
"""

from scrapy.crawler import CrawlerProcess
from spider.spiders.category import CategorySpider


def start_spider():
    process = CrawlerProcess()
    process.crawl(CategorySpider)
    process.start()