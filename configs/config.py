#-*- encoding: utf-8 -*-
'''
config.py
Created on 2019/1/4 9:29
Copyright (c) 2019/1/4, 海牛学院版权所有.
@author: 潘牛
'''

#日志地址
_LOG_DIR = '/tmp/python/hainiu_cralwer/log/%s'
# _LOG_DIR = '/data/python/hainiu_cralwer/log/%s'

#数据地址
_LOCAL_DATA_DIR = '/tmp/python/hainiu_cralwer/data/%s'
# _LOCAL_DATA_DIR = '/data/python/hainiu_cralwer/data/%s'

#数据库配置_测试
_HAINIU_DB = {'HOST':'localhost', 'USER':'root', 'PASSWD':'111111', 'DB':'hainiu_test', 'CHARSET':'utf8', 'PORT':3306}
# _HAINIU_DB = {'HOST':'nn1.hadoop', 'USER':'root', 'PASSWD':'12345678', 'DB':'hainiu_test', 'CHARSET':'utf8', 'PORT':3306}

# NAME, P_SLEEP_TIME, C_MAX_NUM, C_MAX_SLEEP_TIME, C_RETRY_TIMES
_QUEUE_DEMO = {'NAME':'demo', 'P_SLEEP_TIME': 5, 'C_MAX_NUM': 1, 'C_MAX_SLEEP_TIME': 3, 'C_RETRY_TIMES':3}

_QUEUE_HAINIU = {'NAME':'hainiu', 'P_SLEEP_TIME': 3, 'C_MAX_NUM': 1,
                 'C_MAX_SLEEP_TIME': 1, 'C_RETRY_TIMES':3, 'MAX_FAIL_TIMES': 6,
                 'LIMIT_NUM': 2}
#报警电话
_ALERT_PHONE = '110'

_FIND_NEWS_CONFIG = {'NAME':'findnews', 'P_SLEEP_TIME': 3, 'C_MAX_NUM': 5,
                 'C_MAX_SLEEP_TIME': 1, 'C_RETRY_TIMES':3, 'MAX_FAIL_TIMES': 6,
                 'LIMIT_NUM': 1}

_DOWN_NEWS_CONFIG = {'NAME':'downloadnews', 'P_SLEEP_TIME': 3, 'C_MAX_NUM': 10,
                 'C_MAX_SLEEP_TIME': 1, 'C_RETRY_TIMES':3, 'MAX_FAIL_TIMES': 6,
                 'LIMIT_NUM': 1,'FILE_FLAG':'one'}

_REDIS_CLUSTER_CONFIG = {'IPS':['192.168.142.160', '192.168.142.161',
                                '192.168.142.162'], 'PORT': '6379'}
#KAFKA队列配置
#_KAFKA_CONFIG = {'HOST':'nn1.hadoop:9092,nn2.hadoop:9092,s1.hadoop:9092', 'TOPIC':'hainiu_html_class4'}