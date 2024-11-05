from src.task_core.web3_wrap import Web3Wrap
from src.utils.block_chain import Block_chain
from src.utils.wallet_account import Wallet

contract_address = '0x9C4c49C3c3bd7ab49D91576d0103A25514CaD1D6'
contract_abi = '[{"inputs":[{"internalType":"address","name":"collection","type":"address"},{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"disperse","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"int256[3]","name":"sigmoidParams","type":"int256[3]"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":true,"internalType":"address","name":"friend","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"timestamp","type":"uint256"}],"name":"AssetAirdropped","type":"event"},{"inputs":[],"name":"baseAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"baseDisperse","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"nftAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nftsMinted","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"referralsNumber","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"friend","type":"address"}],"name":"sendMeGhostNft","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"x","type":"uint256"}],"name":"sigmoidValue","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"tokenAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"tokensMinted","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalTokensMinted","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'


def process():
    w = Web3Wrap(block_chain=Block_chain.LINEA_TEST, gas_flag=False)
    wallet = Wallet()
    contract_method_call(w, wallet)
    #contract_tx(w, wallet)
    #contract_instance_tx(w, wallet)

#当 合约参数 与类型明确时 调用方法
#
def contract_tx(w:Web3Wrap, wallet:Wallet):
    accounts = wallet.read_test_wallet()
    main_account = accounts[0]  # eth 收集到这个账户
    friend_address = accounts[0].address

    gas_gwei = w.w3.from_wei(245000, 'gwei')
    tx_param = w.contract_build_tx_param(contract_address=contract_address,
                                         abi=contract_abi,
                                         from_account=main_account,
                                         gas_gwei=gas_gwei,
                                         method_name='sendMeGhostNft',
                                         friend=friend_address)
    print('tx_param:', tx_param)
    tx_id = w.tx(main_account, tx_param=tx_param)
    print('tx_id:', tx_id)
    rsp = w.get_receipt(tx_id)
    balance = w.get_balance(main_account.address, unit='ether')
    print('tx address:', ' balance:', balance)


#当合约参数较复杂的时候调用方法
def contract_instance_tx(w:Web3Wrap, wallet:Wallet):
    accounts = wallet.read_test_wallet()
    main_account = accounts[0]  # eth 收集到这个账户
    friend_address = accounts[0].address

    gas_gwei = w.w3.from_wei(245000, 'gwei')

    func = w.contract_instance(contract_address, contract_abi).sendMeGhostNft(friend=friend_address)
    tx_param = w.contract_func_tx_param(func, from_account=main_account, gas_gwei=gas_gwei)

    print('tx_param:', tx_param)
    tx_id = w.tx(main_account, tx_param=tx_param)
    print('tx_id:', tx_id)
    rsp = w.get_receipt(tx_id)
    balance = w.get_balance(main_account.address, unit='ether')
    print('tx address:', ' balance:', balance)


# 合约 方法调用 demo
def contract_method_call(w:Web3Wrap, wallet:Wallet):
    accounts = wallet.read_test_wallet()
    main_account = accounts[0]  # eth 收集到这个账户

    flag =  w.contract_instance(contract_address, contract_abi).nftsMinted(main_account.address).call() == 1
    print('nft mint:', flag)


if __name__ == '__main__':
    process()
    print('finish.....')
    pass