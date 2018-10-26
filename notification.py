"""
    监控指定文件夹的变化
    为了用户更新数据实现自动入库做准备
    对文件实现监控利用watchdog实现
"""
from watchdog.observers import Observer
from watchdog.events import *
import time
import help
import os


class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_moved(self, event):
        if event.is_directory:
            print("directory moved from {0} to {1}".format(event.src_path, event.dest_path))
        else:
            print("file moved from {0} to {1}".format(event.src_path, event.dest_path))

    def on_created(self, event):
            if event.is_directory:
                print('不可向图片文件夹中添加此类文件！ 即将删除！')
                time.sleep(5)
                help.remove_dir_file(event.src_path)
            else:
                file_name = event.src_path.split('\\')[-1]
                format = file_name.split('.')[-1]
                if format != 'JPG':
                    print('请添加格式为JPG的图片，正在删除错误格式图片！')
                    time.sleep(5)
                    os.remove(event.src_path)
                else:
                    data = help.artificial_file_split(event.src_path)
                    id = data[0]
                    pic_type = data[1]
                    pic_size = data[2]

                    database = help.openDB()
                    conn = database[0]
                    cur = database[1]

                    cur.execute("INSERT INTO copy (cultivar_id,pic_type,format,path,pic_size) "
                                "values  (%s,%s,%s,%s,%s)", (id, pic_type, 'JPG', event.src_path, pic_size))
                    conn.commit()
                    cur.close()
                    conn.close

    def on_deleted(self, event):
        if event.is_directory:
            print("directory deleted: {0}".format(event.src_path))
        else:
            print("file deleted: {0}".format(event.src_path))

    def on_modified(self, event):
        if event.is_directory:
            print("directory modified: {0}".format(event.src_path))
        else:
            print("file modified: {0}".format(event.src_path))


if __name__ == '__main__':
    observer = Observer()
    event_handler = FileEventHandler()
    observer.schedule(event_handler, "G:\\mum_pic\\artificial\\pic1", True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()