# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiaoruiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 导航标题 和 url
    parentTitle = scrapy.Field()
    parentUrls = scrapy.Field()

    # 下一页
    nextUrl = scrapy.Field()

    # 小类下的子链接
    sonUrls = scrapy.Field()
    sonTitle = scrapy.Field()

    # 文章标题和内容
    head = scrapy.Field()
    content = scrapy.Field()



