import hashlib
import threading

from eth_account import Account
from web3 import Web3, middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy

from eth_account.messages import defunct_hash_message

from src.utils.block_chain import Block_chain
from src.utils.http_tools import HttpTools


class Web3Wrap:

    def __init__(self, block_chain = Block_chain.LINEA_TEST,  proxy_ip = '127.0.0.1:8889', timeout = 120, gas_flag = True):
        local_ip = HttpTools.get_host_ip()
        #print(local_ip)

        self.proxy_ip = proxy_ip
        self.proxies = HttpTools.build_proxy(proxy_ip)
        self.session = HttpTools.create_session(proxy_ip)

        if local_ip=='204.93.162.198' or local_ip == '213.59.119.132':
            self.w3 = Web3(Web3.HTTPProvider(block_chain.url))
        else:
            self.w3 = Web3(Web3.HTTPProvider(block_chain.url, session=self.session))
        self.timeout = timeout
        self.chainid = self.w3.eth.chain_id
        self.gas_flag = gas_flag

        if gas_flag:
            self.w3.eth.set_gas_price_strategy(medium_gas_price_strategy)
            self.w3.middleware_onion.add(middleware.time_based_cache_middleware)
            self.w3.middleware_onion.add(middleware.latest_block_based_cache_middleware)
            self.w3.middleware_onion.add(middleware.simple_cache_middleware)

        if block_chain.middleware == 'poa':
            pass
            ##self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    instance_dic ={'1':3}

    @staticmethod
    def get_instance(block_chain = Block_chain.LINEA_TEST,  proxy_ip = '127.0.0.1:8889', timeout = 120, gas_flag = True):
        str_msg = block_chain.url + proxy_ip
        key = hashlib.md5(str_msg.encode(encoding='utf-8')).hexdigest()
        if key in  Web3Wrap.instance_dic:
            pass
        else:
            with threading.RLock():
                if key not in Web3Wrap.instance_dic:
                    Web3Wrap.instance_dic[key] = Web3Wrap(block_chain, proxy_ip, timeout, gas_flag)

        return Web3Wrap.instance_dic[key]

    @staticmethod
    def get_instance(block_chain=Block_chain.LINEA_TEST, proxy_ip='127.0.0.1:8889', timeout=120, gas_flag=True):
        str_msg = block_chain.url + proxy_ip
        key = hashlib.md5(str_msg.encode(encoding='utf-8')).hexdigest()
        if key in Web3Wrap.instance_dic:
            pass
        else:
            with threading.RLock():
                if key not in Web3Wrap.instance_dic:
                    Web3Wrap.instance_dic[key] = Web3Wrap(block_chain, proxy_ip, timeout, gas_flag)

        return Web3Wrap.instance_dic[key]

    #Web3.to_int
    def get_balance(self, address = None, private_key = None, unit = 'wei'):
        balance = None
        if address:
            balance = self.w3.from_wei(self.w3.eth.get_balance(Web3.to_checksum_address(address)), unit)
        elif private_key:
            amount = self.w3.eth.get_balance(Account.from_key(private_key).address)
            balance = self.w3.from_wei(amount, unit)

        return balance

    def get_checksum_address(self, address):
        return Web3.to_checksum_address(address)

    """
    num <0 则 获取最新 block信息
    """
    def get_block(self,num=-1):
        if num>=0:
            j = self.w3.eth.get_block(num)
        else:
            j = self.w3.eth.get_block('latest')
        return j

    def get_tx(self, tx):
        return self.w3.eth.get_transaction(tx)

    def get_receipt(self, tx_id, timeout = 180):
        return self.w3.eth.wait_for_transaction_receipt(tx_id, timeout)

    def get_tx_count(self, address):
        return self.w3.eth.get_transaction_count(Web3.to_checksum_address(address))

    def get_gas_price(self, unit='wei'):
        if self.gas_flag :
            return self.w3.from_wei(self.w3.eth.generateGasPrice().real, unit)
        else :
            return self.w3.from_wei(self.w3.eth.gas_price, unit)


    def get_estimate_gas(self, tx_params , unit = 'wei'):
        gas_estimate = self.w3.eth.estimate_gas(tx_params)

        # 获取预估gas价格
        gas_price = self.w3.eth.gas_price
        gas_fee = gas_estimate * gas_price
        eth_fee = self.w3.fromWei(gas_fee, unit)
        return eth_fee

    def build_tx_param(self, from_account, to_address, data =None, gas_gwei=None, gas_price_gwei =None, value_eth = None, nonce = None):
        check_from_address = Web3.to_checksum_address(from_account.address)
        check_to_address = Web3.to_checksum_address(to_address)

        gasPrice = self.w3.to_wei(self.get_gas_price(), 'wei')

        if gas_price_gwei:
            gasPrice = self.w3.to_wei(gas_price_gwei, 'gwei')

        #print('nonce:', self.get_tx_count(Web3.to_checksum_address(check_from_address)))
        nonce_count = self.get_tx_count(Web3.to_checksum_address(check_from_address))
        if nonce:
            nonce_count = nonce

        param = {
            'chainId': self.chainid,
            'gasPrice': gasPrice,
            'from': check_from_address,
            'nonce': nonce_count,
            'to': check_to_address
        }


        if value_eth:
            param['value'] = self.w3.to_wei(value_eth, 'ether')

        if gas_gwei:
            param['gas'] = self.w3.to_wei(gas_gwei, 'gwei')
        else:
            param['gas'] = self.w3.to_wei(self.w3.eth.estimate_gas(param), 'wei') + 10000

        if data:
            param['data'] = data
        return param

    def tx(self, from_account, tx_param):
        signed = from_account.signTransaction(tx_param)
        return self.w3.eth.send_raw_transaction(signed.rawTransaction.hex()).hex()


    def contract_instance(self, address, abi):
        contract_address = Web3.to_checksum_address(address)
        return self.w3.eth.contract(address=contract_address, abi=abi).functions

    def contract_call(self, address, abi, method_name, **kwargs):
        return getattr(self.contract_instance(address=address, abi=abi), method_name)(**kwargs).call()

    def contract_func_call(self, instance_func, method_name, **kwargs):
        return getattr(instance_func, method_name)(**kwargs).call()

    def contract_build_tx_param(self, contract_address, abi, method_name, from_account, to_address = None, gas_gwei=None, gas_price_gwei=None, value_eth = None, **kwargs):
        check_from_address = Web3.to_checksum_address(from_account.address)
        func = getattr(self.w3.eth.contract(address=contract_address, abi=abi).functions, method_name)(**kwargs)
        gasPrice = self.w3.to_wei(self.get_gas_price(), 'wei')

        if gas_price_gwei:
            gasPrice = self.w3.to_wei(gas_price_gwei, 'gwei')

        param= func.build_transaction({
            #'from': check_from_address,  # 接受地址
            'gasPrice': gasPrice,
            'gas': 21000,
            'nonce': self.get_tx_count(Web3.to_checksum_address(check_from_address))

        })

        if to_address:
            param['to'] = Web3.to_checksum_address(to_address)

        if value_eth:
            param['value'] = self.w3.to_wei(value_eth, 'ether')

        if gas_gwei:
            param['gas'] = self.w3.to_wei(gas_gwei, 'gwei')
        else :
            del param['gas']
            param['gas'] = self.w3.to_wei(self.w3.eth.estimate_gas(param), 'wei') + 10000


        return param


    def contract_func_tx_param(self, func, from_account, to_address = None, gas_gwei=None, gas_price_gwei=None, value_eth = None):
        check_from_address = Web3.to_checksum_address(from_account.address)
        gasPrice = self.w3.to_wei(self.get_gas_price(), 'wei')

        if gas_price_gwei:
            gasPrice = self.w3.to_wei(gas_price_gwei, 'gwei')

        param = func.build_transaction({
            'gasPrice': gasPrice,
            'gas': 21000,
            'nonce': self.get_tx_count(Web3.to_checksum_address(check_from_address))

        })

        if to_address:
            param['to'] = Web3.to_checksum_address(to_address)

        if value_eth:
            param['value'] = self.w3.to_wei(value_eth, 'ether')

        if gas_gwei:
            param['gas'] = self.w3.to_wei(gas_gwei, 'gwei')
        else:
            del param['gas']
            param['gas'] = self.w3.to_wei(self.w3.eth.estimate_gas(param), 'wei') + 10000

        return param


    def hex_zfill(self, data):
        if isinstance(data, str):
            if data.startswith('0x'):
                msg = data[2:].zfill(64)
            else:
                msg = data.zfill(64)
        else:
            msg = self.w3.to_hex(data)[2:].zfill(64)
        return msg

    @staticmethod
    def parse_input(data, start=10):
        fun = data[0:start]
        print('#', fun)
        data = data[start:]
        for i in range(int(len(data) / 64)):
            str = data[64 * i:64 * (i + 1)]
            print('#', str, ':', int(str, 16))

    def tx_amount(self, from_account, to_address, amount, gas_price_gwei =None, gas_gwei = None, nonce = None):
        tx_param = self.build_tx_param(from_account, to_address, value_eth=amount,gas_price_gwei=gas_price_gwei, gas_gwei= gas_gwei, nonce = nonce)
        return self.tx_by_param(from_account, tx_param)

    def check_address(self, address):
        return Web3.to_checksum_address(address)
    def tx_by_param(self, from_account, tx_param):
        tx_id = self.tx(from_account, tx_param)
        print('[address]:', from_account.address, ' [tx_id]:', tx_id)
        rsp = self.get_receipt(tx_id)
        balance = self.get_balance(from_account.address, unit='ether')
        print('[status]:', rsp['status'], '[address]:', from_account.address, ' [balance]:', balance, ' [tx count]:',self.get_tx_count(from_account.address))
        return (tx_id, rsp, balance)

    def sign_data(self,sign_account:Account, msg):
        msghash = defunct_hash_message(text=msg)
        key = sign_account.key.hex()
        return self.w3.eth.account.signHash(msghash, key).signature.hex()
