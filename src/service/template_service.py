#from src.dao.template_dao import templateDao


class TemplateService:


    def create_template(self, template_name, template_txt, accounts_exp_1, accounts_exp_2, proxy_ip_exp, param_exp, template_desc):
        records = []
        records.append((template_name, template_txt, accounts_exp_1, accounts_exp_2, proxy_ip_exp, param_exp, template_desc))
        #templateDao.insert_batch(records)

    def modify_template(self, msg_dict):
        #templateDao.update_by_id(msg_dict)
        pass


    def query_template_by_name(self, template_name):
        #return templateDao.select_by_name(template_name)
        pass


templateService = TemplateService()

if __name__ == '__main__':
    c = TemplateService()

    print('')

    print('finish.....')