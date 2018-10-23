"""
    将用户请求获取的品种数据打包并发送至用户邮箱
"""
import json
import help
import pandas as pd
import os
import shutil
from datetime import datetime
import zipfile


def packAndSend(message):
    # 获取php消息中的参数
    msg = message.body.decode();
    email = json.loads(msg).get('email', None)
    classification = json.loads(msg).get('classification', None)
    cultivar_id = json.loads(msg).get('cultivar_id', None)
    quality = json.loads(msg).get('quality')

    if classification == 'artificial':
        database = help.openDB()
        conn = database[0]
        cur = database[1]

        rootDir = help.read_conf(help.getRoot() + '/config/dataConfig.json')['user_file']
        path = rootDir + '\\' + email.split('@')[0]
        nowTime = datetime.now().strftime('%Y-%m-%d_')

        # 读取列名
        cur.execute('select column_name from information_schema.columns where table_schema=%s and table_name=%s', ('public', 'artificial_character',))
        headers = cur.fetchall()
        header = []
        for i in range(len(headers)):
            header.append(headers[i][0])
        print(header)

        # 获取用户需要的指标数据，并转换成dataframe格式
        rows = []
        path_list = []
        for i in cultivar_id:
            # 查询特征形状的信息
            cur.execute('select * from artificial_character where id = %s', (i,))
            row = cur.fetchall()
            rows.append(row[0])
            # 查询指定id 的原图地址
            cur.execute('select path from artificial_shot_pictures where cultivar_id = %s', (i,))
            list = cur.fetchall()
            path_list.append(list)

        print(path_list)
        data = pd.DataFrame(rows)

        # 创建文件夹
        if help.mkdir(path):
            print('创建成功目录成功')
        else:
            print('目录已存在，正在清除旧数据')
            help.remove_dir_file(path)
            help.mkdir(path)
        # 将用户需求的数据写入excel中并保存在指定路径
        data.to_excel(path + '\\' + nowTime + '_artificial_characters.xls', header=header, index=False)

        for i in range(len(cultivar_id)):
            id = cultivar_id[i]
            help.mkdir(path + '\\' + id)
            for j in range(len(path_list[i])):
                shutil.copy(path_list[i][j][0], path + '\\' + id)
                print(path_list[i][j][0])

        # 将当前用户文件夹中的文件打包为压缩文件
        get_file_path = path
        set_file_path = path + '\\' + email.split('@')[0] + '.zip'
        help.compress(get_file_path, set_file_path)

        print('保存excel成功')

    return True
