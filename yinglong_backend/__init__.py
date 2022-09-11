from celery import Celery

celery_app = Celery('YINGLONG_CELERY')
celery_app.config_from_object('yinglong_backend.celery_config')