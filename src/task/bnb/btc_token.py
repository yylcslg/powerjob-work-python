import json

from src.task_core.web3_wrap import Web3Wrap
from src.utils.block_chain import Block_chain
from src.utils.log import worker_log


try:
    param_map = param_dict
except NameError as e:
    var_exists = False
    print('NameError:', e)
else:
    a1 = param_map['account_1']
    num = param_map['exe_num']
    instanceId = param_map['instance_id']
    proxy_ip_str = param_map['proxy_ip']
    batch_name = param_map['batch_name']




user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'



def btc_faucet(w):
    address = 'tb1pkazmlpyfaeuu78chfyn8t5073healy2vgh9dyapev9ruc9khumxqcdv2sq'

    url = 'https://api.thefaucet.org/v3/is_not_login_basic_claimable?coin_config_id=1&user_address=' + address

    rsp = w.session.request(method='get', url=url)


    log_msg = f"[{batch_name}][{num}][{instanceId}]  {address} : status code: {rsp.status_code} content: {rsp.json()}"
    worker_log.msg_info(log_msg, instanceId)

    pass


def claim_btc_test(w):
    address = 'tb1pu5y4t5lsuadry3gk559h63xzr50dy0jwafp3r3j325h57f3tcx0sjrp3yf'
    url = 'https://api.thefaucet.org/v3/claim_basic_not_login'

    payload = {
        "coin_id": 1,
        "address": address
    }
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'User-Agent': user_agent
    }

    rsp = w.session.request(method='post', url=url,headers=headers,  data=json.dumps(payload))

    log_msg = f"[{batch_name}][{num}][{instanceId}]  {address} : status code: {rsp.status_code} content: {rsp.json()}"
    worker_log.msg_info(log_msg, instanceId)


w = Web3Wrap.get_instance(block_chain=Block_chain.Sepolia, proxy_ip=proxy_ip_str, gas_flag=False)
claim_btc_test(w)