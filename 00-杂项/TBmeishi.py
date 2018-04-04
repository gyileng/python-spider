import json
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from config import *
import pymongo

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)

# 请求第一页
def search():
    try:
        browser.get('https://www.taobao.com')
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))
        )
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
        input.send_keys('平安果')
        submit.click()
        totle = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')))
        get_products()
        return totle.text
    except TimeoutException:
        return search()


def next_page(page_number):
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
        )
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page_number)))
        get_products()
    except TimeoutException:
        next_page(page_number)


# 分析网页信息
def get_products():
   wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
   html = browser.page_source
   doc = pq(html)
   items = doc('#mainsrp-itemlist .items .item').items()
   for item in items:
       product = {
           'price':item.find('.price').text(),
           'deal':item.find('.deal-cnt').text()[:-3],
           'title':item.find('.title').text(),
           'shop':item.find('.shop').text(),
           'location':item.find('.location').text()
       }
       # print(product)
       # save_mongodb(product)
       save_file(product)


def save_mongodb(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('存储数据成功')
    except Exception:
        print('存储数据出错', result)


def save_file(result):
    try:
        if result:
            with open('./TaoBao.json', 'a', encoding='utf-8') as f:
                f.write(json.dumps(result, ensure_ascii=False) + '\n')
                print('保存到文件成功')
    except Exception:
        print('保存到文件失败')

# 启动
def main():
    totle = search()
    totle = int(re.compile('(\d+)').search(totle).group(1))
    # print(totle)
    for i in range(2, totle - 50):
        # print(i)
        next_page(i)
    browser.close()


if __name__ == '__main__':
    main()