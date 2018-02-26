# -*- coding: utf-8 -*-

"""
项目调试入口
"""

from scrapy import cmdline


def start_spider():
    # cmdline.execute("scrapy crawl goodList -a start_url=http://list.jd.com/list.html?cat=9987,653,655".split())
    # cmdline.execute("scrapy crawl category".split())
    # cmdline.execute("scrapy crawl brandGoodList -a cat_id=9987,653,655 -a brand_id=18374 -a brand_name=小米（MI）".split())
    cmdline.execute("scrapy crawl goodDetail -a start_url=http://item.jd.com/6029342.html".split())


if __name__ == "__main__":
    start_spider()