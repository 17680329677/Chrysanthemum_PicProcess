"""
    将用户请求获取的品种数据打包并发送至用户邮箱
"""
import os
import json
import help
import pandas as pd
import shutil
from datetime import datetime
from Email.sendEmail import send_email
from Email.pack import pack


def packAndSend(message):
    # 获取php消息中的参数
    msg = message.body.decode();
    email = json.loads(msg).get('email', None)
    classification = json.loads(msg).get('classification', None)
    cultivar_id = json.loads(msg).get('cultivar_id', None)
    quality = json.loads(msg).get('quality')
    type = json.loads(msg).get('type')

    try:
        set_file_path = pack(email, classification, cultivar_id, quality)
        # 若用户选择获取文件的方式是邮件发送
        if type == 'mail':
            # 发送邮件
            print("邮件正在发送到用户邮箱中，请稍后....")
            if send_email(email, set_file_path):
                help.save_redis(email.split('@')[0] + '_email', json.dumps({
                    'status': 'success'
                }))
            else:
                help.save_redis(email.split('@')[0] + '_email', json.dumps({
                    'status': 'failed',
                    'reason': 'Email send failed!'
                }))
            # 如果用户选择获取的方式是下载
        elif type == 'download':
            help.save_redis(email.split('@')[0] + '_dnload', json.dumps({
                'status': 'success',
                'reason': 'File pack success!'
            }))
    except Exception:
        print('打包或发送邮件失败！')
        help.save_redis(email.split('@')[0] + '_email', json.dumps({
            'status': 'failed',
            'reason': 'Pack file and Email send failed!'
        }))

    return True
