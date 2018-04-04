import os
import requests, re
from hashlib import md5
import time
from multiprocessing import Pool

# 获取第一个网页
from requests import RequestException

# 获取第一个页面html
def get_one_page():
    try:
        url = 'https://www.douyu.com/directory/all'
        html = requests.get(url)
        if html.status_code == 200:
            return html.text
        return None
    except RequestException:
        print('请求主页出错')
        return None
    # print(html)


# 分析第一个页面
def parse_one_page(html):
    image_lines = re.findall('data-original="(.*?)"', html, re.S)
    # sum_page = re.findall('<a href="#" class="shark-pager-item">(.*?)</a>', html, re.S)
    # print(html)
    # print(sum_page)
    for image_line in image_lines:
        down_image(image_line)

# 获取下一个页面
def next_page(number):
    try:
        url = 'https://www.douyu.com/gapi/rkc/directory/0_0/' + str(number)
        html = requests.get(url)
        if html.status_code == 200:
            html = html.text
            lines = re.findall('"rs16":"(.*?)"', html)
            sum_page = re.findall('"pgcnt":(\d+)', html)
            for line in lines:
                down_image(line)
            return sum_page
        return None
    except RequestException:
        print('请求主页出错')
        return None

# 下载图片
def down_image(image_line):
    print('正在下载', image_line)
    try:
        # print('正在保存第%d图片' % a)
        image_info = requests.get(image_line).content
        filepath = './DouYuIMG1/' + md5(image_info).hexdigest() + '.jpg'
        if not os.path.exists(filepath):
            with open(filepath, 'ab') as f:
                f.write(image_info)
    except Exception:
        print('保存图片出错')


def main():
    # next_page(number)

    start_time = time.time()
    html = get_one_page()
    parse_one_page(html)
    # groups = [x for x in range(3, int(next_page(2)[1][0]) + 1)]
    for number in range(2, 4):
        next_page(number)
    end_time = time.time()

    print('总共用时%f' % (end_time - start_time))


if __name__ == '__main__':
    # start_time = time.time()
    # html = get_one_page()
    # parse_one_page(html)
    # # groups = [x for x in range(3, int(next_page(2)[1][0]) + 1)]
    # groups = [x for x in range(2, 4)]
    # # main(groups)
    # pool = Pool()
    # pool.map(main, groups)
    # end_time = time.time()
    #
    # print('总共用时%f' % (end_time - start_time))

    main()