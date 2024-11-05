from src.task_core.tools.block_chain import Block_chain
from src.task_core.tools.web3_wrap import Web3Wrap
from src.utils.wallet_account import Wallet


def process():
    w = Web3Wrap(block_chain=Block_chain.BSC, gas_flag=False)
    wallet = Wallet()

    coin_amount = w.w3.to_wei(50000000, 'ether')
    collect_token(w, wallet, '0xf0f2888e61afadf66aedf278ffc324798879d5c1', coin_amount)



def collect_token(w:Web3Wrap, wallet:Wallet, contract_address, coin_amount):
    accounts = wallet.read_test_wallet()
    main_account = accounts[0]  # eth 收集到这个账户
    to_address = accounts[35].address

    data = '0xa9059cbb' + w.hex_zfill(to_address) + w.hex_zfill(coin_amount)
    print('data:', data)
    gas_gwei = w.w3.from_wei(888426, 'gwei')
    tx_param = w.build_tx_param(main_account, contract_address, gas_gwei=gas_gwei, data=data)

    # tx_id = w.tx(main_account, tx_param=tx_param)
    # print('mint: tx_id:', tx_id)
    # rsp = w.get_receipt(tx_id)
    # balance = w.get_balance(main_account.address, unit='ether')
    # print('tx address:', ' balance:', balance)

    pass









if __name__ == '__main__':
    process()
    print('finish.....')
    pass