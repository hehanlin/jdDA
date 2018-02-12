# -*- coding: utf-8 -*-

"""
项目调试入口
"""

from scrapy import cmdline


def start_spider():
    cmdline.execute("scrapy crawl goodList -a start_url=http://list.jd.com/list.html?cat=9987,653,655".split())


if __name__ == "__main__":
    start_spider()