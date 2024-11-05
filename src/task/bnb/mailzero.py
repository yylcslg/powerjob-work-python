
from src.task_core.web3_wrap import Web3Wrap
from src.utils.block_chain import Block_chain
from src.utils.log import log

try:
    param_map = param_dict
except NameError as e:
    var_exists = False
    print('NameError:', e)
else:
    num = param_map['exe_num']
    instanceId = param_map['instance_id']
    a1 = param_map['account_1']
    proxy_ip_str = param_map['proxy_ip']
    batch_name = param_map['batch_name']




def queryDailyInfo(w, address):
    url_2 = 'https://api2.mailzero.network/queryDailyInfo?address=' + address
    rsp = w.session.request(method='get', url=url_2)
    print('[queryDailyInfo] status code:', rsp.status_code, ' content:', rsp.content)


def checkin(w, address):
    url ='https://api2.mailzero.network/checkin?address='+address
    rsp = w.session.request(method='get', url=url)

    log_msg = f"[{batch_name}][{num}][checkin][{instanceId}]  {address} : status code: {rsp.status_code} content: {rsp.json()}"
    log.info(log_msg, instanceId)

    return rsp.json()


w = Web3Wrap.get_instance(block_chain=Block_chain.Sepolia, proxy_ip=proxy_ip_str, gas_flag=False)

rsp =checkin(w, a1.address)






