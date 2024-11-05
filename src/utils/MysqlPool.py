import pymysql
from dbutils.pooled_db import PooledDB

from src.utils.Properties import Properties

class MysqlPool:

    __pool = None

    def __init__(self):
        # 构造函数，创建数据库连接、游标
        self.coon = MysqlPool.getmysqlconn()
        self.cur = self.coon.cursor(cursor=pymysql.cursors.DictCursor)

    @staticmethod
    def getmysqlconn():
        if MysqlPool.__pool is None:
            #pro = Properties('./../resource/param.properties').getProperties()
            pro = Properties('../../resource/param.properties').getProperties()
            __pool = PooledDB(creator=pymysql, mincached=1, maxcached=20, host=pro.get('mysql_ip'),
                              user=pro.get('mysql_user'), passwd=pro.get('mysql_pwd'), db=pro.get('mysql_db'),
                              port=int(pro.get('mysql_port')), charset= 'utf8')
        return __pool.connection()

        # 查询

    def query(self, sql):
        self.cur.execute(sql)  # 执行sql
        rs = self.cur.fetchall()  # 返回结果为字典
        self.coon.commit()
        return rs

    def queryCount(self, sql: str):
        count = 0
        try:
            self.cur.execute(sql)
            count = self.cur.rowcount
            self.coon.commit()
        except Exception as e:
            print("Error: ", e)
        return count


    #insert, update, delete
    def exeSql(self, sql:str):
        state = 0
        try:
            self.cur.execute(sql)
            self.coon.commit()
            state = 1
        except Exception as e:
            print("Error: ", e)
            self.coon.rollback()
        return state



    def insertBatch(self, sql:str, lst):
        state = 0
        try:
            self.cur.executemany(sql, lst)
            self.coon.commit()
            state = 1
        except Exception as e:
            print("Error: ", e)
            self.coon.rollback()
        return state


    def dispose(self):
        self.coon.close()
        self.cur.close()

mysqlPool = MysqlPool()
