from flask import Flask
from config import config
from yinglong_server.extensions import bootstrap, db, login_manager
from config import ENVIRONMENT
from .auth.view import LoginView, RegisterView


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # register blueprint
    from .main import main_bp
    app.register_blueprint(main_bp)

    from .auth import auth_bp as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .api import api_bp as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app


app = create_app(ENVIRONMENT)
app.add_url_rule('/login/', view_func=LoginView.as_view('login'))
app.add_url_rule('/register/', view_func=RegisterView.as_view('register'))
