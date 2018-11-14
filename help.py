"""
    一个辅助模块
    提取一些公共操作
    打包为方法
"""

import os
import psycopg2
import redis
import zipfile
import re


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


# 定义一个读取指定文件夹所有文件名的方法
def get_filename(file_dir):
    L = []
    # root为文件根路径，dirs为该路径下子文件夹， files为该目录下所有文件的文件名
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            L.append(os.path.join(root, file))
    return L


# 获取数据库连接的操作句柄
def openDB():
    # 配置数据库连接参数
    conn = psycopg2.connect(database="postgres", user='postgres', password='123456', host='127.0.0.1', port=5432)
    # 获取数据库连接句柄
    cur = conn.cursor()
    return [conn, cur]


def artificial_file_split(file_path):
    # 获取文件的名称
    file_name = file_path.split('\\')[-1]
    data = []

    # 利用正则搜索id
    id_search = re.search(r'\d+', file_name)
    id = id_search[0]
    data.append(id)
    # 将id截取掉
    str1 = file_name[id_search.end():len(file_name)]
    # 利用正则匹配图片类型 1：花，2-3：花瓣，4-5：叶
    type_search = re.search(r'\d+', str1)
    pic_type = type_search[0]
    data.append(pic_type)

    # 获取文件大小
    pic_size = os.path.getsize(file_path)
    pic_size = round(pic_size / float(1024 * 1024), 2)
    data.append(pic_size)
    return data


# 写入redis数据库，以便php获取python的图片处理的状态
def save_redis(key_name, data, expire_time=600):
    redis_config = read_conf(getRoot() + '/config/dataConfig.json')['redis']
    r = redis.Redis(host=redis_config['host'], port=redis_config['port'])
    r.set(key_name, data)
    r.expire(key_name, expire_time)


# 压缩文件的方法
def compress(get_file_path, set_file_path):
    f = zipfile.ZipFile(set_file_path, 'w', zipfile.ZIP_DEFLATED)
    
    for dirpath, dirnames, filenames in os.walk(get_file_path):
        fpath = dirpath.replace(get_file_path, '')
        fpath = fpath and fpath + os.sep or ''
        for filename in filenames:
            if filename != set_file_path.split('\\')[-1]:
                f.write(os.path.join(dirpath, filename), fpath+filename)
    f.close()
    print('压缩成功！')
