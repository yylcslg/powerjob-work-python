from src.task_core.web3_wrap import Web3Wrap
from src.utils.block_chain import Block_chain
from src.utils.wallet_account import Wallet


def process():
    w = Web3Wrap(block_chain=Block_chain.LINEA_TEST, gas_flag=False)
    wallet = Wallet()
    build_tx(w, wallet)

#不使用 abi 方式调用 合约方法
#https://explorer.goerli.linea.build/tx/0x872abb0460f3100856d6d845d9c36ee0f9545ec9d39dd890c683e3196d42cc03
def build_tx(w:Web3Wrap, wallet:Wallet):
    accounts = wallet.read_test_wallet()
    main_account = accounts[0]  # eth 收集到这个账户
    contract_address = '0x6F03052743CD99ce1b29265E377e320CD24Eb632'  # 合约地址

    to_address = accounts[35].address

    coin_amount = 1000000000000000000

    gas_gwei = w.w3.from_wei(78564, 'gwei')

    data = '0xa9059cbb' + w.hex_zfill(to_address) + w.hex_zfill(coin_amount)
    print('data:',data)
    tx_param = w.build_tx_param(main_account, contract_address, gas_gwei=gas_gwei, data=data)

    tx_id = w.tx(main_account, tx_param=tx_param)
    print('mint: tx_id:', tx_id)
    rsp = w.get_receipt(tx_id)
    balance = w.get_balance(main_account.address, unit='ether')
    print('tx address:', ' balance:', balance)

    pass




if __name__ == '__main__':
    process()
    print('finish.....')
    pass