#from src.dao.job_dao import jobDao
#from src.dao.job_instance_dao import jobInstanceDao
#from src.dao.job_instance_detail_dao import jobInstanceDetailDao
from src.utils import tools_utils
from src.utils.date_utils import DateUtils


class JobService:

    def query_job(self, ts):
        #rs = jobDao.select_all(ts)
        #return rs
        return []


    def modify_job_exe_time(self, job, ts):
        msg_dict = {}
        msg_dict['latest_exe_time'] = ts
        msg_dict['id'] = job['id']
        #jobDao.update_by_id(msg_dict)


    def save_job_instance(self, job_dict):
        ts = DateUtils.get_timestamp()

        lst = []
        instance_dict = {}

        instance_dict['job_id'] = job_dict['id']
        instance_dict['job_name'] = job_dict['job_name']
        instance_dict['job_name_cn'] = job_dict['job_name_cn']
        instance_dict['template_id'] = job_dict['template_id']
        instance_dict['template_name'] = job_dict['template_name']
        instance_dict['instance_id'] = job_dict['instance_id']
        instance_dict['exe_time'] = ts
        instance_dict['batch_name'] = job_dict['batch_name']
        instance_dict['batch_from'] = job_dict['batch_from']
        instance_dict['account_total'] = job_dict['account_total']
        instance_dict['create_time'] = ts

        lst.append(instance_dict)
        #jobInstanceDao.insert_job_instance(lst)

    def save_job_instance_detail(self, job_dict_lst):
        lst = []
        for job_dict in job_dict_lst:
            detail_dict = {}
            ts = DateUtils.get_timestamp()
            detail_dict['instance_id'] = job_dict['instance_id']
            detail_dict['exe_time'] = ts
            tools.target_map_value(detail_dict, job_dict, 'job_name')
            tools.target_map_value(detail_dict, job_dict, 'template_id')

            tools.target_map_value(detail_dict, job_dict, 'template_name')
            tools.target_map_value(detail_dict, job_dict, 'batch_name')
            tools.target_map_value(detail_dict, job_dict, 'wallet_address')

            tools.target_map_value(detail_dict, job_dict, 'tx_id')
            tools.target_map_value(detail_dict, job_dict, 'tx_status')
            tools.target_map_value(detail_dict, job_dict, 'balance')
            tools.target_map_value(detail_dict, job_dict, 'tx_receipt')
            tools.target_map_value(detail_dict, job_dict, 'tx_param_1')
            tools.target_map_value(detail_dict, job_dict, 'tx_param_2')
            tools.target_map_value(detail_dict, job_dict, 'tx_param_3')
            tools.target_map_value(detail_dict, job_dict, 'tx_param_4')
            tools.target_map_value(detail_dict, job_dict, 'tx_error')

            lst.append(detail_dict)
        #jobInstanceDetailDao.insert_job_instance_detail(lst)

    def modify_instance_status(self, instance_id, status):
        #jobInstanceDao.update_job_instance_status(instance_id, status)
        pass



jobService = JobService()

if __name__ == '__main__':
    jobService.modify_instance_status('job_1_20231005_092816_0',2)



