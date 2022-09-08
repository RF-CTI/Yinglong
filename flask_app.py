from flask import Flask
from config import APP_NAME, DB_URL

flask_app = Flask(APP_NAME)
flask_app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
