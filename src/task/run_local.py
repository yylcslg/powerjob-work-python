import os

from src.task_core.task_core_local import TaskCoreLocal

from src.utils.tools_utils import msg_encode


def read_local_file(dir_name, file_name):
    curPath = os.path.abspath(os.path.dirname(__file__))
    with open(curPath+'/' +dir_name+'/'+ file_name) as f:
        template_txt = msg_encode(f.read())
    return template_txt



def run_mailzero(dir_name, file_name):
    template_txt = read_local_file(dir_name, file_name)
    dir_path = 'evm_wallet'
    accounts_exp_1 = 'test[:];tinc_wallet_1[:];tinc_wallet_2[:];tinc_wallet_3[:]'
    #accounts_exp_1 = 'test[:];tinc_wallet_1[:];tinc_wallet_2[:102]'
    accounts_exp_2 = ''
    parallelism_num = 1
    TaskCoreLocal.local_run(template_txt, dir_path,accounts_exp_1= accounts_exp_1, accounts_exp_2 = accounts_exp_2,
                            parallelism_num = parallelism_num,)



def run_btc_fault(dir_name, file_name):
    template_txt = read_local_file(dir_name, file_name)
    dir_path ='btc_wallet'
    accounts_exp_1 = 'btc_test_1[:46]'
    accounts_exp_2 = ''
    parallelism_num = 1
    TaskCoreLocal.local_run(template_txt, dir_path,accounts_exp_1= accounts_exp_1, accounts_exp_2 = accounts_exp_2,
                            parallelism_num = parallelism_num)


def run_test_email(dir_name, file_name):
    template_txt = read_local_file(dir_name, file_name)
    dir_path ='email'
    accounts_exp_1 = 'email[:]'
    accounts_exp_2 = ''
    parallelism_num = 1
    TaskCoreLocal.local_run(template_txt, dir_path,accounts_exp_1= accounts_exp_1, accounts_exp_2 = accounts_exp_2,
                            parallelism_num = parallelism_num)


def run_twitter(dir_name, file_name):
    template_txt = read_local_file(dir_name, file_name)
    dir_path ='twitter'
    accounts_exp_1 = 'x_1[:1]'
    accounts_exp_2 = ''
    parallelism_num = 1
    TaskCoreLocal.local_run(template_txt, dir_path,accounts_exp_1= accounts_exp_1, accounts_exp_2 = accounts_exp_2,
                            parallelism_num = parallelism_num)


if __name__ == "__main__":

    #run_mailzero('bnb', 'mailzero.py')
    #run_test_email('bnb', 'email.py')

    #run_btc_fault('bnb', 'btc_token.py')

    run_twitter('twitter', 'twitter_replay.py')


    print("finish...................")
