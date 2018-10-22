import json
import help
import os
from PIL import Image
import base64


def artificial_pic_process(message):
    """
        人工拍摄图片的搜索与处理
    """
    # 获取php根据用户条件检索出的品种id
    msg = message.body.decode()
    id = json.loads(msg).get('id', None)
    email = json.loads(msg).get('email', None)


    # 创建用户目录存放被选中的处理后的图片
    path = help.read_conf(help.getRoot() + '/config/dataConfig.json')['artificial_porcessed']
    path = path + '\\' + email
    print(path)
    if help.mkdir(path):
        print("创建" + email + "目录成功！")
    else:
        print("用户目录已存在,清除旧数据")
        help.remove_dir_file(path)

    # 获取数据库连接
    database = help.openDB()
    conn = database[0]
    cur = database[1]

    # 在数据库中查询对应id的图片
    for i in range(len(id)):
        cur.execute("select * from artificial_shot_pictures where cultivar_id = %s", (id[i],))
        rows = cur.fetchall()
        conn.commit()
        if rows:
            try:
                # print(email.split('@')[0])
                # 为用户创建一个存储处理过的图片的数据表
                sql = '''create table if not exists pic_'''  + email.split('@')[0] + '''_artificial (cultivar_id INT NOT NULL, pic_type VARCHAR, base64 TEXT NOT NULL);'''
                cur.execute(sql)
                cur.execute("delete from pic_" + email.split('@')[0] + "_artificial")
                conn.commit()
                print("数据库表创建成功！")
            except:
                print("数据库表创建失败")

            try:
                # 按照id再创建不同品种的文件夹
                help.mkdir(path + "\\" + id[i])
                for j in range(len(rows)):
                    print(rows[j][3])

                    image = Image.open(rows[j][3])
                    image.save(path + "\\" + id[i] + '\\' +rows[j][3].split('\\')[-1], quality=10)
                    with open(path + "\\" + id[i] + '\\' +rows[j][3].split('\\')[-1], "rb") as img:
                        cultivar_id = id[i]
                        base64_data = base64.b64encode(img.read())
                        print(base64_data)
                        type = rows[j][3].split('\\')[-1].split('.')[0][-1]
                        sql = '''insert into pic_''' + email.split('@')[0] + '''_artificial (cultivar_id, pic_type, base64) values (%s,%s,%s)'''
                        cur.execute(sql, (cultivar_id, type, base64_data))
                        conn.commit()
                    # shutil.copy(rows[j][3], path + "\\" + id[i])
                    # print(rows[j][3].split('\\')[-1])
            except:
                help.save_redis('artificial', json.dumps({
                    'status': 'failed',
                    'path': "",
                    'reason': "id为：" + id[i] + "的品种图片处理错误"
                }))
    # 将处理的状态存储至redis数据库，方便php读取
    help.save_redis(email, json.dumps({
        'status': 'success',
        'path': path,
        'id': id,
        'email': email.split('@')[0],
        'reason': ""
    }))

    cur.close()
    conn.close()
    return True
