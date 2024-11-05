import pymysql

from src.utils.Properties import Properties


class Mysql_DB:

    def __init__(self,host:str, user:str, pwd:str, db:str,portStr='3307'):
        port = int(portStr)
        self.db = pymysql.connect(host=host,
                             user=user,
                             port=port,
                             password=pwd,
                             database=db)



    def query(self, sql:str):
        cursor = self.db.cursor()
        rs = []
        try:
            cursor.execute(sql)
            rs = cursor.fetchall()
        except Exception as e:
            print("Error: ", e)
        return rs


    def queryCount(self, sql:str):
        cursor = self.db.cursor()
        count = 0
        try:
            cursor.execute(sql)
            count = cursor.rowcount
        except Exception as e:
            print("Error: ", e)
        return count

    #insert, update, delete
    def exeSql(self, sql:str):
        cursor = self.db.cursor()
        state = 0
        try:
            cursor.execute(sql)
            self.db.commit()
            state = 1
        except Exception as e:
            print("Error: ", e)
            self.db.rollback()
        return state



    def insertBatch(self, sql:str, lst):
        cursor = self.db.cursor()
        state = 0
        try:
            cursor.executemany(sql, lst)
            self.db.commit()
            state = 1
        except Exception as e:
            print("Error: ", e)
            self.db.rollback()
        return state



    @staticmethod
    def rowToDic(row, columns):
        dataDic = {}
        for i in range(len(columns)):
            dataDic[columns[i]] = row[i]
        return dataDic


    def close(self):
        self.db.close()


pro = Properties('../../resource/param.properties').getProperties()
mysql = Mysql_DB(pro.get('mysql_ip'), pro.get('mysql_user'), pro.get('mysql_pwd'), pro.get('mysql_db'), pro.get('mysql_port'))