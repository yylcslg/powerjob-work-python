
from eth_account import Account
from web3 import Web3



def web3Wallet():
    w = Web3()
    acct = w.eth.account.create()
    address = acct.address # 地址
    private = acct.key.hex()
    acct.pu
    print("address:"+address +"  private:" +private)




def createMnemonicWallet():
    n =5
    for i in range(n):
        Account.enable_unaudited_hdwallet_features()
        account, mnemonic = Account.create_with_mnemonic()
        print("address:" + account.address +"  private key:" + account.key.hex() +" mnemonic:" + mnemonic)


#
def fromPrivateKey(key:str):
    account = Account.from_key(key)
    address = account.address
    print("Address:", address)

def fromMnemonic():
    Account.enable_unaudited_hdwallet_features()
    mnemonic_phrase ='report fold accident scout minor rude sign soup quantum skirt hobby chuckle'
    account = Account.from_mnemonic(mnemonic_phrase)
    private_key = account.privateKey.hex()
    address = account.address
    print("Generated Private Key:", private_key , "address:" + address)


if __name__ == '__main__':
    #web3Wallet()
    createMnemonicWallet()
    #fromPrivateKey('')
    #fromMnemonic()