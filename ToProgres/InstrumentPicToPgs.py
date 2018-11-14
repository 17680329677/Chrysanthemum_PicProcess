"""
    将仪器拍摄的图片导入数据库
    命名：角度-品种编号-株号_拍摄日期_旋转次数
    侧视：C
    斜视：X
    顶视：D
"""
import os
import help
import re
from datetime import datetime


# 对仪器拍摄的原始数据图片进行清洗和入库
def OriginPicToPgs(pathList):
    database = help.openDB()
    conn = database[0]
    cur = database[1]
    for path in pathList:
        # 获取图片的文件名
        picName = path.split('\\')[-1]

        # 利用正则表达式对文件名进行查分
        pattern = r'[-|_|.]'
        result = re.split(pattern, picName)

        # 获取图片的各种属性准备入库
        angle = result[0]
        cultivar_id = result[1]
        plant_id = result[2]

        # 对日期做出转换
        date = str(result[3][:4]) + '-' + str(result[3][4:6]) + '-' + str(result[3][6:9])
        date = datetime.strptime(date, '%Y-%m-%d').date()
        revolution_num = result[4] # 旋转次数
        format = result[-1]
        # 获取文件大小
        pic_size = os.path.getsize(path)
        pic_size = round(pic_size / float(1024 * 1024), 2)

        cur.execute("INSERT INTO instrument_origin_pictures (cultivar_id,plant_id,format,angle,path,revolution_num,pic_date,pic_size) "
                     "values  (%s,%s,%s,%s,%s,%s,%s,%s)", (cultivar_id, plant_id, format, angle, path, revolution_num, date, pic_size))
        conn.commit()
        print(picName + '入库成功！')
    cur.close()
    conn.close()


# 对仪器处理过后的图片进行清洗和入库
def ProcessPicToPgs(pathList):
    # 通过help获取数据库连接对象和操作句柄
    database = help.openDB()
    conn = database[0]
    cur = database[1]

    for path in pathList:
        # 获取图片文件名
        picName = path.split('\\')[-1]
        # 使用正则表达式对图片名进行分割
        pattern = r'[-|_|.]'
        result = re.split(pattern, picName)
        angle = result[0]
        cultivar_id = result[1]
        plant_id = result[2]

        # 对日期做出转换
        date = str(result[3][:4]) + '-' + str(result[3][4:6]) + '-' + str(result[3][6:9])
        date = datetime.strptime(date, '%Y-%m-%d').date()
        revolution_num = result[4]
        if len(result) == 9:
            process_type = 'LBP'
        else:
            process_type = 'segmentation'
        format = result[-1]
        # 获取文件大小
        pic_size = os.path.getsize(path)
        pic_size = round(pic_size / float(1024 * 1024), 2)

        cur.execute("INSERT INTO instrument_process_pictures (cultivar_id,plant_id,pic_date,revolution_num, angle, process_type,format, path, pic_size) "
                    "values  (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(cultivar_id, plant_id, date, revolution_num, angle, process_type, format, path, pic_size))
        conn.commit()
        print(picName + '入库成功！')
    cur.close()
    conn.close()


if __name__ == '__main__':
    dir_path = help.read_conf(help.getRoot() + '/config/dataConfig.json')['instrument_origin'] + '\\D'
    pathList = help.get_filename(dir_path)
    OriginPicToPgs(pathList)
    # ProcessPicToPgs(pathList)
    # print(pathList)


