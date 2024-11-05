import socket

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

class HttpTools:
    @staticmethod
    def build_proxy(proxy:str):
        return {"http": proxy, "https": proxy}


    @staticmethod
    def create_session(proxy: str) -> requests.Session:
        session = requests.Session()
        if proxy != '':
            session.proxies = HttpTools.build_proxy(proxy)
        try:
            resp = session.get('http://ip-api.com/json/', timeout=10)
            data = resp.json()
            ip = data['query']
            country = data['country']
            city = data['city']
            print('代理ip：{0}，地区：{1}-{2}'.format(ip,country,city))
        except:
            return None

        retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        session.mount("http://", HTTPAdapter(max_retries=retries))
        session.mount("https://", HTTPAdapter(max_retries=retries))
        return session

    @staticmethod
    def get_host_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()

        return ip


