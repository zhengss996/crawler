#-*- encoding: utf-8 -*-
'''
hainiu_queue.py
Created on 2019/3/15 11:37
Copyright (c) 2019/3/15, 海牛学院版权所有.
@author: 潘牛
'''
import sys,Queue
from common.action.base_producer_action import ProducerAction
from common.action.base_consumer_action import ConsumerAction
from common.util.db_util import DBUtil
from common.util.log_util import LogUtil
from configs.config import _HAINIU_DB as db_config
from configs.config import _QUEUE_HAINIU as q_config
from common.action.consumer import Consumer
from common.action.producer import Producer
from common.util.util import Util

class HainiuProducerAction(ProducerAction):
    def __init__(self, max_fail_times, limit_num):
        super(self.__class__, self).__init__()
        self.max_fail_times = max_fail_times
        self.limit_num = limit_num;
        self.logger = LogUtil().get_logger('HainiuProducerAction', 'HainiuProducerAction')


    def queue_items(self):
        #多台机器的时候，查询带上 fail_ip != ip
        # select_sql = """
        # select id, action, params from hainiu_queue \
        # where type='1' and is_work = 0 and fail_ip != '%s' and  fail_times < %d limit 0, %d for update;
        # """


        #行锁
        select_sql = """
        select id, action, params from hainiu_queue \
        where type='1' and is_work = 0 and fail_times < %d limit 0, %d for update;
        """

        update_sql = """
        update hainiu_queue set is_work=1  where id in (%s);
        """
        list = []
        try:
            db_util = DBUtil(db_config)
            #多个行
            result = db_util.read_dict(select_sql % (self.max_fail_times, self.limit_num))
            ids = []

            for row_dict in result:
                id = row_dict['id']
                action = row_dict['action']
                params = row_dict['params']

                c_action = HainiuConsumerAction(id,action,params, self.max_fail_times)
                list.append(c_action)
                #[1,2,3,4]
                ids.append(str(id))

            if len(ids) != 0:
                ids = ','.join(ids)
                db_util.execute_no_commit(update_sql % ids)
            db_util.commit()
        except Exception, message:
            db_util.rollback_close()
            self.logger.exception(message)

        finally:
            db_util.close()

        return list



class HainiuConsumerAction(ConsumerAction):
    def __init__(self, id, act, params,max_fail_times):
        super(self.__class__,self).__init__()
        self.id = id
        self.act = act
        self.params = params
        self.max_fail_times = max_fail_times

        self.logger = LogUtil().get_logger("HainiuConsumerAction", "HainiuConsumerAction")

    def action(self):
        print 'id=%s, action=%s, parmas=%s' % (self.id,self.act,self.params)

        return self.result(True,[self.id,self.act,self.params])

    def success_action(self):
        """
        删除队列的数据信息
        """
        sql = "delete from hainiu_queue where id=%s" % self.id


        try:
            db_util = DBUtil(db_config)

            db_util.execute(sql)
        except Exception, message:
            self.logger.exception(message)
        finally:
            db_util.close()



    def fail_action(self):
        """
        1)更新失败次数、设置失败ip
        2）如果失败次数达到了当前机器的最大失败次数，将is_work更新0；
        """

        update_sql1 = """
            update hainiu_queue set fail_times=fail_times+1, fail_ip='%s'  where id=%s and fail_times < %s;
        """

        update_sql2 = """
             update hainiu_queue set is_work=0  where id=%s;
        """

        try:
            db_util = DBUtil(db_config)
            u = Util()
            ip = u.get_local_ip()
            db_util.execute_no_commit(update_sql1 % (ip, self.id, self.max_fail_times))
            num_1 = self.current_retry_times +1

            self.logger.info("self.current_retry_times1==> %d" % num_1)
            if self.current_retry_times +1 == Consumer._MAX_RETRY_TIMES \
                 and self.current_retry_times + 1 <self.max_fail_times:
                db_util.execute_no_commit(update_sql2 % self.id)

            db_util.commit()

        except Exception, message:
            self.logger.exception(message)

        finally:
            db_util.close()



if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    q = Queue.Queue()
    p_action = HainiuProducerAction(q_config['MAX_FAIL_TIMES'],q_config['LIMIT_NUM'])

    p = Producer(q,p_action,q_config['NAME'],q_config['P_SLEEP_TIME'],
                 q_config['C_MAX_NUM'],q_config['C_MAX_SLEEP_TIME'],
                 q_config['C_RETRY_TIMES'])

    p.start_work()