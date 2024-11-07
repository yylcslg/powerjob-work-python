from eth_account import Account
from web3 import Web3

from src.utils import tools_utils
from src.utils.tools_utils import resource_path

"""
封装 web3 钱包创建方法
"""

class Wallet:

    @staticmethod
    def create_wallet(num:int):
        list = []
        w = Web3()
        for i in range(num):
            account = w.eth.account.create()
            list.append((account.address,account.key.hex()))

        return list

    @staticmethod
    def create_mnemonic_wallet(num:int):
        list = []
        Account.enable_unaudited_hdwallet_features()
        for i in range(num):
            account, mnemonic = Account.create_with_mnemonic()
            list.append((account.address, account.key.hex(),mnemonic))
        return list

    @staticmethod
    def from_private_key(private_key: str) -> Account:
        account = Account.from_key(private_key)
        return account

    @staticmethod
    def from_mnemonic(phrase:str) -> Account:
        Account.enable_unaudited_hdwallet_features()
        account = Account.from_mnemonic(phrase)
        return account

    @staticmethod
    def export_mnemonic_wallet(num:int, file:str):
        lst = Wallet.create_mnemonic_wallet(num)
        with open(file, "w+") as d:
            for t in lst:
                str = t[0]+","+t[1]+","+t[2]+"\n"
                d.write(str)

    @staticmethod
    def read_test_wallet(file_path_prefix= resource_path()):
        wallet_accounts = []

        with open(file_path_prefix + 'test.csv', 'r') as f:
            lst = f.readlines()
            for str in lst:
                array = str.replace('\n', '').split(',')
                wallet_accounts.append(Wallet.from_private_key(array[1]))
        return wallet_accounts

    @staticmethod
    def read_wallet_file(file_name='', file_path_prefix=resource_path()):
        wallet_accounts = []
        w = Wallet()

        with open(file_path_prefix + file_name, 'r') as f:
            lst = f.readlines()
            for str in lst:
                array = str.replace('\n', '').split(',')
                wallet_accounts.append(w.from_private_key(array[1]))
        return wallet_accounts

    @staticmethod
    def read_wallet_records(file_name='', file_path_prefix=resource_path()):
        wallet_accounts = []

        with open(file_path_prefix + file_name, 'r') as f:
            lst = f.readlines()
            for str in lst:
                array = str.replace('\n', '').split(',')
                wallet_accounts.append((array[0],array[1],array[2]))
        return wallet_accounts

    @staticmethod
    def read_wallet_line(file_name='', file_path_prefix=resource_path()):
        with open(file_path_prefix + file_name, 'r') as f:
            lst = f.readlines()

        return lst

    @staticmethod
    def create_prefix_address(prefix = '0x0', num=100):
        lst = []
        Account.enable_unaudited_hdwallet_features()
        count_num = 0
        while True:
            account, mnemonic = Account.create_with_mnemonic()
            if account.address.startswith(prefix) and account.address.endswith('0') == False:
                lst.append((account.address, account.key.hex(), mnemonic))
                count_num = count_num + 1
                print('create_prefix_address count_num:', count_num)
            if count_num >= num:
                break
        return lst

    @staticmethod
    def create_good_address():
        filename = 'a.csv'
        lst = Wallet.create_prefix_address(prefix = '0x0', num=100)

        with open(filename, "w+") as d:
            for t in lst:
                str = t[0] + "," + t[1] + "," + t[2] + "\n"
                d.write(str)

    @staticmethod
    def save_wallet_file(filename,lst, file_path_prefix=resource_path()):
        with open(file_path_prefix + filename, "w+") as d:
            for t in lst:
                str = t[0] + "," + t[1] + "," + t[2] + "\n"
                d.write(str)





if __name__ == '__main__':
    Wallet.create_good_address()

    # for i in range(10):
    #     num = str(1+i)
    #     wallet.export_mnemonic_wallet(1000,"../../resource/1ghost_wallet_"+num+".csv")
