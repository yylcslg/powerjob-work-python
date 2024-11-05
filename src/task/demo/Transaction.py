from numpy import median
from web3.gas_strategies.time_based import medium_gas_price_strategy

import CommonMethod
from web3 import Web3, middleware

from src.utils.block_chain import Block_chain


def tran_tx(web3:Web3):
    private_key = ''
    from_address = web3.toChecksumAddress('')

    # private_key = ''
    target_address = web3.toChecksumAddress('')

    from_address = Web3.toChecksumAddress(from_address)
    target_address = Web3.toChecksumAddress(target_address)
    nonce = web3.eth.getTransactionCount(from_address)  # 获取 nonce 值

    amount=0.1
    gas_limit=21000
    gas_price = 1.6
    params = {
        'from': from_address,
        'nonce': nonce,
        'to': target_address,
        'value': web3.toWei(amount, 'ether'),
        'gas': gas_limit,
        # 'gasPrice': w3.toWei(gas_price, 'gwei'),
        'maxFeePerGas': web3.toWei(gas_price, 'gwei'),
        'maxPriorityFeePerGas': web3.toWei(gas_price, 'gwei'),
        'chainId': 59140,

    }

    signed_tx = web3.eth.account.sign_transaction(params, private_key=private_key)
    # 交易发送并获取交易hash
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction).hex()

    print(tx_hash)


def _estimate_gas(transactions) -> int:
    # Returns the median of the gas in previous block transactions
    return int(median(t.gas for t in transactions))






def latest_middle_gas(w3:Web3):
    w3.eth.set_gas_price_strategy(medium_gas_price_strategy)

    w3.middleware_onion.add(middleware.time_based_cache_middleware)
    w3.middleware_onion.add(middleware.latest_block_based_cache_middleware)
    w3.middleware_onion.add(middleware.simple_cache_middleware)

    gas = w3.eth.generateGasPrice().real
    print('gas:',gas)



if __name__ == '__main__':
    s = CommonMethod.create_session("http://127.0.0.1:8889")

    Block_chain.ETH
    web3 = Web3(Web3.HTTPProvider(Block_chain.ETH.url, session=s))
    latest_middle_gas(web3)
    print('finish')