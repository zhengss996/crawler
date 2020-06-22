#-*- encoding: utf-8 -*-
'''
Created on 2017/7/1 13:49
Copyright (c) 2017/7/1, 海牛学院版权所有.
@author: 青牛
'''
from configs import config
import MySQLdb

class DBUtil:
    
    def __init__(self, db):
        self.db = MySQLdb.connect(host=db['HOST'], user=db['USER'], passwd=db['PASSWD'], db=db['DB'], charset=db['CHARSET'], port=db['PORT'])
        
    def read_one(self,sql):
        self.cursor = self.db.cursor()
        self.cursor.execute(sql)
        return self.cursor.fetchone()
        
    def read_tuple(self, sql):
        """execute sql return tuple
        select a,b,c from table
        ((a,b,c),(a,b,c))
        """
        self.cursor = self.db.cursor()
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def read_dict(self, sql):
        """execute sql return dict
        select a,b,c from table
        ({a:1,b:2,c:33},{a:1,b:3,c:45})
        """
        self.cursor = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def executemany(self,sql,values):
        '''
        insert into table (a,b,c) values(?,?,?)
        values   [(1,2,3),(324,6,1),(11,5,5)]
        :return:
        '''
        self.cursor = self.db.cursor()
        self.cursor.executemany(sql,values)
        self.db.commit()

    def executemany_no_commit(self,sql,values):
        self.cursor = self.db.cursor()
        self.cursor.executemany(sql,values)

    def execute(self,sql):
        self.cursor = self.db.cursor()
        self.cursor.execute(sql)
        self.db.commit()

    def execute_no_commit(self,sql):
        self.cursor = self.db.cursor()
        self.cursor.execute(sql)

    def commit(self):
        self.db.commit()

    def close(self):
        """close db connect
        """
        self.cursor = self.db.cursor()
        self.cursor.close()
        self.db.close()
    
    def rollback(self):
        """rollback db connect
        """
        self.db.rollback()
        
    def rollback_close(self):
        """rollback and close db connect
        """
        self.db.rollback()
        self.db.close()        
    
if __name__ == '__main__':
    db = DBUtil(config._HAINIU_DB)

    sql = """
    insert into hainiu_queue
        (type,action,params,fail_ip,create_times)
        values (1,"10153108084201229","Baltimore Ravens","Sports Team","2015-08-04 21:35:40");
    """
    for i in range(0,10):
        db.execute(sql)

    d = db.read_dict("select count(1) as n from hainiu_queue")
    print d
    db.close()

    #
    # from commons.util.log_util import LogUtil
    # l = LogUtil().get_base_logger()
    # try:
    #     dataT = db.read_dict("select id,action,params from hainiu_queue where type=1 and is_work =0 limit 0,1 for update")
    #     for objs in dataT:
    #         print objs
    #
    #
    #     id = dataT[0]["id"]
    #
    #     print id
    #     sql = "update hainiu_queue set is_work=1 where id=%s" % id
    #     db.execute(sql)
    #     db.commit()
    # except:
    #     l.exception()
    # finally:
    #     db.close()

