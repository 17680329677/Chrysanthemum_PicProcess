import json
import help
import os
from PIL import Image


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
        cur.execute("select * from artificial_shot_pictures where cultivar_id = %s", (id[i]))
        rows = cur.fetchall()
        conn.commit()
        if rows:
            try:
                # 按照id再创建不同品种的文件夹
                help.mkdir(path + "\\" + id[i])
                for j in range(len(rows)):
                    image = Image.open(rows[j][3])
                    image.save(path + "\\" + id[i] + '\\' +rows[j][3].split('\\')[4], quality=50)
                    # shutil.copy(rows[j][3], path + "\\" + id[i])
                    print(rows[j][3].split('\\')[4])
            except:
                help.save_redis('artificial', json.dumps({
                    'status': 'failed',
                    'path': "",
                    'reason': "id为：" + id[i] + "的品种图片处理错误"
                }))

    help.save_redis('artificial', json.dumps({
        'status': 'success',
        'path': path,
        'id': id,
        'reason': ""
    }))

    cur.close()
    conn.close()
    return True
