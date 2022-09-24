from flask import Flask
from config import config
from yinglong_server.extensions import db
from flask_cors import CORS
from config import ENVIRONMENT


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    CORS(app)

    # register blueprint
    from .api import api_bp as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    from .auth import auth_bp as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app


app = create_app(ENVIRONMENT)
