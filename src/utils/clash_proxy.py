import json
import urllib

import requests

from src.utils.Properties import pro


class ClashProxy:

    def __init__(self):
        self.secret = pro.get('secret')
        self.clash_url = pro.get('external_controller')
        self.headers = {
            'Authorization': 'Bearer ' + self.secret,
        }


    def get_all_node(self):
        print('clash_url:  ', self.clash_url)
        url = 'http://' + self.clash_url +'/proxies'

        rsp = requests.request('get', url = url, headers = self.headers)
        data = rsp.json()['proxies']['GLOBAL']['all']
        nodeNames = []
        for node in data:
            if (node=='DIRECT'
                    or node=='REJECT'
                    or '直连' in node
                    or 'IPV60' in node
                    or 'Proxy' in node
                    or 'Domestic' in node
                    or 'AsianTV' in node
                    or 'GlobalTV' in node
                    or 'Others' in node
                    or '官网' in node):
                continue
            nodeNames.append(node)
        return nodeNames



    def test_delay(self, node):
        try:
            encode_Str = urllib.request.quote(node, safe='/:?=&', encoding='utf-8')
            url = 'http://' + self.clash_url + '/proxies/' + encode_Str + '/delay?timeout=5000&url=http%3A%2F%2Fwww.gstatic.com%2Fgenerate_204'
            rsp = requests.request('get', url=url, headers=self.headers)
            print('node:', node, 'rsp:', rsp, rsp.text)
            return rsp.json()['delay']
        except Exception:
            return -1




    def change_node(self, node):
        try:
            url = 'http://' + self.clash_url + '/proxies/GLOBAL'
            payload = {
                "name": node
            }

            rsp = requests.request('put', url=url, headers=self.headers, data=json.dumps(payload))
            print('rsp:', rsp.status_code, rsp.text)
            return 0
        except Exception:
            return -1


if __name__ == '__main__':
    clash = ClashProxy()
    clash.get_all_node()
