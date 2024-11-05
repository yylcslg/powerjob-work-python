from src.cache.cache import taskCache
from src.task_core.task_core_instance import TaskCoreInstance
from src.utils.date_utils import DateUtils
from src.utils.tools_utils import read_proxy_ip
from src.web import processorTracker
from src.web.bean.instance_bean import InstanceBean, Instance_status
from src.web.bean.job_req import JobReq


@processorTracker.route('/a')
def hello():
    return 'Hello,processorTracker!'



def task_process(bean:InstanceBean):
    try:
        taskBean:JobReq = taskCache[bean.instanceId]
        processorInfo = taskBean.processorInfo.split('@')
        template_txt = TaskCoreInstance.read_local_file(processorInfo[0], processorInfo[1])

        jobParam = taskBean.jobParams.split('@')
        rs_dir = jobParam[0]
        accounts_exp_1 = jobParam[1]
        accounts_exp_2 = ''
        if(len(processorInfo)>2):
            accounts_exp_2= processorInfo[2]

        parallelism_num = taskBean.threadConcurrency
        bean.instanceStatus = Instance_status.RUNING.value


        # 可从配置文件读取
        proxy_ip_list = read_proxy_ip()
        account_2 = ''
        if accounts_exp_2 != '':
            account_2 = TaskCoreInstance.file_accounts(accounts_exp_2)[0]

        template_accounts_exp = accounts_exp_1.split(';')

        num = 0
        for account_exp in template_accounts_exp:
            num = num + 1

            t = TaskCoreInstance.file_accounts(rs_dir, account_exp)
            account_1_lst = t[0]
            account_tuple = t[1]

            param_dict = {}
            param_dict['batch_name'] = account_tuple[0]
            param_dict['start_num'] = account_tuple[1]
            param_dict['batch_from'] = account_tuple[3]

            bean.totalTaskNum = len(account_1_lst)

            TaskCoreInstance.instance_startup(template_txt, account_1_lst, account_2,
                                              parallelism_num=parallelism_num,
                                              instance_bean = bean,
                                              proxy_ip_list=proxy_ip_list,
                                              param_dict=param_dict)

        if(bean.instanceStatus != Instance_status.STOP.value):
            bean.instanceStatus = Instance_status.SUCCESS.value

        bean.endTime = DateUtils.get_timestamp()
        bean.result = 'SUCCESS'

    except Exception as e:
        bean.instanceStatus = Instance_status.FAIL.value
        bean.endTime = DateUtils.get_timestamp()
        bean.result = 'FAIL'
        print('task_process error...', e)



