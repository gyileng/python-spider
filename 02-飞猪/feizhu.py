from datetime import datetime
import sys
import os
import re
import json
import time

import pymongo as pymongo
from selenium import webdriver

currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)

from config import city, MONGO_TABLE, MONGO_DB, MONGO_URL
# 链接mongo
client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]


class FeiZzhu(object):
    i = 1
    def __init__(self, start_time, end_time, user_city):
        self.city = user_city
        if start_time == '':
            start_time = str(datetime.utcnow()).split(' ')[0]
        if end_time == '':
            end_time = str(datetime.utcnow()).split(' ')[0]
        self.dr = webdriver.Chrome()
        self.url = 'https://h5.m.taobao.com/trip/hotel/searchlist/index.html?_projVer=1.0.16&isOneSearch=false&guid=1521270890646786407&checkIn={0}&checkOut={1}&%{2}cityCode=469005&cityName={3}&ttid=201300%40travel_h5_3.1.0&cityCode={4}&isLBS=false'.format(
            start_time, end_time, city[user_city][0], user_city, city[user_city][1])

    def get_ajax_url(self):
        dr = self.dr
        dr.get(self.url)
        for i in range(2):
            target = dr.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[1]/div/div/div[last()]')
            dr.execute_script("arguments[0].scrollIntoView();", target)
            time.sleep(3)
        html = dr.page_source
        ajax_url = re.findall(r'script src="(.*?)"></script>', html)
        ajax_urls = []
        for i in ajax_url:
            ajax_urls.append(i.replace(';', '').replace('amp', ''))
        return ajax_urls

    def get_data(self, ajax_urls):
        ajax_urls.pop(0)
        ajax_urls.pop(1)
        ajax_urls.pop(1)
        datas = []
        for ajax_url in ajax_urls:
            js = 'window.open("{}");'.format(ajax_url)
            self.dr.get(ajax_url)
            data = self.dr.page_source
            datas.append(data)
            time.sleep(2)
        # 关闭浏览器
        self.dr.quit()
        return datas

    def paese_data(self, datas):
        for data in datas:
            num = data[131]
            data = data.replace(
                '<html xmlns="http://www.w3.org/1999/xhtml"><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;"> mtopjsonp{}('.format(
                    num), '').replace(')</pre></body></html>', '')
            data = json.loads(data)
            results = data['data']['sections']
            for result in results:
                hotel_results = result['items']
                hotel = {}
                for i in hotel_results:
                    try:
                        hotel['name'] = i['name']
                        hotel['picUrl'] = i['picUrl']
                        hotel['star'] = i['star']
                        hotel['realAddress'] = i['realAddress']
                        hotel['price'] = i['price'].replace('00', '')
                        hotel['rateNumber'] = i['rateNumber']
                        hotel['scoreDesc'] = i['scoreDesc']
                        hotel['lastBookingDescription'] = i['lastBookingDescription']
                        hotel['rateCount'] = i['rateCount']
                        hotel['tel'] = i['tel']
                    except Exception:
                        continue
                    yield hotel

    def save_mongodb(self, result):
        """保存到mongodb"""
        try:
            if db[MONGO_TABLE[self.city]].insert(result):
                print('第{0}页内容存储数据成功'.format(FeiZzhu.i))
                FeiZzhu.i += 1
        except Exception:
            print('第{0}页内容存储数据出错'.format(FeiZzhu.i), result)
            FeiZzhu.i += 1

    def main(self):
        ajax_urls = self.get_ajax_url()
        datas = self.get_data(ajax_urls)
        hotels = self.paese_data(datas)
        self.save_mongodb(hotels)


if __name__ == '__main__':
    user_city = input('请输入旅游城市:')
    st = input('请输入开始时间(回车代表当日):')
    et = input('请输入结束时间(回车代表当日):')
    feizhu = FeiZzhu(st, et, user_city)
    feizhu.main()
