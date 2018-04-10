# -*- coding: utf-8 -*-
import os

import scrapy

from XiaoRui.items import XiaoruiItem


class XiaoruiSpider(scrapy.Spider):
    name = 'xiaorui'
    # allowed_domains = ['xiaorui.cc']
    start_urls = ['http://xiaorui.cc/']

    def parse(self, response):
        # 用于传递上下文
        items = []
        # 所有大类的url 和 标题
        parentUrls = response.xpath('//*[@id="zan-header"]/nav/div/ul/li/a/@href').extract()
        parentTitle = response.xpath('//*[@id="zan-header"]/nav/div/ul/li/a/text()').extract()
        other = response.xpath('//*[@id="zan-header"]/nav/div/ul/li/ul/li/a/@href').extract()
        other_title = response.xpath('//*[@id="zan-header"]/nav/div/ul/li/ul/li/a/text()').extract()
        # 删除混淆的无用链接
        del parentUrls[5:]
        del parentTitle[5:]
        # 拼接
        parentUrls += other[:-4]
        parentTitle += other_title[:-4]

        for i in range(0, len(parentTitle)):
            # 指定大类目录的路径和目录名
            parentFilename = "./Data/" + parentTitle[i]

            # 如果目录不存在，则创建目录
            if (not os.path.exists(parentFilename)):
                os.makedirs(parentFilename)

            item = XiaoruiItem()

            # 保存大类的title和urls
            item['parentTitle'] = parentTitle[i]
            item['parentUrls'] = parentUrls[i]
            items.append(item)

        # 爬取每个分类下的数据
        for item in items:
            yield scrapy.Request(url=item['parentUrls'], meta={'meta_1': item}, callback=self.second_parse)

    def second_parse(self, response):
        # 接收上下文
        meta_1 = response.meta['meta_1']
        # 获取下一页的链接
        next_page = response.xpath('//*[@id="load-more"]/@href').extract()
        # 判断是否存在下一页,存在进行递归
        if next_page:
            yield scrapy.Request(url=next_page[0], meta={'meta_1': meta_1}, callback=self.second_parse)
        sonUrls = response.xpath('//*[@id="mainstay"]/div/section[1]/a/@href').extract()
        sonTitle = response.xpath('//*[@id="mainstay"]/div/section[1]/div[1]/h1/a/text()').extract()
        item = XiaoruiItem()
        item['parentTitle'] = meta_1['parentTitle']
        item['parentUrls'] = meta_1['parentUrls']
        item['sonUrls'] = sonUrls
        item['sonTitle'] = sonTitle
        # 获取每一页的数据
        for sonUrl in sonUrls:
            yield scrapy.Request(url=sonUrl, meta={'meta_1': item}, callback=self.third_parse)

    def third_parse(self, response):
        item = XiaoruiItem()
        # 接收上下文
        meta_1 = response.meta['meta_1']
        article = response.body.decode()
        head = response.xpath('//*[@id="zan-bodyer"]/div/section/div/article/div[1]/div[1]/h1/a/text()').extract()[0]
        item['parentTitle'] = meta_1['parentTitle']
        item['parentUrls'] = meta_1['parentUrls']
        item['sonUrls'] = meta_1['sonUrls']
        item['sonTitle'] = meta_1['sonTitle']
        item['head'] =head
        item['content'] = article
        yield item