
from src.task_core.web3_wrap import Web3Wrap
from src.utils.block_chain import Block_chain
from src.utils.log import worker_log

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





def pring_msg(w, a1):
    print(a1)
    log_msg = f"[{batch_name}][{num}][{instanceId}]  {a1} "

    worker_log.msg_info(log_msg, instanceId)

w = Web3Wrap.get_instance(block_chain=Block_chain.Sepolia, proxy_ip=proxy_ip_str, gas_flag=False)

rsp =pring_msg(w, a1)