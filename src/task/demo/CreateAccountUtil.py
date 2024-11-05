import pandas as pd
import os
from eth_account import Account
from datetime import datetime

Account.enable_unaudited_hdwallet_features()

df_account = pd.DataFrame(columns=['Address','Seed Phrase','PrivateKey'])


account_count = 5000

for i in range(account_count):
    local_account,mnemonic_phrase = Account.create_with_mnemonic()
    private_key_bytes = local_account._private_key
    private_key = private_key_bytes.hex()[2:]
    address = local_account._address
    # 如果是追加到excel里，则要先获取当前的行数，再往下添加记录
    # rows = df_account.shape[0]
    # df_account.loc[rows+i] = [address, mnemonic_phrase, private_key]
    df_account.loc[i] = [address,mnemonic_phrase,private_key]
    print('{0}/{1} 创建成功：{2}'.format(i+1,account_count,address))
    # print('Address:', address)
    # print('Phrase:', mnemonic_phrase)
    # print('Private Key:', private_key)

print('-----------------------------------------\n')
file_name = datetime.now().strftime('%Y%m%d%H%M%S')+'.xlsx'
df_account.to_excel(file_name,index=False, engine="openpyxl")
print('已导出文件至'+os.path.abspath('.')+'\\'+file_name)
