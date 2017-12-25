import timefrom selenium import webdriverfrom selenium.common.exceptions import TimeoutExceptionfrom selenium.webdriver.support.wait import WebDriverWaitfrom selenium.webdriver.support import expected_conditions as ECfrom selenium.webdriver.common.by import Byimport re, requestsfrom requests.exceptions import RequestExceptionfrom hashlib import md5from multiprocessing import Pool# 定义一个谷歌浏览器，这里可以使用PhantomJSbrowser = webdriver.Chrome()wait = WebDriverWait(browser, 10)# 获取第一个页面的htmldef chrome():    browser.get('https://mm.taobao.com/search_tstar_model.htm?spm=5679.126488.640745.2.535e14b2dpvd56&style=%E7%94%9C%E7%BE%8E&place=city%3A')    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_GirlsList')))    html = browser.page_source    # print(html)    return html# 分析htmldef parse_html(html):    results = re.findall('<li class="item">.*?<a href="(.*?)"', html, re.S)    # print(results)    for result in results:        # print(result)        url = 'https:' + result        yield url# 获取淘宝女孩的主页的htmldef get_taogirls(url):    try:        html = requests.get(url)        if html.status_code == 200:            html = html.text            parse_index(html)        return None    except TimeoutException:        return get_taogirls(url)# 分析淘宝女孩的html,正则匹配图片链接def parse_index(html):    # print(html)    image_lines = re.findall('<img style="float.*?src="(.*?)"', html, re.S)    for image_line in image_lines:        image_line = 'https:' + image_line        # print(image_line)        down_img(image_line)# 下载图片def down_img(image_line):    print('正在下载', image_line)    try:        data = requests.get(image_line)        if data.status_code == 200:            save_img(data.content)    except RequestException:        print('保存到文件失败', image_line)        return None# 保存图片def save_img(content):    try:        file_path = './Taogirls/' + md5(content).hexdigest() + '.jpg'        with open(file_path, 'wb') as f:            f.write(content)    except Exception:        return None# 模拟点击下一页def next_page():    click = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.lady-girls-wrap.tb_mm_main > div.mm_paginator > div > span.page-next.page-next-disabled')))    click.click()    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_GirlsList')))    html = browser.page_source    for url in parse_html(html):        get_taogirls(url)    time.sleep(0.5)    next_page() #灰调函数def main():    html = chrome()    urls = parse_html(html)    for url in urls:        get_taogirls(url)    '''    这里可以使用多进程    groups = [url for url in urls]    pool = Pool()    pool.map(get_taogirls, groups)    '''    time.sleep(0.5)    next_page()if __name__ == '__main__':    main()