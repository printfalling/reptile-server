#! /usr/bin/env python
import smtplib
from email.mime.text import MIMEText

mailto_list = ['wjn2015@mail.ustc.edu.cn']  # 收件人(列表)
mail_host = "smtp.126.com"  # 使用的邮箱的smtp服务器地址
mail_user = "mzzhangmin"  # 用户名
mail_pass = "971126"  # 密码
mail_postfix = "126.com"  # 邮箱的后缀


def send_mail(to_list, sub, content):
    me = "hello" + "<" + mail_user + "@" + mail_postfix + ">"
    msg = MIMEText(content, _subtype='plain')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)  # 将收件人列表以‘；’分隔
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)  # 连接服务器
        server.login(mail_user, mail_pass)  # 登录操作
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except(Exception) as e:
        print(str(e))
        return False


for i in range(5):  # 发送五封，不过会被拦截的。。。
    if send_mail(mailto_list, "来自SMTP的问候", "你好，这里是linux下的pycharm， 你的测试成功了！！"):  # 邮件主题和邮件内容
        print("done!" + ' ' + str(i + 1))
    else:
        print("failed!" + ' ' + str(i + 1))
