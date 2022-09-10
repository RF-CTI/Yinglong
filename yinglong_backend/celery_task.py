from sendemail import sendEmail
from . import celery_app

@celery_app.task
def sendEmailTask(title:str,content:str,receivers:list,attach:str or None):
    sendEmail(title,content,receivers,attach)

@celery_app.task
def test():
    with open('tmp','a+',encoding='utf-8') as f:
        f.write('hello')