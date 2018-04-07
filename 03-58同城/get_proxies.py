import requests

def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").content

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


if __name__ == '__main__':

    def getHtml():
        # ....
        retry_count = 5
        proxy = get_proxy()
        while retry_count > 0:
            try:
                html = requests.get('https://www.example.com', proxies={"http": "http://{}".format(proxy)})
                # 使用代理访问
                return html
            except Exception:
                retry_count -= 1
        # 出错5次, 删除代理池中代理
        delete_proxy(proxy)
        return None