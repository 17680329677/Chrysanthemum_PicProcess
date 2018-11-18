"""
    仪器拍摄图片的处理
"""
import json
import help
import os
from PIL import Image
import base64


def origin_process(message):
    msg = message.body.decode()
    email = json.loads(msg).get('email', None)
    id = json.loads(msg).get('id', None)

    database = help.openDB()
    conn = database[0]
    cur = database[1]

    if id:
        # 创建用户目录存放被选中的处理后的图片
        dir = help.read_conf(help.getRoot() + '/config/dataConfig.json')['instrument_compress']
        dir = dir + '\\' + email.split('@')[0]
        print(dir)
        if help.mkdir(dir):
            print("创建" + email + "目录成功！")
        else:
            print("用户目录已存在,清除旧数据")
            help.remove_dir_file(dir)
            help.mkdir(dir)

        for i in id:
            cur.execute("select path from instrument_origin_pictures where id = %s", (i,))
            result = cur.fetchall()
            conn.commit()
            if result:
                try:
                    # 读取图片地址
                    path = result[0][0]
                    # 获取图片的名称并将图片的格式转换为jpg方便压缩
                    pic_name = path.split('\\')[-1]
                    pic_name = pic_name.split('.')[0] + '.jpg'
                    image = Image.open(path)    # 将图片读取出来并
                    image.thumbnail((600, 400), Image.ANTIALIAS)    # 使用抗锯齿模式生成缩略图（压缩图片）
                    image.save(dir + '\\' + pic_name)
                    print(pic_name + '  生成缩略图成功')
                    with open(dir + '\\' + pic_name, 'rb') as img:
                        base64_data = base64.b64encode(img.read())
                        print(str(base64_data, 'utf8'))
                        base64_data = str(base64_data, 'utf8')
                        cur.execute("update instrument_origin_pictures set base64 = %s where id = %s", (base64_data, i,))
                        conn.commit()
                except:
                    help.save_redis('instrument_origin_' + email.split('@')[0], json.dumps({
                        'status': 'failed',
                        'reason': "id为：" + id[i] + "的品种图片处理错误"
                    }))
        help.save_redis('instrument_origin_' + email.split('@')[0], json.dumps({
            'status': 'success',
            'reason': 'Origin pictures process succeed!'
        }))
        cur.close()
        conn.close()

    return True


def pro_process(message):
    msg = message.body.decode()
    email = json.loads(msg).get('email', None)
    pathList = json.loads(msg).get('pathList', None)

    # 创建用户目录存放被选中的处理后的图片
    dir = help.read_conf(help.getRoot() + '/config/dataConfig.json')['instrument_compress']
    dir = dir + '\\' + email.split('@')[0]
    print(dir)
    if help.mkdir(dir):
        print("创建" + email + "目录成功！")
    else:
        print("用户目录已存在,清除旧数据")
        help.remove_dir_file(dir)
        help.mkdir(dir)

    database = help.openDB()
    conn = database[0]
    cur = database[1]
    try:
        # 对目标图片进行压缩处理并转换为base64存入数据库
        for path in pathList:
            pic_name = path.split('\\')[-1]
            print(pic_name)
            image = Image.open(path)
            image.thumbnail((600, 400), Image.ANTIALIAS)  # 使用抗锯齿模式生成缩略图（压缩图片）
            image.save(dir + '\\' + pic_name)
            print(pic_name + '  生成缩略图成功')
            with open(dir + '\\' + pic_name, 'rb') as img:
                base64_data = base64.b64encode(img.read())
                print(str(base64_data, 'utf8'))
                base64_data = str(base64_data, 'utf8')
                cur.execute("update instrument_process_pictures set base64 = %s where path = %s", (base64_data, path,))
                conn.commit()
        help.save_redis(email.split('@')[0] + '_pro_process', json.dumps({
            'status': 'success',
            'reason': 'proPic process successfully!'
        }))
    except:
        help.save_redis(email.split('@')[0] + '_pro_process', json.dumps({
            'status': 'failed',
            'reason': 'pic compress failed!'
        }))


    return True