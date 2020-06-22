#-*- encoding: utf-8 -*-
'''
base_consumer_action.py
Created on 2019/3/13 10:34
Copyright (c) 2019/3/13, 海牛学院版权所有.
@author: 潘牛
'''
import sys
sys.path.append('')
class ConsumerAction(object):
    """
    消费动作基类
    """
    def __init__(self):
        self.current_retry_times = 0
        self.consumer_thread_name = ''


    def action(self):
        """
        制定消费动作的执行规则，子类实现具体的消费逻辑
        :return:
        """
        pass

    def result(self,success_flag, values):
        """
        action()返回时调用的方法
        :param success_flag: True:成功；False:失败
        :param values: []
        :return: [true, 1,2,3,4]
        """
        list = []
        if success_flag:
            self.success_action(values)

        else:
            self.fail_action(values)

        list.append(success_flag)
        for v in values:
            list.append(v)

        return list



    def success_action(self, values):
        """
        action(),执行成功返回结果前的逻辑处理
        :return:
        """
        pass


    def fail_action(self, values):
        """
        action(), 执行失败返回结果前的逻辑处理
        :return:
        """

        pass


