#-*- encoding: utf-8 -*-
'''
Created on 2017/7/1 13:49
Copyright (c) 2017/7/1, 海牛学院版权所有.
@author: 青牛
'''
import sys
sys.path.append('/home/hadoop/hainiu_crawler')

from common.util.db_util import DBUtil
from common.util.log_util import LogUtil
from configs import config
from download_page.util.redis_utill import RedisUtill
import time,random,json,redis


def push_queue_items():
    # 符合 写入的种子的队列数据的数量
    count_news_seed_queue_sql = """select count(*) from hainiu_queue where type=3 and fail_times=0;"""
    # 生成写入队列数据 条件： type=3
    insert_news_seed_internally_queue_items_sql = """insert into hainiu_queue (type,action,params) values(3,%s,%s);"""
    # 日志
    rl = LogUtil().get_base_logger()

    redisdb = RedisUtill()
    try:

        # 开始时间
        starttime = time.clock()

        redis_data_statu = True
        # 线程锁
        lock_key = 'get_news_seed_internally_data'
        sql = ""
        total_all = 0

        d = DBUtil(config._HAINIU_DB)
        d.execute_no_commit("set NAMES utf8mb4;")
        #符合 写入的种子的队列数据的数量 --- 之前的队列数据还没有处理完，所以不重新写队列数据到队列中
        sql = count_news_seed_queue_sql

        queue_total = d.read_one(sql)[0]
        if queue_total != 0:
            rl.info('last download_page queue not finish,last queue %s unFinish' % (queue_total))
            # return


        while redis_data_statu:

            is_lock = redisdb.get_conn().exists(lock_key)

            if is_lock==False:
                #锁上线程  --- 10 秒失效
                lockd =redisdb.get_lock(lock_key,10)
                if lockd == False:
                    rl.info('无法获取线程锁，退出采集下载queue线程 ')
                    continue

                ips = config._REDIS_CLUSTER_CONFIG['IPS']
                port = config._REDIS_CLUSTER_CONFIG['PORT']

                def scan_limit_to_queue_table(host, port, cursor, match, count):
                    total_num = 0
                    r = redis.Redis(host, port)
                    rs = r.scan(cursor, match, count)
                    next_num = rs[0]
                    key_list = []
                    value_list = []
                    for k in rs[1]:
                        key_list.append(k)
                        total_num += 1

                    # print key_list
                    print total_num
                    values = redisdb.get_values_batch_keys(key_list)

                    for v in values:
                        value_list.append((v,''))
                    print value_list

                    sql = insert_news_seed_internally_queue_items_sql
                    d.executemany(sql, value_list)

                    redisdb.delete_batch(rs[1])

                    if next_num == 0:
                        return total_num
                    return total_num + scan_limit_to_queue_table(host, port, next_num, match, count)

                total_num = 0
                for ip in ips:
                    total_num += scan_limit_to_queue_table(ip, port, 0,'down:*', 10)
                    print '======'
                print total_num

                if total_num > 0:
                    break

                redisdb.release(lock_key)
            else:
                rl.info('其他线程正在处理，请等待 ')
                time.sleep(0.3)
        endtime = time.time()
        # 一共执行的时间
        worksec = int(round((endtime - starttime)))
        # 日志

        rl.info('push seed_internally queue finish,total items %s,action time %s\'s' % (total_all,worksec))
    except:
        rl.exception()
        rl.error(sql)
        d.rollback()
    finally:
        redisdb.release(lock_key)
        d.close()

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    push_queue_items()