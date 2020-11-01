import os
import win32com.client as win32
import smtplib
import datetime
from utils import getpathInfo, readConfig

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

import time

read_conf = readConfig.ReadConfig()
subject = read_conf.get_email('subject')#从配置文件中读取，邮件主题
app = str(read_conf.get_email('app'))#从配置文件中读取，邮件类型
msg_from = read_conf.get_email('msg_from')#从配置文件中读取，邮件发送人
msg_pwd = read_conf.get_email('msg_pwd')#从配置文件中读取，邮件发送授权码
msg_to = read_conf.get_email('msg_to')#从配置文件中读取，邮件收件人
msg_cc = read_conf.get_email('msg_cc')#从配置文件中读取，邮件抄送人
content = read_conf.get_email('content') #邮件内容
mail_path = os.path.join(getpathInfo.get_Path(), 'result', 'report.html')#获取测试报告路径

ISOTIMEFORMAT = '%Y%m%d'

class send_email():
    def outlook(self):
        olook = win32.Dispatch("%s.Application" % app)#app=Outlook
        mail = olook.CreateItem(win32.constants.olMailItem)
        mail.To = msg_to # 收件人
        mail.CC = msg_cc # 抄送
        mail.Subject = str(datetime.datetime.now())[0:19]+'%s' %subject#邮件主题
        mail.Attachments.Add(mail_path, 1, 1, "myFile")
        content = """
                    执行测试中……
                    测试已完成！！
                    生成报告中……
                    报告已生成……
                    报告已邮件发送！！
                    """
        mail.Body = content
        mail.Send()

    def sendTencent(self):
        '''
        msg_from='xxxxxxxxx@qq.com'                                 #发送方邮箱
        passwd='abcdefghigklmnop'                                   #填入发送方邮箱的授权码
        msg_to='xxxxx@foxmail.com'                                  #收件人邮箱

        subject="python邮件测试"                                     #主题
        content="这是我使用python smtplib及email模块发送的邮件"     　#正文

        msg = MIMEText(content)
        msg['Subject'] = subject
        msg['From'] = msg_from
        msg['To'] = msg_to
        try:
            s = smtplib.SMTP_SSL(app,465) #邮件服务器及端口号
            s.login(msg_from, msg_pwd)
            s.sendmail(msg_from, msg_to, msg.as_string())
            print("发送成功")
        except smtplib.SMTPException  as e:
            print("发送失败")
        finally:
            s.quit()
            '''
        #==============定义发送邮件 ===============
        f = open(mail_path,'rb')
        #读取测试报告正文
        mail_body = f.read()
        f.close()
        # 发送邮箱服务器
        smtpserver = "smtp.exmail.qq.com"
        # 发件人邮箱
        sender = 'wangyan@tuying.com.cn'
        # 发件人邮箱密码
        password = 'Wcgr7jydk5mwwx2X'
        # 接收人邮箱
        receiver = ['wangyan@tuying.com.cn']

        #通过  模块构造的带附件的邮件如图
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = msg_from
        msg['To'] = msg_to
        #编写html类型的邮件正文，MIMEtext()用于定义邮件正文
        #发送正文
        text = MIMEText(mail_body, 'html', 'utf-8')
        text['Subject'] = Header('自动化测试报告', 'utf-8')
        msg.attach(text)
        #发送附件
        #Header()用于定义邮件标题
        msg['Subject'] = Header('自动化测试报告', 'utf-8')
        msg_file = MIMEText(mail_body, 'html', 'utf-8')
        msg_file['Content-Type'] = 'application/octet-stream'
        msg_file["Content-Disposition"] = 'attachment; filename="TestReport.html"'
        msg.attach(msg_file)

        # 如果只发正文的话，上面的代码 从receiver下面到这段注释上面
        # 全部替换为下面的两行代码即可，上面的代码是增加了发送附件的功能。
        #     text = MIMEText(mail_body, 'html', 'utf-8')
        #     text['Subject'] = Header('自动化测试报告', 'utf-8')

        smtp = smtplib.SMTP_SSL(smtpserver,465)
        try:
            smtp.login(sender, password)  # 登录的用户名和密码
            smtp.sendmail(sender, receiver, msg.as_string())
            print("发送成功")
        except smtplib.SMTPException  as e:
            print("发送失败")
        finally:
            smtp.quit()

    def send126(self):
        caodate = str(time.strftime(ISOTIMEFORMAT,time.localtime()))
        host = 'smtp.126.com'
        #设置发件服务器地址
        port = 465
        #设置发件服务器端口号。注意，这里有SSL和非SSL两种形式
        sender = 'wangluyan128@126.com'
        #设置发件邮箱，一定要自己注册的邮箱
        pwd = 'luyan128'
        #设置发件邮箱的密码，126邮箱的授权码
        receiver0 = 'wangluyan128@126.com'
        #设置邮件接收人
        #body = '<h1>' + caodate + '</h1><p>zhongfs</p>'
        body  = ('执行测试中……'
                '<p>测试已完成！！</p>'
                '<p>生成报告中……</p>'
                '<p>报告已生成……</p>'
                '<p>报告已邮件发送！！</p>')
        #设置邮件正文，这里是支持HTML的
        msg = MIMEText(body,'html')
        #设置正文为符合邮件格式的HTML内容
        message = MIMEMultipart()
        message['subject'] = caodate+'下载附件通知'
        #设置邮件标题
        message['from'] = sender
        #设置发送人
        message['to'] = receiver0
        #设置接收人
        message.attach(msg)
        filename = 'xfurlwett-' + caodate + '.txt'
        #构造附件1，传送当前目录下的filename文件
        #att1 = MIMEText(open(filename,'rb').read(),'base64','utf-8')
        att1 = MIMEText(open(mail_path,'rb').read(),'html','utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        #这里的filename可以任意写
        #att1["Content-Disposition"]  = 'attachment;filename="' + filename +'"'
        att1["Content-Disposition"]  =  'attachment; filename="TestReport.html"'
        message.attach(att1)
        try:
            s = smtplib.SMTP_SSL(host,port)  #注意！如果是使用SSL端口，这里就要NTY YL smtp__ssl
            s.login(sender,pwd)#登录邮箱
            s.sendmail(sender,receiver0,message.as_string())    #发送邮件
            print('Done.sent email success')
        except smtplib.SMTPException:
            print('Error.send email fail')
#======================查找最新的测试报告==========================

    def new_report(testreport):
        dirs = os.listdir(testreport)
        dirs.sort()
        newreportname = dirs[-1]
        print('The new report name: {0}'.format(newreportname))
        file_new = os.path.join(testreport, newreportname)
        return file_new

if __name__ == '__main__':# 运营此文件来验证写的send_email是否正确
    print(subject)
    #send_email().sendTencent()
   # print("send email ok!!!!!!!!!!")
  #  test_report = "D:\\Python\\Demo\\report"
  #  new_report = send_email().new_report(test_report)
    send_email().send126()