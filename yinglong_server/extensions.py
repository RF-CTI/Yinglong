from flask_bootstrap import Bootstrap4
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


bootstrap = Bootstrap4()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth_bp.login'
