import decimal
import json

from src.task_core.web3_wrap import Web3Wrap
from src.utils.block_chain import Block_chain


def process():
    w = Web3Wrap(block_chain=Block_chain.ZKS_ERA, gas_flag=False)

    #karatdao
    #url_get_price(w, contract_name = 'karatdao', contract_address='0x112E5059a4742ad8b2baF9C453fDA8695c200454')
    #
    url_get_price(w, contract_name='syncswap', contract_address='0x32400084c286cf3e17e7b677ea9583e60a000324')
    pass


def url_get_price(w:Web3Wrap, contract_name, contract_address, limit=10):
    url = f'https://zksync2-mainnet-explorer.zksync.io/transactions?limit='+str(limit)+'&direction=older&contractAddress='+contract_address
    rsp = json.loads(w.session.get(url).text)
    data = rsp['list']
    feeCounts = []
    for i in data:
        if i['status'] != "failed":
            eth_price = decimal.Decimal(i['erc20Transfers'][0]['tokenInfo']['usdPrice'])
            fee_value = decimal.Decimal(w.w3.from_wei(int(i['fee'], 16), 'ether'))
            feeCounts.append(fee_value)
    averageFee = sum(feeCounts) / len(feeCounts)
    final_result = (eth_price * averageFee).quantize(decimal.Decimal(".00000001"))
    print('contract_name[',contract_name,'] 最近20笔tx平均gas:', averageFee, eth_price, f'{final_result}/usdt')
    return final_result
    pass



if __name__ == '__main__':
    process()
    print('finish.....')
    pass