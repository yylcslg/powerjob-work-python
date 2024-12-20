import json
import random
import urllib
import yaml


import requests

class ClashProxy:

    def __init__(self):
        self.read_clash_yaml()
        self.headers = {
            'Authorization': 'Bearer ' + self.secret,
        }

    def read_clash_yaml(self):
        file_path = '/home/yinyunlong/.config/clash/config.yaml'
        with open(file_path, encoding='utf-8') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            self.clash_url = data['external-controller']
            self.secret = data['secret']



    def get_all_node(self):
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


        node_len = len(nodeNames)
        if(node_len == 0):
            return nodeNames

        ##特殊处理，第一个节点放最后，最后的节点放最前， 防止clash 节点调整后不能调整回来
        temp = nodeNames[0]

        nodeNames[0] = nodeNames[node_len -1]
        nodeNames[node_len - 1] = temp


        return nodeNames



    def test_delay(self, node):
        try:
            encode_Str = urllib.request.quote(node, safe='/:?=&', encoding='utf-8')
            url = 'http://' + self.clash_url + '/proxies/' + encode_Str + '/delay?timeout=5000&url=http%3A%2F%2Fwww.gstatic.com%2Fgenerate_204'
            rsp = requests.request('get', url=url, headers=self.headers)
            return rsp.json()['delay']
        except Exception:
            return -1




    def change_node(self, node):
        try:
            url = 'http://' + self.clash_url + '/proxies/GLOBAL'
            payload = {
                "name": node
            }
            requests.request('put', url=url, headers=self.headers, data=json.dumps(payload))
            return 0
        except Exception:
            return -1


    def random_change_node(self):
        try:
            nodeNames = self.get_all_node()
            num = random.randint(0, len(nodeNames)-1)
            self.change_node(nodeNames[num])
        except Exception:
            return -1


    def get_config(self):
        try:
            url = 'http://' + self.clash_url + '/configs'

            rsp = requests.request('get', url=url, headers=self.headers)
            print('rsp:' , rsp.status_code, rsp.text)
            return 0
        except Exception as e:
            print(e)
            return -1

if __name__ == '__main__':
    clash = ClashProxy()
    nodeNames = clash.get_all_node()
    print(nodeNames)


