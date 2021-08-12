
import smtplib
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import FileSystemLoader, Environment

from core.config import *


class EmailPoster(object):
    """
    邮件发送基础类
    """

    @staticmethod
    def get_template():
        loader = FileSystemLoader('templates')
        env = Environment(loader=loader)
        template = env.get_template("default.html")
        return template

    def send(self, data: dict):
        payload = data.get("payload", {})
        if payload:
            template = self.get_template()
            content = template.render(payload=payload)
        elif data.get("body"):
            content = data.get('body', '默认内容')
        else:
            return
        subject = data.get('subject', '')
        mail_to = data.get('to', [])
        mail_from = data.get('from', MAIL_ADDRESS)
        self._send(content, subject, mail_from, mail_to)

    @staticmethod
    def _send(content: str, subject: str, mail_from: str, mail_to: list):
        msg_root = MIMEMultipart('related')
        msg_text = MIMEText(content, 'html', 'utf-8')
        msg_root.attach(msg_text)
        msg_root['Subject'] = subject
        msg_root['From'] = mail_from
        msg_root['To'] = ";".join(mail_to)

        try:
            stp = smtplib.SMTP_SSL(MAIL_HOST, MAIL_PORT)
            # stp.set_debuglevel(1)
            stp.ehlo()
            stp.login(MAIL_USER, MAIL_PASSWORD)
            stp.sendmail(MAIL_ADDRESS, mail_to, msg_root.as_string())
            stp.quit()
        except Exception as e:
            print(traceback.format_exc(e))

