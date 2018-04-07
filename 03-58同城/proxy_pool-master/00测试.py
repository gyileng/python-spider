from Manager.ProxyManager import ProxyManager

def get():
    proxy = ProxyManager().get()
    return proxy if proxy else 'no proxy!'



if __name__ == '__main__':
    ip = get()
    print(ip)