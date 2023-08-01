from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import logging
class Email():
    def __init__(self,content,resportpath,Email_config):#初始化邮箱
        self.smtpHost = Email_config['HOST_SERVER'] #服务器
        self.port = 465 #端口
        self.myMail   = Email_config['FROM'] #发送邮箱
        self.userName = Email_config['emailuser'] #邮箱用户名
        self.passWord = Email_config['emailpw']#邮箱密码
        self.bossMail = Email_config['TO']#接收方邮箱
        self.Subject  = Email_config['emailtatle']#邮箱标题
        self.login(content,resportpath)
    # 登录邮箱
    def login(self,content,resportpath):
        """
        :param fail_list: 错误用例列表
        :param timelist: 时间列表
        :param versionlist: 版本列表
        :param resportpath: 报告路径
        :return:
        """
        logging.basicConfig(filename='log_record.txt',
                            level=logging.DEBUG, filemode='w', format='[%(asctime)s] [%(levelname)s] >>>  %(message)s',
                            datefmt='%Y-%m-%d %I:%M:%S')
        '''建立服务器连接'''
        mailLink = smtplib.SMTP_SSL(self.smtpHost,self.port)
        mailLink.set_debuglevel(0)
        m = MIMEMultipart()
        '''登录邮箱'''
        mailLink.login(self.userName,self.passWord)
        '''html报告'''
        content= content
        '''写入内容'''
        msg = MIMEText(content, 'html', 'utf-8')
        '''邮件标题标题'''
        m['Subject'] = Header(self.Subject, 'utf-8')
        '''接受人'''
        m['from'] = self.userName
        '''写入报告附件'''
        exc = MIMEApplication(open(resportpath, 'rb').read())
        exc.add_header('Content-Disposition', 'attachment', filename=resportpath)
        m.attach(exc)
        m.attach(msg)
        '''发送报告'''
        mailLink.sendmail(self.myMail, self.bossMail.split(','), m.as_string())
        quit()

