
from src.task_core.web3_wrap import Web3Wrap
from src.utils.block_chain import Block_chain
from src.utils.log import worker_log

try:
    param_map = param_dict
except NameError as e:
    var_exists = False
    print('NameError:', e)
else:
    exe_num = param_map['exe_num']
    instanceId = param_map['instance_id']
    a1 = param_map['account_1']
    proxy_ip_str = param_map['proxy_ip']
    batch_name = param_map['batch_name']



def claim_daily_reward(w, a1):
    contract_address = '0xa18f6FCB2Fd4884436d10610E69DB7BFa1bFe8C7'
    gas_gwei = w.w3.from_wei(300000, 'gwei')

    # 42.54
    data = '0xb88a802f'

    tx_param = w.build_tx_param(a1, contract_address, gas_gwei=gas_gwei, gas_price_gwei=0, data=data)
    (tx_id, rsp, balance) = w.tx_by_param(a1, tx_param)
    log_msg = f"[{batch_name}][{exe_num}][{instanceId}]  {a1.address} : status code: {rsp['status']} "
    worker_log.msg_info(log_msg, instanceId)


def claim_buffer(w, a1):
    if(a1.address == '0x1Ee62353F811fB4C78F05fF7f3bF09BE4DaEa6c8' or a1.address == '0x3141CcBCC38FeCB363d52f3a03EEC86cCDBe34eB'):
        contract_address = '0xa18f6FCB2Fd4884436d10610E69DB7BFa1bFe8C7'
        gas_gwei = w.w3.from_wei(300000, 'gwei')

        # 42.54
        data = '0x354d970a'

        tx_param = w.build_tx_param(a1, contract_address, gas_gwei=gas_gwei, gas_price_gwei=0, data=data)
        (tx_id, rsp, balance) = w.tx_by_param(a1, tx_param)
        log_msg = f"[{batch_name}][{exe_num}][{instanceId}]  {a1.address} : status code: {rsp['status']}"
        worker_log.msg_info(log_msg, instanceId)

w = Web3Wrap.get_instance(block_chain=Block_chain.Humanity, proxy_ip=proxy_ip_str, gas_flag=False)

claim_daily_reward(w, a1)
claim_buffer(w, a1)