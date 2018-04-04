# -*- coding:utf-8 -*-
import json
import re
from datetime import datetime
from multiprocessing import Pool

import pymongo
import requests

from config import MONGO_URL, MONGO_DB, MONGO_TABLE, city_dict, url_dict, base_city

# 链接mongo
client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]


class XieCheng(object):
    def __init__(self, start_time, end_time, city):
        """初始化"""
        self.city = city
        self.url = url_dict[city]
        self.headers = {
            'Referer': 'http://hotels.ctrip.com/hotel/beijing1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
        }
        if start_time == '':
            start_time = str(datetime.utcnow()).split(' ')[0]
        if end_time == '':
            end_time = str(datetime.utcnow()).split(' ')[0]

        city_dict[city].update(base_city)
        self.data = city_dict[city]

        self.data['StartTime'] = start_time
        self.data['DepTime'] = end_time
        self.data['checkIn'] = start_time
        self.data['checkOut'] = end_time

    def get_data(self):
        """主页数据"""
        response = requests.get(self.url, headers=self.headers)
        data = response.content.decode()
        return data

    def post_data(self, url):
        """其它页数据"""
        response = requests.post(url=url, headers=self.headers, data=self.data)
        data = response.content.decode()
        try:
            data = json.loads(data)
            hotelPositionJSON = data['hotelPositionJSON']
            HotelMaiDianData = json.loads(data['HotelMaiDianData']['value']['htllist'])
            amount_dict = {}
            for amount in HotelMaiDianData:
                amount_dict[amount['hotelid']] = amount['amount']
            for hotel in hotelPositionJSON:
                hotel['url'] = 'http://hotels.ctrip.com' + hotel['url']
                hotel['img'] = 'http:' + hotel['img']
                hotel['amount'] = amount_dict[hotel['id']]
		# 获取主页的酒店详情的图片
                hotel_id = hotel['id']
                results = self.get_img_data('http://hotels.ctrip.com/pic/{0}.html'.format(hotel_id))
                hotel['detail_imgs'] = results
                yield hotel
        except Exception:
            print('第{0}页获取失败'.format(self.data['page']))

    def parse_data(self, data):
        """处理主页数据"""
        results = re.findall(r'hotelPositionJSON:.*?(.*?)\]', data, re.S)[0]
        htllist = re.findall(r'htllist: \'(.*?)\'', data, re.S)[0]
        results = json.loads(results + ']')
        htllist = json.loads(htllist)
        i = 0
        for hotel in results:
            hotel['url'] = 'http://hotels.ctrip.com' + hotel['url']
            hotel['img'] = 'http:' + hotel['img']
            hotel['amount'] = htllist[i]['amount']
            i += 1
	    # 获取其它页的酒店详情的图片
            hotel_id = hotel['id']
            results = self.get_img_data('http://hotels.ctrip.com/pic/{0}.html'.format(hotel_id))
            hotel['detail_imgs'] = results
            yield hotel

    def get_img_data(self, url):
        response = requests.get(url=url, headers=self.headers)
        results = self.parse_img_data(response.content.decode())
        print(url, '图片获取成功')
        return results

    def parse_img_data(self, data):
        results = re.findall(r'album:.*?(.*?)}],', data, re.S)[0]
        results = (results + '}]').replace('"', '\\"').replace('\'', '\"').replace('max', '"max"').replace('min',
                                                                                                           '"min"') \
            .replace('title', '"title"').replace('info', '"info"').replace('source', '"source"').replace('index',
                                                                                                         '"index"') \
            .replace('pid:', '"pid":')
        results = json.loads(results)
        hotel_img = []
        for result in results:
            hotel_img.append('http:' + result['max'])
        return hotel_img

    def save_mongodb(self, result):
        """保存到mongodb"""
        try:
            if db[MONGO_TABLE[self.city]].insert(result):
                print('第{0}页内容存储数据成功'.format(self.data['page']))
        except Exception:
            print('第{0}页内容存储数据出错'.format(self.data['page']), result)

    def run(self, page):
        """执行函数"""
        if int(page) == 2:
            data = self.get_data()
            hotel_list = self.parse_data(data)
            self.save_mongodb(hotel_list)
        self.data['page'] = page
        p_data = self.post_data('http://hotels.ctrip.com/Domestic/Tool/AjaxHotelList.aspx')
        self.save_mongodb(p_data)


if __name__ == '__main__':
    city = input('请输入目的地：')
    start_time = input('请输入住店时间(格式：xxxx-xx-xx, 当日请回车):')
    end_time = input('请输入离店时间(格式：xxxx-xx-xx, 当日请回车)：')
    # 创建实例
    xiecheng = XieCheng(start_time, end_time, city)
    # 创建进程池
    pool = Pool()
    pages = [x for x in range(2, 10)]
    pool.map(xiecheng.run, pages)
