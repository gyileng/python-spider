# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JohuiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 城市名称
    city_name = scrapy.Field()
    # 公司名称
    company_name = scrapy.Field()
    # 浏览人数
    company_look = scrapy.Field()
    # 公司信息
    company_info = scrapy.Field()
    # 公司类型
    company_industry = scrapy.Field()
    # 公司简介
    company_introduce = scrapy.Field()
    # 平均薪资
    company_money = scrapy.Field()
    # 公司地址
    company_address = scrapy.Field()
    # 公司电话
    company_phone = scrapy.Field()
