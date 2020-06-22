#-*- encoding: utf-8 -*-
'''
base_producer_action.py
Created on 2019/3/13 10:30
Copyright (c) 2019/3/13, 海牛学院版权所有.
@author: 潘牛
'''
class ProducerAction(object):
    """
    生产动作基类
    生产 消费动作ConsumerAction）实例列表
    """

    def queue_items(self):
        """
        制定 生产动作对象（ProducerAction） 生产 消费动作（ConsumerAction）实例列表 的规则,
        具体的生产逻辑由子类去实现
        :return: 消费动作实例列表(list)
        """
        pass