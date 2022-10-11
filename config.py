import os
from urllib.parse import quote_plus as urlquote

# Project Setting
SITE_DOMAIN = os.getenv('YINGLONG_SITE_DOMAIN','YOUR_SITE_DOMAIN')
ENVIRONMENT = os.getenv('YINGLONG_ENVIRONMENT','YOUR_ENVIRONMENT') # development, testing, product
TMP_FILE_DIR = './tmp'
GIT_ACCESS_TOKEN = os.getenv('YINGLONG_GIT_ACCESS_TOKEN','YOUR_GIT_ACCESS_TOKEN')

# E-mail Setting
SEND_EMAIL_ADDRESS = os.getenv('YINGLONG_SEND_EMAIL_ADDRESS',"YOUR_SEND_EMAIL_ADDRESS")
SEND_EMAIL_PASSWORD = os.getenv('YINGLONG_SEND_EMAIL_PASSWORD',"YOUR_SEND_EMAIL_PASSWORD")
SEND_EMAIL_SMTP = os.getenv('YINGLONG_SEND_EMAIL_SMTP',"YOUR_SEND_EMAIL_SMTP")

# Database Setting
MYSQL_USERNAME = os.getenv('YINGLONG_MYSQL_USERNAME','YOUR_MYSQL_USERNAME')
MYSQL_PASSWORD = os.getenv('YINGLONG_MYSQL_PASSWORD','YOUR_MYSQL_PASSWORD')
MYSQL_TEST_DATABASE = os.getenv('YINGLONG_MYSQL_TEST_DATABASE','YOUR_MYSQL_TEST_DATABASE')
MYSQL_PRO_DATABASE = os.getenv('YINGLONG_MYSQL_PRO_DATABASE','YOUR_MYSQL_PRO_DATABASE')
MYSQL_DATABASE = os.getenv('YINGLONG_MYSQL_TEST_DATABASE','YOUR_MYSQL_DATABASE')
DB_URL =  'mysql+pymysql://{}:{}@{}'.format(MYSQL_USERNAME,urlquote(MYSQL_PASSWORD),MYSQL_DATABASE)
DB_PRO_URL =  'mysql+pymysql://{}:{}@{}'.format(MYSQL_USERNAME,urlquote(MYSQL_PASSWORD),MYSQL_PRO_DATABASE)
DB_TEST_URL = 'mysql+pymysql://{}:{}@{}'.format(MYSQL_USERNAME,urlquote(MYSQL_PASSWORD),MYSQL_TEST_DATABASE)
REDIS_URL = os.getenv('YINGLONG_REDIS_URL','redis://localhost:6379')

# Flask Setting
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# 基本配置类
class BaseConfig(object):
    SECRET_KEY = os.getenv('YINGLONG_SECRET_KEY', 'Yinglong Project copyright Redflag Organization')
    ITEMS_PER_PAGE = 10
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LOG_PATH = os.path.join(BASE_DIR, 'logs')
    LOG_PATH_GLOBAL = os.path.join(LOG_PATH, 'global.log')
    LOG_PATH_ERROR = os.path.join(LOG_PATH, 'error.log')
    LOG_PATH_INFO = os.path.join(LOG_PATH, 'info.log')
    LOG_FILE_MAX_BYTES = 100 * 1024 * 1024
    # 轮转数量是 10 个
    LOG_FILE_BACKUP_COUNT = 10

    @classmethod
    def init_app(cls, app):
        import logging
        from logging.handlers import RotatingFileHandler

        logFormatStr = '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
        logging.basicConfig(format = logFormatStr, filename = cls.LOG_PATH_GLOBAL, level=logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s '
            '%(pathname)s %(lineno)s %(message)s')
 
        # FileHandler Info
        file_handler_info = RotatingFileHandler(filename=cls.LOG_PATH_INFO)
        file_handler_info.setFormatter(formatter)
        file_handler_info.setLevel(logging.INFO)
        app.logger.addHandler(file_handler_info)
 
        # FileHandler Error
        file_handler_error = RotatingFileHandler(filename=cls.LOG_PATH_ERROR)
        file_handler_error.setFormatter(formatter)
        file_handler_error.setLevel(logging.ERROR)
        app.logger.addHandler(file_handler_error)


#  开发环境
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL', DB_TEST_URL)


# 测试环境
class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', DB_TEST_URL)
    WTF_CSRF_ENABLED = False


# 生产环境
class ProductionConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', DB_PRO_URL)
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'product': ProductionConfig,
    'default': DevelopmentConfig
}
