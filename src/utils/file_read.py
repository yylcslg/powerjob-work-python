from src.utils import tools_utils
from src.utils.tools_utils import resource_path
from src.utils.wallet_account import Wallet


def file_accounts(rs_dir, account_exp):
    dir_path = resource_path() + rs_dir + '/'
    if account_exp.strip().isspace():
        return []
    t = tools_utils.parse_exp(account_exp.strip())

    ## 处理 evm  下的 账户
    if ('evm' in rs_dir):
        if t[2] == 0:
            accounts = Wallet.read_wallet_file(file_name=t[0] + '.csv', file_path_prefix=dir_path)[t[1]:]
        else:
            accounts = Wallet.read_wallet_file(file_name=t[0] + '.csv', file_path_prefix=dir_path)[t[1]:t[2]]
        return (accounts, t)
    else:
        if t[2] == 0:
            accounts = Wallet.read_wallet_line(file_name=t[0] + '.csv', file_path_prefix=dir_path)[t[1]:]
        else:
            accounts = Wallet.read_wallet_line(file_name=t[0] + '.csv', file_path_prefix=dir_path)[t[1]:t[2]]
        return (accounts, t)