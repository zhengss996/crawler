#-*- encoding: utf-8 -*-
'''
demo.py
Created on 2019/3/13 11:01
Copyright (c) 2019/3/13, 海牛学院版权所有.
@author: 潘牛
'''

import Queue
from common.action.base_producer_action import ProducerAction

from common.action.base_consumer_action import ConsumerAction

from common.action.producer import Producer

from configs.config import _QUEUE_DEMO

from common.util.log_util import LogUtil
class DemoProducerAction(ProducerAction):

    def queue_items(self):
        list = []
        for i in range(1, 11):
            print "produce apple_%d" % i
            action = DemoConsumerAction('apple_%d' % i )
            list.append(action)

        return list




class DemoConsumerAction(ConsumerAction):

    def __init__(self, name):
        super(self.__class__, self).__init__()
        self.name = name

        self.logger = LogUtil().get_logger("DemoConsumerAction", 'DemoConsumerAction')

    def action(self):
        self.logger.info('consume %s' % self.name)

        flag = True

        return self.result(flag, [self.name])


    def success_action(self):
        print 'success_op() ==> %s' % self.name


    def fail_action(self):
        print 'fail_op() ==> %s' % self.name





if __name__ == '__main__':
    q = Queue.Queue()
    p_action = DemoProducerAction()

    p = Producer(q,p_action,_QUEUE_DEMO['NAME'],_QUEUE_DEMO['P_SLEEP_TIME'],
                 _QUEUE_DEMO['C_MAX_NUM'],_QUEUE_DEMO['C_MAX_SLEEP_TIME'],
                 _QUEUE_DEMO['C_RETRY_TIMES'])

    #启动消费线程和生产线程
    p.start_work()



    #---------单线程玩法------------------------
    # q = Queue.Queue()
    #
    # p = DemoProducerAction()
    # #调用生产动作对象实例列表
    # list = p.queue_items()
    #
    # while True:
    #     if len(list) == 0 :
    #         break;
    #     #从列表取出往队列里放
    #     action = list.pop()
    #
    #     q.put(action)
    #
    #
    # while True:
    #     if q.empty():
    #         break
    #     #从队列里取出来进行消费
    #     action = q.get()
    #     action.action()










