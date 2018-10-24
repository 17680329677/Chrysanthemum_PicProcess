import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


def send_email(receiver, file_path):
    # 第三方smtp服务
    mail_host = "smtp.163.com"
    mail_user = "laobahepijiu@163.com"
    mail_pass = "DHZ19960618"

    # 发送人和接收人
    sender = "laobahepijiu@163.com"
    receivers = [receiver]

    mail_msg = """
        <h1>菊花数据平台-----数据打包</h1>
        <p>您选择的数据已经处理并打包在附件压缩包中！</p>
        <p><a href="http://www.baidu.com">返回平台</a></p>
    """
    # 创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = Header("北京林业大学", 'utf-8')
    message['To'] = Header("菊花数据平台测试", "utf-8")
    subject = "北京林业大学 菊花数据平台邮件测试"
    message['Subject'] = Header(subject, "utf-8")

    # 邮件的征文内容
    message.attach(MIMEText(mail_msg, 'html', 'utf-8'))

    # 构造附件
    file = MIMEText(open(file_path, 'rb').read(), 'base64', 'utf-8')
    file["Content-Type"] = 'application/octet-stream'
    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    file["Content-Disposition"] = 'attachment; filename="data.zip"'
    message.attach(file)

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print('邮件发送成功')
        return True
    except smtplib.SMTPException:
        print("邮件发送失败")
        return False


if __name__ == '__main__':
    pass
