from celery import Celery
from config import APP_NAME

celery_app = Celery(APP_NAME)
celery_app.config_from_object('celery_task.celery_config')