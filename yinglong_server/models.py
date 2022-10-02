import json
from .extensions import db
from passlib.apps import custom_app_context as pwd_context
from utils.time_utils import timestamp2Datastring, getTimeInt
from utils.other_utils import generateMD5Code


class User(db.Model):
    __tablename__ = 'user'
    STATUS_MAP = {0: "unverified", 1: "normal", 2: "abandon"}
    id = db.Column('user_id', db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(64))
    token = db.Column(db.String(64))
    is_login = db.Column(db.Boolean, default=False)
    subscribe_type = db.Column(db.Integer, default=0)
    subscribe_content = db.Column(db.String(256), default='')
    verification_code = db.Column(db.String(256))
    status = db.Column(db.Integer, default=0)
    create_time = db.Column(db.Integer, default=0)
    last_login = db.Column(db.Integer, default=0)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = self.hash_password(password)
        self.token = generateMD5Code(ctype=1)
        self.is_login = False
        self.subscribe_type = None
        self.subscribe_content = json.dumps({'content': []})
        self.verification_code = generateMD5Code(ctype=4)
        self.status = 0
        self.create_time = getTimeInt()
        self.last_login = 0

    def __repr__(self):
        return '<User %r>' % self.username

    def hash_password(self, password):
        return pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def getStatus(self):
        return (self.status, self.STATUS_MAP.get(self.status, 'unverified'))

    def to_json(self):
        res = {}
        for item in self.__dict__.keys():
            if item in ['username', 'email', 'token']:
                res[item] = self.__dict__[item]
        return res


class PhishingInfo(db.Model):
    __tablename__ = 'phishing_info'
    id = db.Column('phishing_id',
                   db.Integer,
                   primary_key=True,
                   autoincrement=True)
    ip = db.Column(db.String(64))
    domain = db.Column(db.String(128))
    timestamp = db.Column(db.Integer)
    source = db.Column(db.ForeignKey('data_source.source_id'))

    def __init__(self, ip, domain, timestamp, source) -> None:
        super().__init__()
        self.ip = ip
        self.domain = domain
        self.timestamp = timestamp
        self.source = source

    def __repr__(self) -> str:
        return "<PhishingInfo: ip-%r, domain-%r>" % (self.ip, self.domain)

    def to_json_simple(self):
        res = {}
        for item in self.__dict__.keys():
            if item in ['ip', 'timestamp', 'domain']:
                res[item] = self.__dict__[item]
        return res

    def to_json(self):
        res = {}
        for item in self.__dict__.keys():
            if item != '_sa_instance_state':
                res[item] = self.__dict__[item]
        return res


class C2Info(db.Model):
    __tablename__ = 'c2_info'
    id = db.Column('c2_id', db.Integer, primary_key=True, autoincrement=True)

    domain = db.Column(db.String(256))
    ioc = db.Column(db.String(256))
    uri_path = db.Column(db.String(256))
    timestamp = db.Column(db.Integer)
    source = db.Column(db.ForeignKey('data_source.source_id'))

    def __init__(self, domain, ioc, uri_path, timestamp, source) -> None:
        super().__init__()
        self.domain = domain
        self.ioc = ioc
        self.uri_path = uri_path
        self.timestamp = timestamp
        self.source = source

    def __repr__(self) -> str:
        return "<C2Info: ioc-%r, domain-%r, uri_path-%r>" % (
            self.ioc, self.domain, self.uri_path)

    def to_json_simple(self):
        res = {}
        for item in self.__dict__.keys():
            if item in ['ioc', 'domain', 'timestamp']:
                res[item] = self.__dict__[item]
        return res

    def to_json(self):
        res = {}
        for item in self.__dict__.keys():
            if item != '_sa_instance_state':
                res[item] = self.__dict__[item]
        return res


class BotnetInfo(db.Model):
    __tablename__ = 'botnet_info'
    id = db.Column('botnet_id',
                   db.Integer,
                   primary_key=True,
                   autoincrement=True)
    ip_address = db.Column(db.String(64))
    port = db.Column(db.Integer)
    hostname = db.Column(db.String(128))
    country = db.Column(db.String(8))
    as_number = db.Column(db.Integer)
    as_name = db.Column(db.String(256))
    status = db.Column(db.String(16))
    first_seen = db.Column(db.Integer)
    timestamp = db.Column(db.Integer)
    malware = db.Column(db.String(64))
    source = db.Column(db.ForeignKey('data_source.source_id'))

    def __init__(self, ip_address, port, hostname, status, country, as_number,
                 as_name, first_seen, timestamp, malware, source) -> None:
        super().__init__()
        self.ip_address = ip_address
        self.port = port
        self.country = country
        self.as_name = as_name
        self.as_number = as_number
        self.hostname = hostname
        self.status = status
        self.first_seen = first_seen
        self.timestamp = timestamp
        self.malware = malware
        self.source = source

    def __repr__(self) -> str:
        return "<BotnetInfo: name-%r, ip-%r, port-%r>" % (self.as_name,
                                                          self.ip, self.port)

    def to_json(self):
        res = {}
        for item in self.__dict__.keys():
            if item != '_sa_instance_state':
                res[item] = self.__dict__[item]
        return res

    def to_json_simple(self):
        res = {}
        for item in self.__dict__.keys():
            if item in ['ip_address', 'port', 'status', 'malware']:
                res[item] = self.__dict__[item]
        return res


class IntelligenceTypeInfo(db.Model):
    __tablename__ = 'intelligence_type'
    id = db.Column('type_id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32))

    def to_json(self):
        res = {}
        for item in self.__dict__.keys():
            if item != '_sa_instance_state':
                res[item] = self.__dict__[item]
        return res


class DataRecordInfo(db.Model):
    __tablename__ = 'data_record'
    id = db.Column('record_id',
                   db.Integer,
                   primary_key=True,
                   autoincrement=True)
    begin_time = db.Column(db.Integer)
    end_time = db.Column(db.Integer)
    size = db.Column(db.Integer)
    url = db.Column(db.String(256))
    sha_code = db.Column(db.String(256))
    intelligence_type = db.Column(db.ForeignKey('intelligence_type.type_id'))

    def to_json(self):
        res = {}
        for item in self.__dict__.keys():
            if item != '_sa_instance_state':
                if item in ['begin_time', 'end_time']:
                    res[item] = timestamp2Datastring(self.__dict__[item])
                elif item == 'size':
                    res[item] = str(
                        self.__dict__[item]
                    ) + 'B' if self.__dict__[item] < 1024 else str(
                        self.__dict__[item] // 1024) + 'KB'
                else:
                    res[item] = self.__dict__[item]
        return res


class DataSourceInfo(db.Model):
    __tablename__ = 'data_source'
    id = db.Column('source_id',
                   db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(32))
    intelligence_type = db.Column(db.ForeignKey('intelligence_type.type_id'))

    def to_json(self):
        res = {}
        for item in self.__dict__.keys():
            if item != '_sa_instance_state':
                res[item] = self.__dict__[item]
        return res


class APILogInfo(db.Model):
    __tablename__ = 'api_log'
    id = db.Column('log_id', db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.Integer)
    ip_address = db.Column(db.String(128))
    url = db.Column(db.String(256))
    token = db.Column(db.String(128))
    parameters = db.Column(db.String(512))
    result = db.Column(db.String(512))

    def __init__(self, token, url, ip_address, parameters, result) -> None:
        super().__init__()
        self.ip_address = ip_address
        self.token = token
        self.url = url
        self.parameters = parameters
        self.result = result
        self.create_time = getTimeInt()

    def to_json(self):
        res = {}
        for item in self.__dict__.keys():
            if item != '_sa_instance_state':
                res[item] = self.__dict__[item]
        return res


class UserLogInfo(db.Model):
    __tablename__ = 'user_log'
    action_choices = {
        0: '',
        1: '登录',
        2: '退出登录',
        3: '订阅',
        4: '取消订阅',
        5: '下载'
    }
    id = db.Column('log_id', db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.Integer)
    content = db.Column(db.String(512))
    ip_address = db.Column(db.String(128))
    user_id = db.Column(db.ForeignKey('user.user_id'))
    action = db.Column(db.Integer)

    def __init__(self, user_id, ip_address, content, action) -> None:
        super().__init__()
        self.action = action
        self.user_id = user_id
        self.ip_address = ip_address
        self.content = content
        self.create_time = getTimeInt()

    def to_json(self):
        res = {}
        for item in self.__dict__.keys():
            if item != '_sa_instance_state':
                res[item] = self.__dict__[item]
            elif item == 'action':
                res[item] = self.action_choices[self.__dict__[item]]
        return res


if __name__ == '__main__':
    db.create_all()
