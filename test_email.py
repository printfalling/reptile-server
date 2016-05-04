#! /usr/bin/env python
import smtplib
from email.mime.text import MIMEText

mailto_list = [
            'cyh88888@mail.ustc.edu.cn'
            ]  # 收件人(列表)

mail_host = "smtp.126.com"  # 使用的邮箱的smtp服务器地址
mail_user = "mzzhangmin"  # 用户名
mail_pass = "971126"  # 密码
mail_postfix = "126.com"  # 邮箱的后缀


def send_mail(to_list, sub, content):
    me = "hello" + "<" + mail_user + "@" + mail_postfix + ">"
    msg = MIMEText(content, _subtype='plain')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user, mail_pass)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception as e:
        print(str(e))
        return False

if __name__ == '__main__':

    for i in range(100):  # 发送。。。
        if send_mail(mailto_list, "meeting", "I am here to informed you to take the meeting at 2:00"):  # 邮件主题和邮件内容
            print("done!" + " " + str(i))
        else:
            print("failed!")
