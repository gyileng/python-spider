import requests
import json
import re
import time
import execjs
from lxml import etree
from commons import cityList
import os


# from get_proxies import get_proxy,delete_proxy
from ProxyGetter.getFreeProxy import GetFreeProxy
from queue import Queue

class Spider58(object):
    """
    目标：
    58同城各城市出租信息
    
    功能：
    获取所有城市对应url
    获取信息
    实现换页
    
    反爬手段：
    请求频繁后会有拖动条验证码----待解决(尝试通过切换ip避免验证码出现)
    换页时需要取得请求参数PGTID，ClickID
    请求头需要封装referer
    需切换代理
    
    """

    def __init__(self):
        self.url = "http://www.58.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
        }

        # self.proxies = {
        #     "http": "http://115.223.249.231"
        # }
        #
        # self.session = requests.session()
        # # ,proxies=self.proxies
        # self.session.get(self.url, headers=self.headers)

        self.ClickID = 1


    def connect_html(self,url=None,headers=None,params=None):
        """通过代理获取"""

        # 使用数据库的方法
        # resp = None
        # while not resp:
        #     self.retry_count = 5
        #     self.proxy = get_proxy()
        #     print(self.proxy)
        #     self.proxies = {
        #         "http": "http://{}".format(self.proxy)
        #     }
        #     while self.retry_count > 0:
        #         try:
        #             self.session = requests.session()
        #             # 使用代理访问
        #             if url is None:
        #                 resp = self.session.get(self.url, headers=self.headers,proxies=self.proxies,timeout=2)
        #             else:
        #                 resp = self.session.get(url, headers=headers, params=params,proxies=self.proxies, timeout=2)
        #             if resp:
        #                 print("获取代理")
        #                 print(proxy)
        #                 self.count = 1
        #                 break
        #         except Exception:
        #             self.retry_count -= 1
        #     # 出错5次, 删除代理池中代理
        #     delete_proxy(self.proxy)


        # 不使用数据库的方法
        # 先获取500个ip放到队列中
        proxy_queue = Queue()
        proxies = GetFreeProxy()
        for proxy in proxies.freeProxyWallSecond():
            proxy_queue.put(proxy)

        resp = None
        while not resp:
            # 设定请求次数
            retry_count = 5
            # 从队列中获取一个ip
            proxy = proxy_queue.get()

            self.proxies = {
                "http": "http://{}".format(proxy)
            }
            while retry_count > 0:
                try:
                    self.session = requests.session()
                    # 使用代理访问
                    if url is None:
                        resp = self.session.get(self.url, headers=self.headers,proxies=self.proxies,timeout=2)
                    else:
                        resp = self.session.get(url, headers=headers,params=params,proxies=self.proxies, timeout=2)
                    if resp:
                        print("获取代理")
                        print(proxy)
                        self.count = 1
                        break
                except Exception:
                    retry_count -= 1


    def get_url(self):
        """获取所有城市url"""
        # cities_url = self.url + "/changecity.html"
        # resp = self.session.get(cities_url,headers=self.headers,proxise=self.proxies)
        # http://hf.58.com/chuzu/

        url_dict = {}
        for province,cities in  cityList.items():
            # url_list = []
            url_dict[province] = {}
            for city,city_code in cities.items():
                city_code = city_code.split("|")[0]
                url = "http://"+city_code+".58.com/"+"chuzu/"
                # url_list.append(url)
                url_dict[province][city] = url
        return url_dict


    def get_PGTID(self,_trackURL):

        # 通过上一个html获取页面JS中的_trackURL
        with open("my_params.js", "rb") as f:
            js_data = f.read().decode()

        pagetype = _trackURL["pagetype"]
        cate = _trackURL["cate"]
        area = _trackURL["area"]

        PGTID = execjs.compile(js_data).call("getGTID",pagetype,cate,area)
        # print(PGTID)

        # ClickID初始值是1
        # 每获取一次PGTID就+1
        self.ClickID += 1

        return PGTID


    def get_page_data(self,url,headers,params):
        """获取每页数据"""

        # 判断请求次数超过100，更换代理
        if self.count>100:
            print("重新获取代理")
            self.connect_html(url,headers,params)

        if params is None:
            # 每个城市的首页
            resp = self.session.get(url, headers=self.headers,proxies=self.proxies)
            self.count += 1

        else:
            # 换页
            resp = self.session.get(url,headers=headers,params=params,proxies=self.proxies)
            self.count += 1

        content_url = resp.url

        return resp.content, content_url


    def parse_data(self,data):
        """分析各种类型数据"""

        html = etree.HTML(data.decode())
        node_list = html.xpath('//ul[@class="listUl"]/li[not(@class="apartments-pkg apartments" or @id="bottom_ad_li")]')
        data_list = []

        # 信息去重
        url_set = set()
        for node in node_list:
            house_url = node.xpath('./div[@class="des"]/h2/a/@href')[0]
            if house_url not in url_set:
                temp = {}
                temp["title"] = node.xpath('./div[@class="des"]/h2/a/text()')[0].strip()
                temp["url"] = node.xpath('./div[@class="des"]/h2/a/@href')[0]
                # 数字问题
                temp["size"] = node.xpath('./div[@class="des"]/p/text()')[0].strip()
                temp["address"] = node.xpath('./div[@class="des"]/p/a/text()')
                # temp["owner"] = node.xpath('./div[@class="des"]/div/text()')
                temp["money"] = node.xpath('./div[@class="listliright"]/div[@class="money"]/b/text()')
                # print(node.xpath('./div[@class="des"]/h2/a/text()')[0])
                data_list.append(temp)
                url_set.add(house_url)
        print(data_list)
        # 获取下一页url
        page_url = html.xpath('//*[@id="bottom_ad_li"]/div[2]/a[@class="next"]/@href')
        if page_url:
            page_url = page_url[0]
        else:
            page_url = None

        # 获取参数_trackURL
        # var _trackURL = "(.*?)";
        _trackURL = re.findall('var _trackURL = "(.*?)";.*?</script>',data.decode(),re.S)[0].replace("false","False").replace("true","True")
        # _trackURL = json.loads(_trackURL.encode())

        _trackURL = eval(_trackURL)
        return data_list,page_url,_trackURL


    def save_data(self,data_list,province,city):
        """保存数据"""
        if not os.path.exists("58City"):
            os.mkdir("58City")
        if not os.path.exists("58City/{}".format(province)):
            os.mkdir("58City/{}".format(province))
        if not os.path.exists("58City/{}/{}".format(province,city)):
            os.mkdir("58City/{}/{}".format(province,city))
        os.chdir("58City/{}/{}".format(province,city))

        with open("{}.json".format(self.i), "wb") as f:
            for data in data_list:
                data_json = json.dumps(data,ensure_ascii=False) + ",\n"
                f.write(data_json.encode())
        self.i += 1
        os.chdir("../../..")


    def run(self):
        """主程序，实现换城市换页逻辑"""

        # self.get_url()
        url_list = self.get_url()
        self.connect_html()

        for province,city_list in url_list.items():
            print(province+"----->")
            for city,url in city_list.items():
                print(city+"----->")
                # 每当进入新城市首页，初始化参数
                self.i = 1
                self.ClickID = 1
                page_url = url
                headers = self.headers
                params = None
                while page_url:
                    data,content_url = self.get_page_data(page_url,headers,params)

                    data_list,page_url,_trackURL = self.parse_data(data)
                    PGTID = self.get_PGTID(_trackURL)
                    # 封装请求参数
                    params = {
                        "PGTID":PGTID,
                        "ClickID":self.ClickID
                    }
                    # 封装请求头
                    headers = {
                        "Referer":content_url,
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
                    }
                    # 防止请求过快
                    # time.sleep(2)
                    self.save_data(data_list,province,city)


if __name__ == '__main__':
    s = Spider58()
    s.run()

