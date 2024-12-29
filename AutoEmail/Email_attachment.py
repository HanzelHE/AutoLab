import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

class SendEmail:
    def __init__(self, mail_host, mail_user, mail_key, sender, *receivers):
        # 设置服务器信息
        self.mail_host = mail_host
        self.mail_user = mail_user
        self.mail_key = mail_key
        self.sender = sender
        # 把receivers可变参数这个元组转化成列表
        if not type(receivers).__name__ == 'list': #判断是否为列表
            self.receivers = list(receivers)

    def __login_and_send(self, message):

        smtp_obj = smtplib.SMTP()
        smtp_obj.connect(self.mail_host, 25)  #端口号
        smtp_obj.login(self.mail_user, self.mail_key)
        smtp_obj.sendmail(self.sender, self.receivers, message.as_string())
        smtp_obj.quit()
        
    def __to_receivers_convert(self, to_receivers):
        if isinstance(to_receivers, list):
            receivers_str = ''
            for receiver in to_receivers:
                receivers_str = receivers_str + receiver + '; '
            return receivers_str
        else:
            print('to_receivers参数的值必须是列表')

    def send_email_by_att(self, content, attachment_file_path, subject='自动化测试报告邮件_含附件'):
        # 编写含附件的邮件主体
        message = MIMEMultipart()
        message['Subject'] = subject
        message['From'] = self.sender
        # 如果 receivers 是列表，转化成字符型
        message['To'] = self.__to_receivers_convert(self.receivers)
        text_body = MIMEText(content, 'plain', 'utf-8')
        message.attach(text_body)
 
        att_file = open(file=attachment_file_path, mode='rb')
        att = MIMEApplication(att_file.read())
        att_file.close()
        # 动态获取并定义“附件名称” filename
        file_name = os.path.split(os.path.abspath(attachment_file_path))[1]
        att.add_header('content-disposition', 'attachment', filename=file_name)
        message.attach(att)
        # 调用私有方法 __login_and_send 进行邮件的连接、登录和最终发送
        self.__login_and_send(message)

if __name__ == '__main__': #自定义收发方
    mail_host = 'smtp.163.com' #服务器
    mail_user = 'xxxxxxx@163.com' #账号
    mail_key = 'xxxxxxxx' #设备密码
    sender = 'xxxxxxx.com' #发送者邮箱
    receivers = 'xxxxxx.com' #接受者邮箱发送者邮箱
    subject = '自定义主题'
    text = '自定义内容'
    filepath = r'./attachment.txt' #自定义附件
    send_email = SendEmail(mail_host, mail_user, mail_key, sender, receivers)
    if subject :
        send_email.send_email_by_att(text, filepath, subject)
    else:
        send_email.send_email_by_att(text, filepath)

