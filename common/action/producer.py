#-*- encoding: utf-8 -*-
'''
producer.py
Created on 2019/3/13 11:18
Copyright (c) 2019/3/13, 海牛学院版权所有.
@author: 潘牛
'''
import threading,time

from common.action.consumer import Consumer
from common.action.base_producer_action import ProducerAction
from common.util.log_util import LogUtil


class Producer(threading.Thread):
    """
    生产者线程
    """

    def __init__(self, queue, p_action, name, p_sleep_time, c_max_num, c_max_sleep_time, c_retry_times):
        """
        生产者线程初始化参数
        :param queue:            队列
        :param p_action:         生产动作对象实例
        :param name:             线程名称
        :param p_sleep_time:     生产线程每多长时间工作一次
        :param c_max_num:        消费线程的最大线程数
        :param c_max_sleep_time: 消费线程工作间隔最大休眠时间
        :param c_retry_times:    消费动作对象action 最大重试次数

        """
        super(self.__class__, self).__init__()
        self.queue = queue
        self.p_action = p_action
        self.name = name
        self.p_sleep_time = p_sleep_time
        self.c_max_num  = c_max_num
        self.c_max_sleep_time = c_max_sleep_time
        self.c_retry_times = c_retry_times

        #校验p_action 是不是 ProducerAction的子类，如果不是抛异常
        if not isinstance(self.p_action, ProducerAction):
            raise Exception("%s is not ProducerAction instance" % self.p_action.__name__)
        #初始化logger
        self.logger = LogUtil().get_logger("producer_%s" % self.name, "producer_%s" % self.name)


    def run(self):

        list = []
        while True:
            try:
                #获取starttime
                start_time = time.time()

                #判断list是否是空的，如果是，就调用 p_action.queue_ites()，
                # 生产 ConsumerAction 子类实例列表
                if len(list) == 0:
                    list = self.p_action.queue_items()


                #计算本次生产了多少
                total_num = len(list)

                #打印日志
                self.logger.info("queue.name=【producer_%s】, current time produce %d "
                                 "actions" % (self.name, total_num))

                while True:
                    #列表空了，就出去继续生产
                    if len(list) == 0:
                        break

                    #当队列的未完成数量小于等于最大消费线程数，就往queue里面put
                    if self.queue.unfinished_tasks <= self.c_max_num:
                        c_action = list.pop()

                        self.queue.put(c_action)

                # 获取endtime
                end_time = time.time()

                run_time = end_time - start_time

                # 计算每分钟生产多少个
                if run_time == 0:
                    rate = total_num
                else:
                    rate = round(float(total_num * 60) / run_time, 2)

                self.logger.info("queue.name=【producer_%s】, total_num=%d,"
                                 " produce %d actions/min, sleep_time=%d" %
                                 (self.name, total_num, rate, self.p_sleep_time))

                # 睡眠
                time.sleep(self.p_sleep_time)


            except Exception, message:
                self.logger.exception(message)








    def start_work(self):
        for i in range(0, self.c_max_num):
            c = Consumer(self.queue,'%s_%d' % (self.name, i+1),self.c_max_sleep_time,self.c_retry_times)
            c.start()
            time.sleep(2)

        self.start()

