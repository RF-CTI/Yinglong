import uuid
from hashlib import md5
from .extensions import db


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
        self.subscribe_type = None
        self.subscribe_content = None

    def __repr__(self):
        return '<User %r>' % self.username


class PhishingInfo(db.Model):
    id = db.Column('user_id', db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(64))
    domain = db.Column(db.String(128))
    create_time = db.Column(db.Integer)

    def __init__(self, ip, domain, create_time) -> None:
        super().__init__()
        self.ip = ip
        self.domain = domain
        self.create_time = create_time

    def __repr__(self) -> str:
        return "<PhishingInfo: ip-%r, domain-%r>" % (self.ip, self.domain)


class BotnetInfo(db.Model):
    id = db.Column('user_id', db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(64))
    port = db.Column(db.Integer)
    hostname = db.Column(db.String(128))
    country = db.Column(db.String(8))
    as_number = db.Column(db.Integer)
    as_name = db.Column(db.String(256))
    status = db.Column(db.String(16))
    first_seen = db.Column(db.Integer)
    last_online = db.Column(db.Integer)
    malware = db.Column(db.String(64))

    def __init__(self, ip, port, hostname, status, country, as_number, as_name,
                 first_seen, last_online, malware) -> None:
        super().__init__()
        self.ip = ip
        self.port = port
        self.country = country
        self.as_name = as_name
        self.as_number = as_number
        self.hostname = hostname
        self.status = status
        self.first_seen = first_seen
        self.last_online = last_online
        self.malware = malware

    def __repr__(self) -> str:
        return "<BotnetInfo: name-%r, ip-%r, port-%r>" % (self.as_name,
                                                          self.ip, self.port)


if __name__ == '__main__':
    db.create_all()
