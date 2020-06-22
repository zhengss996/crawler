#-*- encoding: utf-8 -*-
'''
consumer.py
Created on 2019/3/13 11:31
Copyright (c) 2019/3/13, 海牛学院版权所有.
@author: 潘牛
'''
import threading,time,random

from common.util.log_util import LogUtil


class Consumer(threading.Thread):

    _MAX_RETRY_TIMES = 0

    def __init__(self, queue, name, max_sleep_time, retry_times):
        super(self.__class__, self).__init__()
        self.queue = queue
        self.name = name
        self.max_sleep_time = max_sleep_time
        self.retry_times = retry_times
        Consumer._MAX_RETRY_TIMES = retry_times
        #初始化日志
        self.logger = LogUtil().get_logger("comsumer_%s" % self.name, "comsumer_%s" % self.name)

    def run(self):
        while True:
            try:
                #如果队列是空的，就睡眠一会，继续判断
                if self.queue.empty():
                    time.sleep(self.max_sleep_time)
                    continue

                #获取开始时间
                start_time = time.time()

                #从队列（queue）里取出action
                action = self.queue.get()

                action.consumer_thread_name = self.name

                #在调用action()进行消费
                result = action.action()

                rs = 'SUCCESS' if result[0] else 'FAIL'

                #获取结束时间
                end_time = time.time()


                #获取随机休眠时间
                random_sleep_time = round(random.uniform(0.2, self.max_sleep_time), 2)


                run_time = end_time - start_time

                #打印日志
                self.logger.info("queue.name=【comsumer_%s】, run_time=%d, sleep_time=%d, retry_times=%d, "
                                 " result=%s, detail=%s" % (self.name, run_time,
                                random_sleep_time, action.current_retry_times, rs,result[1:]))



                #判断结果成功还是失败，如果是失败，并且失败次数小于最大重试次数，需要重试
                if not result[0] and action.current_retry_times < self.retry_times:
                    action.current_retry_times += 1
                    self.queue.put(action)

                #无论成功失败都要执行
                self.queue.task_done()

                #随机睡眠
                time.sleep(random_sleep_time)
            except Exception, message:
                self.logger.exception(message)
