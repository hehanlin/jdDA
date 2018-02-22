# -*- coding: utf-8 -*-


class CATEGORY(object):
    LEVEL_ONE = 1       # 一级分类
    LEVEL_TWO = 2       # 二级分类
    LEVEL_THREE = 3     # 三级分类
    LIST_YES = True     # 链接直接显示列表
    LIST_NO = False     # -------不----
    PATH_JOIN_MARK = "-->"      # 连接路径的符号


MAX_PAGES = 4   # 商品列表爬取的最大翻页数


class GOODDETAIL(object):
    COMMENT_URL = "https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv" \
                  "{comment_version}&productId={productId}&score={score}&sortType=6&page={page}" \
                  "&pageSize=10&isShadowSku=0&fold=1"  # 评论url
    ALL_COMMENT = 0  # 所有评论
    POOR_COMMENT = 1  # 差评
    GENERAL_COMMENT = 2  # 中评
    GOOD_COMMENT = 3  # 好评
    IMG_COMMENT = 4  # 有图
    AFTER_COMMENT = 5  # 追评
    COMMENT_MAX_PAGES = 100  # 评论最大页数
    COMMENT_PAGE_NUM = 10  # 评论每页个数
    DIFF_COMMENTS_NAME = [
        'all_comments', 'poor_comments', 'general_comments', 'good_comments', 'img_comments', 'after_comments'
    ]
