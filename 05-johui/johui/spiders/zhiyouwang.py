# -*- coding: utf-8 -*-
import re
import scrapy

from johui.items import JohuiItem


class ZhiyouwangSpider(scrapy.Spider):
    name = 'zhiyouwang'
    allowed_domains = ['www.jobui.com']
    start_urls = ['http://www.jobui.com/']
    # 获取所有城市的名称
    navigation_url = 'http://www.jobui.com/changecity/'
    # 拼接的城市url
    city_url = 'http://www.jobui.com/cmp?area={city_name}&keyword='
    # 拼接的公司url
    company_url = 'http://www.jobui.com{company_url}'
    # 下一个的拼接链接
    next_url = 'http://www.jobui.com{next}'

    def start_requests(self):
        """请求城市列表"""
        yield scrapy.Request(url=self.navigation_url, callback=self.parse_navigation)

    def parse_navigation(self, response):
        """处理每个城市的请求"""
        city_names = list(response.xpath('/html/body/div[1]/div[3]/dl/dd/a/text()').extract())[1:]
        for city_name in city_names:
            item = JohuiItem()
            item['city_name'] = city_name
            yield scrapy.Request(url=self.city_url.format(city_name=city_name), meta={'meta_1': item}, callback=self.parse_city)

    def parse_city(self, response):
        """处理每个城市的下一页，并请求公司链接"""
        item = response.meta['meta_1']
        company_urls = response.xpath('/html/body/div/div/div/div/ul/li/div/h2/span/a[1]/@href').extract()
        for company_url in company_urls:
            yield scrapy.Request(url=self.company_url.format(company_url=company_url), meta={'meta_1': item}, callback=self.parse_company)
        # 递归请求下一页的链接
        next = response.xpath('/html/body/div/div/div/div/div/p/a[4]/@href').extract_first()
        yield scrapy.Request(url=self.next_url.format(next=next), meta={'meta_1': item}, callback=self.parse_city)

    def parse_company(self, response):
        """获取公司的详细信息"""
        item = response.meta['meta_1']
        item['company_name'] = response.xpath('//*[@id="companyH1"]/a/text()').extract_first()
        item['company_look'] = list(response.xpath('/html/body/div/div/div/div/div/div[2]/div[1]/text()').extract())[3].replace('\r\n\t\t\t\t\t\t\t\t', '').strip().replace('\xa0', '')
        item['company_info'] = str(response.xpath('//*[@id="cmp-intro"]/div/div[2]/dl/dd[1]/text()').extract_first()).strip()
        item['company_industry'] = response.xpath('//*[@id="cmp-intro"]/div/div[2]/dl/dd[2]/a/text()').extract_first()
        item['company_introduce'] = str(response.xpath('//*[@id="textShowMore"]/text()').extract_first()).strip()
        try:
            item['company_money'] = re.findall(r'<h3 class="swf-tit">(.*?)</h3>', response.text)[1]
        except Exception:
            item['company_money'] = None
        item['company_address'] = str(response.xpath('/html/body/div/div/div/div/div/div/dl/dd/span/a/@href').extract_first()).split('=')[-1]
        item['company_phone'] = str(response.xpath('/html/body/div/div/div/div/div/div/dl/div/dd/text()').extract_first()).split('/')[0].replace('\xa0', '')
        yield item