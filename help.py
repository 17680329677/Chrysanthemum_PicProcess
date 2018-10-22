"""
    一个辅助模块
    提取一些公共操作
    打包为方法
"""

import os
import psycopg2
import redis




# 创建新的文件夹
def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        return True
    else:
        return False


# 删除文件夹
def rmdir(path):
    try:
        os.rmdir(path)
        return True
    except:
        print("删除文件夹失败")
        return False


def remove_dir_file(path):
    if len(os.listdir(path)):   # 有文件、子文件夹
        for sub_name in os.listdir(path):
            # print(sub_name)
            sub_path = os.path.join(path, sub_name)
            if os.path.isfile(sub_path):    # 是文件
                os.remove(sub_path)
            else:   # 是文件
                remove_dir_file(sub_path)
    os.rmdir(path)     # 最后删除根文件夹


# 获取项目的绝对路径
def getRoot():
    project_dir = os.path.dirname(os.path.abspath(__file__));
    return project_dir


# 读取文件的操作
def read_conf(filename):
    import configparser
    import json

    with open(filename, 'r', encoding='utf-8') as f:
        config = json.load(f);
    return config


# 获取数据库连接的操作句柄
def openDB():
    # 配置数据库连接参数
    conn = psycopg2.connect(database="postgres", user='postgres', password='123456', host='127.0.0.1', port=5432)
    # 获取数据库连接句柄
    cur = conn.cursor()
    return [conn, cur]


# 写入redis数据库，以便php获取python的图片处理的状态
def save_redis(key_name, data, expire_time=600):
    redis_config = read_conf(getRoot() + '/config/dataConfig.json')['redis']
    r = redis.Redis(host=redis_config['host'], port=redis_config['port'])
    r.set(key_name, data)
    r.expire(key_name, expire_time)

