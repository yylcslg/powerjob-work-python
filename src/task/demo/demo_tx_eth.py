from src.task_core.web3_wrap import Web3Wrap
from src.utils.block_chain import Block_chain
from src.utils.wallet_account import Wallet


def process():
    w = Web3Wrap(block_chain=Block_chain.GOERLI_TEST, gas_flag=False)
    wallet = Wallet()
    #collect_eth(w, wallet, keep_amount=0.1)
    dispatch_eth(w, wallet, amount_eth = 0.1)
    #tx_eth_demo(w, wallet)


#收集 eth 到主账户
#main_amount 每个钱包最多保留的 eth, 留做gas费用
def collect_eth(w:Web3Wrap, wallet:Wallet, keep_amount=0.00008):
    accounts = wallet.read_test_wallet()
    main_account = accounts[0] # eth 收集到这个账户
    other_account = wallet.read_wallet_file(file_name='mnemonic_wallet_1.csv') # 等待收集的账户

    for a in other_account:
        balance = w.get_balance(a.address)
        if balance > w.w3.to_wei(keep_amount, 'ether'):
            # 账户内 超过 main_amount 的金额转出
            amount = balance - w.w3.to_wei(keep_amount, 'ether')
            print('amount:', amount)
            tx_eth(w, w.w3.from_wei(amount, 'ether'), main_account.address, a)

#分散eth到 其他账户
def dispatch_eth(w:Web3Wrap, wallet:Wallet, amount_eth = 0.1, keep_amount = 0.08):
    accounts = wallet.read_test_wallet()
    main_account = accounts[0]  # eth 收集到这个账户
    other_account = wallet.read_wallet_file(file_name='mnemonic_wallet_1.csv') # 等待收集的账户
    num = 0

    for a in other_account:
        num = num + 1
        print('------------------------',num,'--------------------------------------------')
        balance = w.get_balance(a.address)
        if balance < w.w3.to_wei(keep_amount, 'ether'):
            # gas_gwei = w.w3.from_wei(283155, 'gwei')
            # gas_price_gwei = 80
            # tx_param = w.build_tx_param(main_account, a.address ,
            #                             gas_gwei = gas_gwei,
            #                             gas_price_gwei=gas_price_gwei,
            #                             value_eth =amount_eth)
            # w.tx_by_param(from_account = main_account, tx_param= tx_param)
            gas_price_gwei = 0.01 *num
            tx_eth(w, amount_eth, a.address, main_account, gas_price_gwei=gas_price_gwei)



def tx_eth(w:Web3Wrap, amount, to_address, collect_ghost_account, gas_price_gwei):
    tx_param = w.build_tx_param(collect_ghost_account, to_address, value_eth=amount,gas_price_gwei=gas_price_gwei)
    tx_id = w.tx(collect_ghost_account, tx_param)
    print('tx_eth: tx_id:', tx_id)
    rsp = w.get_receipt(tx_id)
    balance = w.get_balance(to_address, unit='ether')
    print('tx_eth address:', ' balance:', balance)



def tx_eth_demo(w:Web3Wrap, wallet:Wallet, amount_eth = 0.001):
    accounts = wallet.read_test_wallet()
    main_account = accounts[0]  # eth 收集到这个账户
    a = wallet.read_wallet_file(file_name='mnemonic_wallet_1.csv')[1]  # 等待收集的账户

    #w.tx_amount(main_account, a.address, amount_eth)
    #tx_eth(w, amount_eth, main_account.address, a)

    tx_param = w.build_tx_param(a, main_account.address, value_eth=amount_eth)
    print(tx_param)
    w.tx_by_param(a, tx_param)

    pass


if __name__ == '__main__':
    process()
    print('finish.....')
    pass