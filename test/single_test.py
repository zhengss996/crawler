#-*- encoding: utf-8 -*-
'''
single_test.py
Created on 2019/3/19 9:14
Copyright (c) 2019/3/19, 海牛学院版权所有.
@author: 潘牛
'''
import time,threading

print '---第一种单例模式不适合多线程---'
#第一种单例模式不适合多线程
class Singleton(object):
    def __init__(self):
        import time
        time.sleep(1)

    #classmethod   标明为类的方法，而类的方法第一个参数是cls，对象方法的第一个参数的是self，类方法是属于类的，
    #              而对象方法是属于对象的，类方法是公用的。而对象方法是属于对象自己的。
    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(Singleton, "_instance"):
            Singleton._instance = Singleton()
        return Singleton._instance



def task(arg):
    obj = Singleton.instance()
    print obj

for i in range(10):
    t = threading.Thread(target=task,args=[i,])
    t.start()

time.sleep(2)
print '2#' * 10


print '---第二种单例模式加了线程锁，变成适合多线程---'
#第二种单例模式加了线程锁，变成适合多线程
import time
import threading
class Singleton(object):
    _instance_lock = threading.Lock()
    def __init__(self):
        time.sleep(1)
    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(Singleton, "_instance"):
            with Singleton._instance_lock:
                if not hasattr(Singleton, "_instance"):
                    Singleton._instance = Singleton()
        return Singleton._instance

def task(arg):
    obj = Singleton.instance()
    print(obj)
for i in range(10):
    t = threading.Thread(target=task,args=[i,])
    t.start()
obj = Singleton.instance()
print(obj)

time.sleep(2)
print '3#' * 10

print '---第三种使用__new__方法---'
#第三种使用__new__方法
import time
import threading
class Singleton(object):

    _instance_lock = threading.Lock()
    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        with Singleton._instance_lock:
            if not hasattr(Singleton, "_instance"):
                Singleton._instance = object.__new__(cls, *args, **kwargs)
        return Singleton._instance
obj1 = Singleton()
obj2 = Singleton()
print(obj1,obj2)



time.sleep(2)
print '4#' * 10

print '---第四种方法使用元类__metaclass_---'
#第四种方法使用元类__metaclass__
import threading
class SingletonType(type):
    _instance_lock = threading.Lock()
    def __call__(self, *args, **kwargs):
        print '__call__'
        with SingletonType._instance_lock:
            if not hasattr(self, "_instance"):
                self._instance = super(SingletonType,self).__call__(*args, **kwargs)
        return self._instance

class Foo(object):
    __metaclass__ = SingletonType
    def __init__(self,name):
        self.name = name

obj1 = Foo('name')
obj2 = Foo('name')
print(obj1,obj2)