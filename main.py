# -*- coding: utf-8 -*-

"""
项目入口
"""

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def start_spider():
    process = CrawlerProcess(get_project_settings())
    process.crawl('category')
    process.start()

if __name__ == "__main__":
    start_spider()