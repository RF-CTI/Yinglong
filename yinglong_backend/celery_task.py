import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from config import SEND_EMAIL_ADDRESS, SEND_EMAIL_PASSWORD, SEND_EMAIL_SMTP
from . import celery_app

@celery_app.task
def sendEmail(from_: str, to_: str, title: str, content: str, receivers: list, attach: str) -> None:
    """Send e-mail to managers when the task is finished.

    Args:
        task (str): Task target.
        num (str): The count of new items get from the task.
    """
    sender = SEND_EMAIL_ADDRESS

    message = MIMEMultipart()
    text = MIMEText(content, 'plain', 'utf-8')
    message['From'] = Header(from_, 'utf-8')  # 发送者
    message['To'] = Header(to_, 'utf-8')  # 接收者
    message.attach(text)

    if attach != '':
        attachfile = MIMEText(open(attach, 'rb').read(), 'base64', 'utf-8')
        attachfile["Content-Type"] = 'application/octet-stream'
        attachfile["Content-Disposition"] = 'attachment; filename="{}"'.format(
            attach)
        message.attach(attachfile)

    subject = title
    message['Subject'] = Header(subject, 'utf-8')

    smtpObj = smtplib.SMTP()
    smtpObj.connect(SEND_EMAIL_SMTP, 25)
    smtpObj.login(sender, SEND_EMAIL_PASSWORD)
    smtpObj.sendmail(sender, receivers, message.as_string())
    smtpObj.quit()

@celery_app.task
def test():
    with open('tmp','a+',encoding='utf-8') as f:
        f.write('hello')