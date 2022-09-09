import uuid
from hashlib import md5
from flask_sqlalchemy import SQLAlchemy
from flask_app import flask_app


db = SQLAlchemy(flask_app)


class User(db.Model):
    id = db.Column('user_id', db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(64))
    uid = db.Column(db.String(64))
    is_login = db.Column(db.Boolean, default=False)
    subscribe_type = db.Column(db.Integer, default=0)
    subscribe_content = db.Column(db.String(256), default='')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.uid = md5(str(uuid.uuid1()).encode('utf-8')).hexdigest()
        self.is_login = False
        self.subscribe_type = 0
        self.subscribe_content = ''

    def __repr__(self):
        return '<User %r>' % self.username


if __name__ == '__main__':
    db.create_all()
