#-*- encoding: utf-8 -*-
'''
time_test.py
Created on 2019/3/19 17:02
Copyright (c) 2019/3/19, 海牛学院版权所有.
@author: 潘牛
'''
from common.util.time_util import TimeUtil

import threading,datetime,time

def task(arg):
    tu = TimeUtil()
    create_time = tu.get_timestamp()

    print create_time


for i in range(10):
    t = threading.Thread(target=task,args=[i,])
    t.start()