# -*- coding:utf8 -*-
__author__ = "杨果"
# TODO(yang.guo@dr-elephant.com):这是邮件发送的代码

import os
import time
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.text import MIMEText
import smtplib
from common.Log import MyLog
from common import Config

upPath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# print(upPath)
resultPath = os.path.join(upPath, "TestResult\\result\\result.html")
# print(resultPath)

class SendEmail:

    @staticmethod
    def send_mail():
        # 读取Emial配置文件
        config = Config.Config()

        # email_from = "yang.guo@dr-elephant.com"     # 邮件发送人
        email_from = config.get_email("mail_sender")
        # email_to = "yang.guo@dr-elephant.com"       # 邮件收件人
        email_to = config.get_email("mail_receiver")
        email_sub = "接口自动化报告" + " " + str(time.strftime("%Y/%m/%d", time.localtime()))
        # print(email_sub)

        message = MIMEMultipart("alternative")
        htmlfile = open(resultPath, "r", encoding="utf-8").read()
        message["From"] = Header(email_from, "utf-8")
        message["To"] = Header(email_to, "utf-8")
        message["Subject"] = Header(email_sub, "utf-8")

        # 邮件主体内容
        # mail_body = ("hi,all:" + "<br><br>" +
        #              "&nbsp;&nbsp;测试中，请勿回复" + "<br><br>")
        # 邮件正文内容  "plain","html"
        # message.attach(MIMEText(mail_body, "html", "utf-8"))

        message.attach(MIMEText(htmlfile, "html", "utf-8"))
        # 构造附件，传送当前目录下的文件
        att = MIMEText(open(resultPath, "rb").read(), "base64", "utf-8")
        att["Content-Type"] = "application/octet-stream"
        # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        att["Content-Disposition"] = "attachment; filename=\"auto_result_report.html\""
        message.attach(att)

        log = MyLog.get_log()
        logger = log.get_logger()

        try:
            host = config.get_email("mail_host")
            port = config.get_email("mail_port")
            user = config.get_email("mail_user")
            password = config.get_email("mail_password")

            # conn = smtplib.SMTP('smtp.dr-elephant.com', 587)
            conn = smtplib.SMTP(host, port)
            conn.ehlo()
            conn.starttls()
            conn.ehlo()
            # conn.login("yang.guo@dx.com", "Dx123456")
            conn.login(user, password)
            conn.sendmail(email_from, email_to, message.as_string())
            logger.info("邮件已发送成功!")
            conn.close()
        except smtplib.SMTPException as e:
            logger.info("Error:邮件发送失败:%s" % e)

if __name__ == "__main__":
    sendEmail = SendEmail()
    sendEmail.send_mail()


