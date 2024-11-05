from src.task_core.web3_wrap import Web3Wrap
from src.utils.block_chain import Block_chain
from src.utils.MysqlDB import mysql


def test_sql():
    columns = ['user_name', 'user_pwd', 'user_desc', 'user_flag']
    columns_str = ','.join([x for x in columns])
    sql = 'SELECT ' + columns_str + ' FROM b_user_info'

    # sql = "insert into b_user_info(user_name,user_pwd,user_desc, user_flag) VALUES('test_11','test_1_pwd','test_1_desc',1)"
    # sql = 'delete from b_user_info where id =2'

    # sql = "update b_user_info set user_name = 'tes001' where id =1"
    rs = mysql.query(sql)
    print(rs)


def test_query_wallet():
    #wallet =WalletDao()
    #rs = wallet.queryByBatch('ba')
    #print('rs:',rs)
    pass



if __name__ == '__main__':
    #test_sql()
    #test_query_wallet()
    proxy_ip = '127.0.0.1:8889'
    b1 = Web3Wrap.get_instance(block_chain=Block_chain.BSC_ANKR, proxy_ip= proxy_ip)
    Web3Wrap.get_instance(block_chain=Block_chain.BSC_ANKR, proxy_ip='127.0.0.1:8889')
    Web3Wrap.get_instance(block_chain=Block_chain.BSC_ANKR, proxy_ip='127.0.0.1:8889')
    Web3Wrap.get_instance(block_chain=Block_chain.BSC_ANKR, proxy_ip='127.0.0.1:8889')
    Web3Wrap.get_instance(block_chain=Block_chain.BSC_ANKR, proxy_ip='127.0.0.1:8889')
    Web3Wrap.get_instance(block_chain=Block_chain.BSC_ANKR, proxy_ip='127.0.0.1:8889')
    b2 = Web3Wrap.get_instance(block_chain=Block_chain.BSC_ANKR, proxy_ip='127.0.0.1:8889')
    print(b1,b2)
    print('finish.....')
    pass