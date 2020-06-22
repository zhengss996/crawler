#-*- encoding: utf-8 -*-
'''
test123.py
Created on 2019/3/19 12:19
Copyright (c) 2019/3/19, 海牛学院版权所有.
@author: 潘牛
'''
class PP (object):
    def __init__(self):
        print '__init__'

    def __new__(cls, *args, **kwargs):
        print '__new__'
        return super(PP, cls).__new__(cls,*args, **kwargs)

    def __call__(self, *args, **kwargs):
        print '__call__'

p = PP()
print '----------'
p()