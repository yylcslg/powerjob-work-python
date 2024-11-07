import random
from concurrent.futures import ThreadPoolExecutor

from src.service.proxy_service import Proxy_type
from src.utils import tools_utils
from src.utils.tools_utils import resource_path, msg_decode
from src.utils.wallet_account import Wallet
from src.web.bean.instance_bean import InstanceBean


class TaskCoreLocal:

    @staticmethod
    def local_run(template_txt,rs_dir,accounts_exp_1,accounts_exp_2='', parallelism_num =1):
        try:
            proxy_ip_list = ['127.0.0.1:8889']
            account_2=''
            if accounts_exp_2 != '':
                account_2 = TaskCoreLocal.file_accounts(accounts_exp_2)[0]

            template_accounts_exp = accounts_exp_1.split(';')

            for account_exp in template_accounts_exp:
                param_dict = {}
                t = TaskCoreLocal.file_accounts(rs_dir, account_exp)

                account_1_lst = t[0]
                account_tuple = t[1]
                param_dict['batch_name'] = account_tuple[0]
                param_dict['start_num'] = account_tuple[1]
                param_dict['batch_from'] = account_tuple[3]
                param_dict['account_total'] = len(account_1_lst)

                TaskCoreLocal.local_single(template_txt, account_1_lst, account_2, parallelism_num = parallelism_num,
                                           proxy_ip_list=proxy_ip_list, param_dict=param_dict)

        except Exception as e:
            print('local_run error...', e)

    @staticmethod
    def file_accounts(rs_dir,account_exp):
        dir_path = resource_path() + rs_dir+'/'
        if account_exp.strip().isspace():
            return []
        t = tools_utils.parse_exp(account_exp.strip())
        if t[2] == 0:
            accounts = Wallet.read_wallet_file(file_name=t[0]+'.csv', file_path_prefix=dir_path)[t[1]: ]
        else:
            accounts = Wallet.read_wallet_file(file_name=t[0] + '.csv', file_path_prefix=dir_path)[t[1]:t[2]]
        return (accounts, t)


    def local_single(template_txt,accounts_1_lst,accounts_2, proxy_ip_list, parallelism_num ,param_dict={}):
        try:
            if parallelism_num > 1:
                with ThreadPoolExecutor(max_workers=parallelism_num) as executor:
                    num = param_dict['start_num']
                    for a in accounts_1_lst:
                        proxy_ip = random.choice(proxy_ip_list)
                        executor.submit(TaskCoreLocal.run_single,
                                        template_txt,
                                        exe_num=num,
                                        account_1=a,
                                        account_2=accounts_2,
                                        proxy_ip=proxy_ip,
                                        param_dict=param_dict)
                        num = num + 1
            else:
                num = param_dict['start_num']
                for a in accounts_1_lst:
                    proxy_ip = random.choice(proxy_ip_list)
                    TaskCoreLocal.run_single(template_txt,
                                        exe_num=num,
                                        account_1=a,
                                        account_2=accounts_2,
                                        proxy_ip=proxy_ip,
                                        param_dict=param_dict)
                    num = num + 1

        except Exception as e:
            print('local_single error...', e)


    @staticmethod
    def run_single(template_txt, exe_num, account_1,  account_2, proxy_ip, param_dict={}):
        try:
            param_dict['account_1'] = account_1
            param_dict['proxy_ip'] = proxy_ip
            param_dict['account_2'] = account_2
            param_dict['exe_num'] = str(exe_num)
            param_dict['instance_id'] = -1
            param_dict['instance_bean'] = ''
            param_dict['wallet_address'] = account_1.address

            exec_param = {'param_dict': param_dict}

            exec(msg_decode(template_txt), exec_param)
        except Exception as e:
            print('run_single error：',e)
