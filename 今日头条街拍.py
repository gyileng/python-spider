import json, time
from hashlib import md5
from multiprocessing import Pool
import os
import pymongo
from bs4 import BeautifulSoup
import requests, re
from urllib.parse import urlencode
from requests.exceptions import RequestException
from config import *
from json.decoder import JSONDecodeError
import gevent
# from gevent import monkey
# monkey.patch_all()

# 保存到MONGODB
# client = pymongo.MongoClient(MONGO_URL, connect=False)
# db = client[MONGO_DB]


def get_page_index(number, keyword):
    data = {
        'offset': number,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': '3',
        'from':'gallery'
    }

    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引页出错')
        return None


def parse_page_index(html):
    try:
        data = json.loads(html)
        if data and 'data' in data.keys():
            for item in data.get('data'):
                # print(item.get('article_url'))
                yield item.get('article_url')
    except JSONDecodeError:
        pass


def get_page_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引页出错', url)
        return None


def parse_page_detail(html, url):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.select('title')[0].get_text()
    print(title)
    images_pattent = re.compile('JSON.parse\("(.*?)"\),', re.S)
    result = re.search(images_pattent, html)
    if result:
        data = json.loads(result.group(1).replace('\\', ''))
        # data = json.loads(result.group(1))
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]
            for image in images:download_image(image)
            return {
                'title': title,
                'url': url,
                'images': images
            }

# 保存到MONGODB
# def save_to_mongo(result):
#     if db[MONGO_TABLE].insert(result):
#         print('存储数据库成功', result)
#         return True
#     return False


def download_image(url):
    print('正在下载', url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            save_image(response.content)
        return None
    except RequestException:
        print('请求图片出错', url)
        return None


def save_image(content):
    file_path = './today-news/' + md5(content).hexdigest() + '.jpg'
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)


def main(offset):
    html = get_page_index(offset, KEYWORD)
    for url in parse_page_index(html):
        html = get_page_detail(url)
        if html:
            result = parse_page_detail(html, url)
            # print(result)
            # if result:
            #     save_to_mongo(result)


if __name__ == '__main__':
    start_time = time.time()
    # 使用多进程加快获取速度
    groups = [x*20 for x in range(GROUP_START, GROUP_END + 1)]
    # main(groups)
    pool = Pool()
    pool.map(main, groups)
    #
    # # work = gevent.spawn(main, groups)
    # # gevent.joinall([work])
    end_time = time.time()
    print('总共用时%f' % (end_time - start_time))