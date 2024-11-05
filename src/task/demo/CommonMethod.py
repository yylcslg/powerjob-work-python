import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

def create_session(proxy: str) -> requests.Session:
    session = requests.Session()
    session.proxies = {"http": proxy, "https": proxy}
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


