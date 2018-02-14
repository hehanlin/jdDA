# -*- coding: utf-8 -*-
import scrapy
from spider.items import CategoryItem
from spider.consts import CATEGORY
from re import match


class CategorySpider(scrapy.Spider):
    """
    抓取分类
    """
    name = 'category'
    allowed_domains = ['www.jd.com']
    start_urls = [
        'https://www.jd.com/allSort.aspx'
    ]
    custom_settings = {
        'ITEM_PIPELINES': {
            'spider.pipelines.CategoryPipeline': 1
        }
    }

    def parse(self, response):
        level_one_cates = response.xpath(
            "//div[contains(@class, 'category-items')]//div[contains(@class, 'category-item')]"
        )
        for each in level_one_cates:
            level = CATEGORY.LEVEL_ONE
            name = each.xpath("div[@class='mt']//span/text()").get()
            url = ''        # 一级分类没有url
            path = name
            is_list = CATEGORY.LIST_NO
            yield CategoryItem(
                level=level, name=name, url=url, path=path, is_list=is_list, cat_id=None
            )
            for two_each in self.parse_level_two_cates(each, name):
                yield two_each

    def parse_level_two_cates(self, level_one_cate, level_one_name):
        """
        解析出二级分类
        :param level_one_cate: 一级分类的html节点
        :param level_one_name: 一级分类名
        :return:
        """
        level_two_cates = level_one_cate.xpath("div[@class='mc']/div[@class='items']/dl")
        for each in level_two_cates:
            level = CATEGORY.LEVEL_TWO
            name = each.xpath("dt/a/text()").get().strip()
            if not name:
                name = each.xpath("dt//text()").get().strip()
            url = each.xpath("dt/a/@href").get()
            path = self.generate_path([level_one_name, name])
            is_list = CATEGORY.LIST_NO
            yield CategoryItem(
                level=level, name=name, url=url, path=path, is_list=is_list, cat_id=None
            )
            for three_each in self.parse_level_three_cates(each, level_one_name, name):
                yield three_each

    def parse_level_three_cates(self, level_two_cate, level_one_name, level_two_name):
        """
        解析出三级分类
        :param level_two_cate: 二级分类的html节点
        :param level_one_name: 一级分类名
        :param level_two_name: 二级分类名
        :return:
        """
        level_three_cates = level_two_cate.xpath("dd/a")
        for each in level_three_cates:
            level = CATEGORY.LEVEL_THREE
            name = each.xpath("text()").get()
            url = each.xpath("@href").get()
            path = self.generate_path([level_one_name, level_two_name, name])
            re_matcher = match(r"/{0,2}list\.jd\.com/list.html\?cat=(\d+,\d+,\d+)?(.*)", url)
            if re_matcher:
                is_list = CATEGORY.LIST_YES
                cat_id = re_matcher.group(1)
            else:
                is_list = CATEGORY.LIST_NO
                cat_id = None
            yield CategoryItem(
                level=level, name=name, url=url, path=path, is_list=is_list, cat_id=cat_id
            )

    def generate_path(self, cate_list):
        """
        生成分类路径
        :return: str
        """
        return CATEGORY.PATH_JOIN_MARK.join(cate_list)







