# -*- coding: utf-8 -*-
# @Time    : 2019/3/25 19:51
# @Author  : wangluchao

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os
import datetime
# import smtplib
#
#
# def send_email(message, email_address):
#     sender = 'from@fromdomain.com'
#     receivers = email_address
#     try:
#         smtpObj = smtplib.SMTP('localhost')
#         smtpObj.sendmail(sender, receivers, message)
#         info = '邮件发送成功'
#         print info
#     except Exception,e:
#         info = '邮件发送失败！'
#         print info
#     return info


# MyEmail(to_list=收件人列表,tag=主题,content=邮件内容,doc=附件地址).send()
class MyEmail:
    def __init__(self, to_list, cc_list=None, tag='海外留学交流平台发送邮件', content=None, doc=None):
        """
        :param  user 发送人邮箱
        :param  passwd 发送人密码
        :param  to_list 收件人列表
        :param  cc_list 抄送人列表(经测试无效)
        :param  tag 主题
        :param  content 发宋内容 {'content': 'test','type': plain(文字)/html(html内容),'coding': 'utf-8',}
        :param  附件(附件全路径)
        """
        self.user = "wangluchao@starmerx.com"
        self.passwd = "Mox802352."
        self.to_list = to_list
        self.cc_list = []
        self.tag = tag
        self.content = content
        self.doc = doc


    def send(self):
        '''
        发送邮件
        '''
        # try:
        server = smtplib.SMTP_SSL("smtp.exmail.qq.com",port=465)
        server.login(self.user,self.passwd)
        print '正在发送邮件'
        server.sendmail("<%s>"%self.user, self.to_list, self.get_attach())
        server.close()
        print "邮件发送成功"
        # except Exception as e:
        #     print "send email failed %s"%e
    def get_attach(self):
        '''
        构造邮件内容
        '''
        attach = MIMEMultipart()
        if self.content:
            email_content = MIMEText(
                self.content.get('content', ''),
                self.content.get('type', 'plain'),
                self.content.get('coding', ''),
            )
            attach.attach(email_content)
        if self.tag is not None:
            #主题,最上面的一行
            attach["Subject"] = self.tag
        if self.user is not None:
            #显示在发件人
            attach["From"] = "海外留学交流平台<%s>"%self.user
        if self.to_list:
            #收件人列表
            attach["To"] = ";".join(self.to_list)
        if self.cc_list:
            #抄送列表
            attach["Cc"] = ";".join(self.cc_list)
        if self.doc:
            #估计任何文件都可以用base64，比如rar等
            #文件名汉字用gbk编码代替
            name = os.path.basename(self.doc)
            f = open(self.doc,"rb")
            doc = MIMEText(f.read(), "base64", "utf-8")
            doc["Content-Type"] = 'application/octet-stream'
            doc["Content-Disposition"] = 'attachment; filename="'+name+'"'
            attach.attach(doc)
            f.close()
        return attach.as_string()


if __name__ == '__main__':
    MyEmail(
        to_list=['1158529652@qq.com'],
        tag='test',
        content={
            'content': '车阿萨德发色的发',
            'type': 'plain',
            'coding': 'utf-8'
        }
    ).send()

def time_format(date):
    if date:
        format_time = (date+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
        return format_time
    else:
        return ''