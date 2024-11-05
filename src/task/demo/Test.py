import random

import requests
from numpy import median
from requests.adapters import HTTPAdapter
from urllib3 import Retry
from web3 import Web3, EthereumTesterProvider, middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy

from src.task_core.web3_wrap import Web3Wrap
from src.utils.block_chain import Block_chain
from src.utils.wallet_account import Wallet


def create_session(proxy: str) -> requests.Session:
    session = requests.Session()
    session.proxies = {"http": proxy, "https": proxy}
    try:
        resp = session.get('http://ip-api.com/json/', timeout=10)
        data = resp.json()
        ip = data['query']
        country = data['country']
        city = data['city']
        print('代理ip：{0}，地区：{1}-{2}'.format(ip,country,city))
    except:
        return None

    retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    session.mount("http://", HTTPAdapter(max_retries=retries))
    session.mount("https://", HTTPAdapter(max_retries=retries))
    return session

def print_hi(name):
    #w3 = Web3(EthereumTesterProvider())
    #print(w3.is_connected())
    #print(w3.eth.get_block('latest'))

    #https://koge-rpc-bsc.48.club
    # w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/a4c5b4ef4d704823980c3349f3b99d18'))


    #https://mainnet.infura.io/v3/
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/a4c5b4ef4d704823980c3349f3b99d18', session=create_session("http://127.0.0.1:8889")))

    print(w3.is_connected())
    #print(w3.eth.get_block('latest'))
    print(w3.eth.blockNumber)



    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def contract_print():
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/a4c5b4ef4d704823980c3349f3b99d18', session=create_session("http://127.0.0.1:8889")))

    address = ''
    abi = '[{"inputs":[{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"symbol","type":"string"},{"internalType":"uint256","name":"maxNftSupply","type":"uint256"},{"internalType":"uint256","name":"saleStart","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"BAYC_PROVENANCE","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MAX_APES","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"REVEAL_TIMESTAMP","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"apePrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"baseURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"emergencySetStartingIndexBlock","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"flipSaleState","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxApePurchase","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"numberOfTokens","type":"uint256"}],"name":"mintApe","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"reserveApes","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"saleIsActive","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"baseURI","type":"string"}],"name":"setBaseURI","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"provenanceHash","type":"string"}],"name":"setProvenanceHash","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"revealTimeStamp","type":"uint256"}],"name":"setRevealTimestamp","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"setStartingIndex","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"startingIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"startingIndexBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenOfOwnerByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
    contract_instance = w3.eth.contract(address=address, abi=abi)


    print(contract_instance.functions.name().call())

    print(contract_instance.functions.symbol().call())

    #print(contract_instance.functions.decimals().call())
    print(contract_instance.functions.totalSupply().call())
    alice =''
    print(contract_instance.functions.balanceOf(alice).call())





def wallet():
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/a4c5b4ef4d704823980c3349f3b99d18',
                                session=create_session("http://127.0.0.1:8889")))

    wallet_address = ''

    print(w3.eth.getBalance(wallet_address) ,"wei")

    # balance here is formatted in ether,
    balance = w3.eth.getBalance(wallet_address)
    print(w3.fromWei(balance, "ether") ,"E")

    print(w3.eth.accounts)


def latest_middle_gas():
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/a4c5b4ef4d704823980c3349f3b99d18',
                                session=create_session("http://127.0.0.1:8889")))
    w3.eth.set_gas_price_strategy(medium_gas_price_strategy)

    w3.middleware_onion.add(middleware.time_based_cache_middleware)
    w3.middleware_onion.add(middleware.latest_block_based_cache_middleware)
    w3.middleware_onion.add(middleware.simple_cache_middleware)

    gas = w3.eth.generateGasPrice()
    print(gas.real)

# Press the green button in the gutter to run the script.

def test():
    lst = [1,2,3,4]
    for a in lst:
        print(a)

    pass




def send_demail():
    w = Web3Wrap(block_chain=Block_chain.BSC_ANKR, gas_flag=False)
    wallet = Wallet()

    data = '0x87260a7c0000000000000000000000007748e319e64c213917a7a2408ee4278f86875d58000000000000000000000000bc3b48c8ebbd0a33ae951a5f41b1e03d33f904190000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000012000000000000000000000000000000000000000000000000000000000000000'
    old_address = '7748e319e64c213917a7a2408ee4278f86875d58'
    new_address = '3c54D93214F2526A8184CaEb3560E96eFFE24e59'.lower()
    data = data.replace(old_address, new_address)

    test_account = wallet.read_wallet_file(file_name='mnemonic_wallet_1.csv')[0]

    gas_gwei = w.w3.from_wei(70705, 'gwei')
    tx_param = w.build_tx_param(test_account, '0x98f39d0f8c67885071cc99c5af1d4cacbcc89b0c', gas_gwei=gas_gwei, gas_price_gwei=1.1, data=data)
    w.tx_by_param(test_account, tx_param)

    print(data)





if __name__ == '__main__':
    send_demail()

    print('finish....')