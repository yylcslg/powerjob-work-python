from src.task_core.tools.block_chain import Block_chain
from src.task_core.tools.web3_wrap import Web3Wrap
from src.utils.wallet_account import Wallet


def process():
    w = Web3Wrap(block_chain=Block_chain.LINEA_TEST, gas_flag=False)
    #w = Web3_wrap(block_chain=Block_chain.Sepolia, gas_flag=False)
    collect_mnemonic_wallet_eth(w, keep_amount= 0.2)



def collect_test_eth(w:Web3Wrap, keep_amount):
    wallet = Wallet()
    accounts = wallet.read_test_wallet()
    main_account = accounts[0]
    other_account = accounts[1:]


    for a in other_account:
        balance = w.get_balance(a.address)
        if balance > w.w3.to_wei(keep_amount, 'ether'):
            amount = balance - w.w3.to_wei(keep_amount, 'ether')
            print('address:', a.address, 'amount:', amount)
            tx_eth(w, w.w3.from_wei(amount, 'ether'), main_account.address, a)

    pass

def tx_eth(w:Web3Wrap, amount, to_address, collect_ghost_account):
    tx_param = w.build_tx_param(collect_ghost_account, to_address, value_eth=amount)
    tx_id = w.tx(collect_ghost_account, tx_param)
    print('tx_eth: tx_id:', tx_id)
    rsp = w.get_receipt(tx_id)
    balance = w.get_balance(to_address, unit='ether')
    print('tx_eth address:', to_address, ' balance:', balance)

def collect_ghost_file_eth(w:Web3Wrap, keep_amount):
    wallet = Wallet()
    main_account = wallet.read_test_wallet()[0]

    lst = [1, 2,3,4,5,6,7,8,9,10]
    for index in lst:
        num = str(index)
        filename = "ghost_wallet_" + num + ".csv"
        accounts = wallet.read_wallet_file(filename)

        balance = w.get_balance(accounts[0].address)
        if balance > w.w3.to_wei(keep_amount, 'ether'):
            amount = balance - w.w3.to_wei(keep_amount, 'ether')
            print('address:', accounts[0].address, 'amount:', amount)
            tx_eth(w, w.w3.from_wei(amount, 'ether'), main_account.address, accounts[0])

def collect_mnemonic_wallet_eth(w:Web3Wrap, keep_amount):
    wallet = Wallet()
    accounts = wallet.read_test_wallet()
    main_account = accounts[0]
    other_account = wallet.read_wallet_file(file_name='mnemonic_wallet_1.csv')

    num = 0
    for a in other_account:
        num = num +1
        print('-----------------', num, '-----------------------------')
        balance = w.get_balance(a.address)
        if balance > w.w3.to_wei(keep_amount, 'ether'):
            amount = balance - w.w3.to_wei(keep_amount, 'ether')
            print('address:', a.address, 'amount:', amount)
            tx_eth(w, w.w3.from_wei(amount, 'ether'), main_account.address, a)


if __name__ == '__main__':
    process()
    print('finish.....')
    pass