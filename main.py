# -*- coding: utf-8 -*-

"""
项目入口
"""

from scrapy import cmdline

def start_spider():
    cmdline.execute("scrapy crawl category".split())


if __name__ == "__main__":
    start_spider()