from enum import Enum

#from src.dao.proxy_dao import proxyDao
from src.utils.date_utils import DateUtils


class Proxy_type(Enum):
    LOCAL_PROXY = ('local_proxy')
    STATIC_PROXY = ('static_proxy')
    DYNC_PROXY = ('dync_proxy')

class ProxyService:

    def create_proxy(self,ip, port,user_name='', user_pwd='', proxy_type = Proxy_type.LOCAL_PROXY.value):
        ts = DateUtils.get_timestamp()
        records = []

        records.append((ip, port, user_name, user_pwd, proxy_type, 1, '', ts))
        #proxyDao.insert_batch(records)

    def query_by_type(self, proxy_type):
        #rs = proxyDao.select_by_type(proxy_type)
        rs =[]
        lst = []
        for line in rs:
            if proxy_type == Proxy_type.LOCAL_PROXY.value:
                lst.append(line['ip'] + ':' + line['port'])
            if proxy_type == Proxy_type.STATIC_PROXY.value:
                proxy_str = 'http://{0}:{1}@{2}:{3}'.format(line['user_name'],
                                                            line['user_pwd'],
                                                            line['ip'],
                                                            line['port'])
                lst.append(proxy_str)

        return lst

proxyService = ProxyService()


if __name__ == '__main__':
    p = ProxyService()
    #p.create_proxy('192.0.0.7','8889', 'yyl','yyl_pwd', Proxy_type.STATIC_PROXY.value)

    #p.query_by_type(Proxy_type.STATIC_PROXY.value)
    print(Proxy_type.LOCAL_PROXY.value)

    print('finish.....')