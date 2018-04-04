import requests, re
import json
import time
from multiprocessing import Pool


class Spider(object):
    def __init__(self):
        self.i = 1
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'}
        self.list = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]

    def start_spider(self, url):
        response = requests.get(url, headers=self.headers).text
        # print(response)
        results = re.findall(
            '<div class="board-item-main">.*?data-val="{movieId:.*?}">(.*?)</a>.*?<p class="star">(.*?)</p>.*?<p class="releasetime">(.*?)</p>',
            response, re.S)
        # print(results)
        # with open('./猫眼电影TOP100.txt', 'ab') as f:
        # for result in results:
        # name, star, releasetime = result
        # Name = name.strip()
        # Star = star.strip()
        # Releasetime = releasetime.strip()
        # data = ('%s.'% str(self.i) + Name + '\n          ' + Star + '\n             ' + Releasetime + '\r\n').encode()
        # # print('正在保存第%d页的内容' % i)
        # f.write(data)
        # self.i += 1
        for result in results:
            yield {
                'name': result[0],
                'star': result[1].strip()[3:],
                'time': result[2].strip()[5:]
            }

    def write(self, item):
        with open('./猫眼电影TOP100.txt', 'a', encoding='utf-8') as f:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
            f.close()

    def start(self, i):
        # start_time = time.time()
        # for i in self.list:
        first_url = 'http://maoyan.com/board/4?offset='
        url = first_url + str(i)
        items = self.start_spider(url)
        for item in items:
            print(item)
            self.write(item)
        # print('开始保存第%d页的内容' % (i // 10 + 1))
    # end_time = time.time()
    # print('全部保存完毕,总共用时%f' % (end_time - start_time))


if __name__ == '__main__':
    start_time = time.time()
    maoyan = Spider()
    for i in range(10):
        maoyan.start(i*10)
    # pool = Pool()
    # noinspection PyArgumentList
    # pool.map(maoyan.start, [i*10 for i in range(10)])
    end_time = time.time()
    print('全部保存完毕,总共用时%f' % (end_time - start_time))
