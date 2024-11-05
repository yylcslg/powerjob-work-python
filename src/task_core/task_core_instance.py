import random
from concurrent.futures import ThreadPoolExecutor

from src.utils import tools_utils
from src.utils.tools_utils import resource_path, msg_decode, task_file_path, msg_encode
from src.utils.wallet_account import Wallet
from src.web.bean.instance_bean import InstanceBean, Instance_status


class TaskCoreInstance:

    @staticmethod
    def read_local_file(dir_name, file_name):

        with open(task_file_path() + dir_name + '/' + file_name) as f:
            template_txt = msg_encode(f.read())
        return template_txt

    @staticmethod
    def file_accounts(rs_dir,account_exp):
        dir_path=''
        dir_path = resource_path() + rs_dir+'/'
        if account_exp.strip().isspace():
            return []
        t = tools_utils.parse_exp(account_exp.strip())
        if t[2] == 0:
            accounts = Wallet.read_wallet_file(file_name=t[0]+'.csv', file_path_prefix=dir_path)[t[1]: ]
        else:
            accounts = Wallet.read_wallet_file(file_name=t[0] + '.csv', file_path_prefix=dir_path)[t[1]:t[2]]
        return (accounts, t)


    def instance_startup(template_txt,accounts_1_lst,accounts_2, proxy_ip_list, parallelism_num ,instance_bean:InstanceBean, param_dict={}):
        try:
            if parallelism_num > 1:
                with ThreadPoolExecutor(max_workers=parallelism_num) as executor:
                    num = param_dict['start_num']
                    for a in accounts_1_lst:
                        if(instance_bean.result == 'stop'):
                            instance_bean.instanceStatus = Instance_status.STOP.value
                            break
                        proxy_ip = random.choice(proxy_ip_list)
                        executor.submit(TaskCoreInstance.run_single,
                                        template_txt,
                                        exe_num=num,
                                        account_1=a,
                                        account_2=accounts_2,
                                        proxy_ip=proxy_ip,
                                        instance_bean=instance_bean,
                                        param_dict=param_dict)
                        num = num + 1
                        instance_bean.succeedTaskNum = instance_bean.succeedTaskNum + 1
            else:
                num = param_dict['start_num']
                for a in accounts_1_lst:
                    if (instance_bean.result == 'stop'):
                        instance_bean.instanceStatus = Instance_status.STOP.value
                        break
                    proxy_ip = random.choice(proxy_ip_list)
                    TaskCoreInstance.run_single(template_txt,
                                        exe_num=num,
                                        account_1=a,
                                        account_2=accounts_2,
                                        proxy_ip=proxy_ip,
                                        instance_bean=instance_bean,
                                        param_dict=param_dict)
                    num = num + 1
                    instance_bean.succeedTaskNum = instance_bean.succeedTaskNum + 1

        except Exception as e:
            print('instance_startup error...', e)


    @staticmethod
    def run_single(template_txt, exe_num, account_1,  account_2, proxy_ip, instance_bean:InstanceBean, param_dict={}):
        try:
            param_dict['account_1'] = account_1
            param_dict['proxy_ip'] = proxy_ip
            param_dict['account_2'] = account_2
            param_dict['exe_num'] = str(exe_num)
            param_dict['instance_id'] = instance_bean.instanceId
            param_dict['instance_bean'] = instance_bean

            exec_param = {'param_dict': param_dict}

            exec(msg_decode(template_txt), exec_param)
        except Exception as e:
            instance_bean.failedTaskNum = instance_bean.failedTaskNum + 1
            print('run_single error：',e)
