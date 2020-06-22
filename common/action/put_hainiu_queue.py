#-*- encoding: utf-8 -*-
'''
put_hainiu_queue.py
Created on 2019/3/15 16:44
Copyright (c) 2019/3/15, 海牛学院版权所有.
@author: 潘牛
'''
import sys,traceback,time
from common.util.db_util import DBUtil
from configs.config import _HAINIU_DB as db_config

class PutHainiuQueue:

    def put_queue(self, show_num):
        select_count_sql = """
            select count(*) from hainiu_web_seed where status = 0;
        """
        select_limit_sql = """
            select url, category from hainiu_web_seed where status = 0 limit %s, %s;
        """

        insert_sql = """
            insert into hainiu_queue (type, action, params) values (%s, %s, %s);
        """
        db_util = DBUtil(db_config)
        try:
            #计算总数
            total_num = db_util.read_one(select_count_sql)
            #计算总页数
            page_num = total_num[0]/show_num if total_num[0] % show_num == 0 else total_num[0]/show_num + 1
            i = 0
            while i < page_num:
                limit_1 = i * show_num
                limit_2 = show_num
                print '%d , %d' % (limit_1, limit_2)
                sql = select_limit_sql % (limit_1, limit_2)
                print "select_limit_sql==> %s " % sql
                i += 1
                #分页查询结果
                result = db_util.read_dict(sql)
                values = []
                for row_dict in result:
                    url = row_dict['url']
                    category = row_dict['category']
                    #[(1, 'url1', 'c1'),(1,'url2','c2')]
                    values.append((1, url, category))

                print "insert values ==> %s" % values
                #将查询的结果进行批量insert插入
                db_util.executemany(insert_sql, values)

                #time.sleep(5)

        except Exception, message:

            traceback.print_exc(message)

        finally:
            db_util.close()


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    p = PutHainiuQueue()
    p.put_queue(2)