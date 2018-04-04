import json, time
from config import *
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from multiprocessing import Pool
from urllib import urlencode


def get_page_index(type_num, number):
    data = {
        'type': type_num,
        'interval_id': '100:90',
        'action':'',
        'start': number,
        'limit': '20'
    }
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'}

    # headers = {'User - Agent': 'Mozilla / 5.0(WindowsNT10.0;Win64;Gecko) Chrome / 52.0.2743.116Safari / 537.36Edge / 15.15063'}
    url = 'https://movie.douban.com/j/chart/top_list?type=' + str(type_num) + '&interval_id=100%3A90&action=&start='+str(number)+'&limit=20'
    # print(url)
    try:
        response = requests.get(url, headers = headers)
        # print(response.status_code)
        if response.status_code == 200:
            return response.text
    except RequestException:
        print('请求出错')
        return None

def parse_page_index(html):
        data = json.loads(html.replace('\\', ''))
        for item in data:
            # print(item)
            yield {
                'rating':item['rating'],
                'rank':item['rank'],
                'types':item['types'],
                'regions':item['regions'],
                'title':item['title'],
                'url':item['url'],
                'release_date':item['release_date'],
                'actors':item['actors']
            }

def down_info(result):
    with open('./豆瓣电影排行榜-喜剧' + '.json', 'a', encoding='utf-8') as f:
        result = json.dumps(dict(result),ensure_ascii=False) + '\n'
        f.write(result)



def main(type_num):
    html = get_page_index(KEYWORD1, type_num)
    if html:
        results = parse_page_index(html)
        for result in results:
            # print(result)
            down_info(result)


if __name__ == '__main__':
    start_time = time.time()
    # groups = [x*20 for x in range(GROUP_START1, GROUP_END1 + 1)]
    for x in range(GROUP_START1, GROUP_END1 + 1):
        main(x*20)
    end_time = time.time()
    print('总用时%f' % (end_time - start_time))
    # pool = Pool()
    # pool.map(main, groups)
    # print('正在保存')
    # main(0)