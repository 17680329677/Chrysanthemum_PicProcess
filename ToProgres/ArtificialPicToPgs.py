"""
    将人工拍摄的图片自动写入数据库对应表
    实现当感应到文件夹数据变化时
    自动执行该脚本
    将本次新增加的图片添加到数据库
"""
import os
import re
import help


# 定义一个读取指定文件夹所有文件名的方法
def get_filename(file_dir):
    L = []
    # root为文件根路径，dirs为该路径下子文件夹， files为该目录下所有文件的文件名
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            L.append(os.path.join(root, file))
    return L


"""
    参数：所有图片文件的绝对路径
    功能：将文件名分离，存入artificial_shot_pictures
"""


def save_to_pgs(pathList):
    database = help.openDB()
    conn = database[0]
    cur = database[1]
    for path in pathList:
        data = help.artificial_file_split(path)
        id = data[0]
        pic_type = data[1]
        pic_size = data[2]

        cur.execute("INSERT INTO artificial_shot_pictures (cultivar_id,pic_type,format,path,pic_size) "
                    "values  (%s,%s,%s,%s,%s)", (id, pic_type, 'JPG', path, pic_size))
        conn.commit()
    cur.close()
    conn.close
    print('执行完毕')



if __name__ == '__main__':
    print(help.getRoot() + '/config/dataConfig.json')
    pathList = get_filename(help.read_conf(help.getRoot() + '/config/dataConfig.json')['artificial'])
    print(pathList)
    # save_to_pgs(pathList)


