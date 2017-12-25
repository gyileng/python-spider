import json
import re, time

import pymongo
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from config import *

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)

# 获取第一个页面html
def get_one_page():
    try:
        browser.get('https://www.douyu.com/directory/all')
        totle = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, '#J-pager > a:nth-child(11)')))
        get_products()
        return totle.text
    except TimeoutException:
        return get_one_page()


def next_page(page_number):
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#J-pager > input'))
        )
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J-pager > a.shark-pager-submit')))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, '#J-pager > a.shark-pager-item.current'), str(page_number)))
        get_products()
    except TimeoutException:
        next_page(page_number)


# 分析页面
def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#live-list-content')))
    html = browser.page_source
    # print(html)
    results = re.findall('data-original="(.*?)".*?<div class="mes">.*?<h3 class="ellipsis">(.*?)</h3>.*?<span class="tag ellipsis">(.*?)</span>.*?<span class="dy-name ellipsis fl">(.*?)</span>.*?<span class="dy-num fr">(.*?)</span>', html, re.S)
    for result in results:
        product = {
            'room':result[1].strip(),
            'category':result[2].strip(),
            'name':result[3].strip(),
            'number':result[4].strip(),
            'img_line':result[0].strip()
        }
        save_file(product)
        save_mongo(product)


def save_file(result):
    try:
        if result:
            with open('./DouYu.json', 'a', encoding='utf-8') as f:
                f.write(json.dumps(result, ensure_ascii=False) + '\n')
    except Exception:
        print('保存到文件失败')


def save_mongo(result):
    try:
        db[MONGO_TABLE].insert(result)
    except Exception:
        print('存储数据出错', result)


def main():
    totle = get_one_page()
    totle = int(re.compile('(\d+)').search(totle).group(1))
    # print(totle)
    for i in range(2, totle + 1):
        next_page(i)
        print('第%d页保存成功' % i)
        print('存储数据成功')
        time.sleep(1)


if __name__ == '__main__':
    main()