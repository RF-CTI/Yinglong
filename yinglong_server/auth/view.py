import json
from flask import jsonify, request, current_app
from ..models import db, User, IntelligenceTypeInfo, DataSourceInfo, UserLogInfo
from yinglong_backend.celery_task import sendEmail
from flask_restful import Resource
from config import SITE_DOMAIN
from ..common import LANGERAGE_MAP
from utils.time_utils import getTodayString, getTime
from utils.other_utils import getErrorMessage, generateVerification


class BasicAPI(Resource):
    CODE = 200
    MESSAGE = 'ok.'

    def __init__(self) -> None:
        super().__init__()

    def setCodeAndMessage(self, code, message):
        self.CODE = code
        self.MESSAGE = message
    
    def infoLog(self, user_id, ip_address, content, action):
        current_app.logger.info('ip-{} content-{} action-{}'.format(
            ip_address, content, action))
        log = UserLogInfo(user_id=user_id,ip_address=ip_address,content=content,action=action)
        db.session.add(log)
        db.session.commit()

    def errorLog(self):
        current_app.logger.error(getErrorMessage())


class RegisterVerificationAPI(BasicAPI):

    def post(self):
        data = json.loads(request.data)
        username = data.get('username')
        token = data.get('token')
        if username is None:
            self.setCodeAndMessage(300, "Missing required parameter!")
        else:
            user = User.query.filter_by(username=username).first()
            if user is None:
                self.setCodeAndMessage(301, "Username does not exist!")
            else:
                if user.verification_code != token:
                    self.setCodeAndMessage(302, "Verification failed!")
                else:
                    user.status = 1
                    db.session.commit()
        return jsonify({
            'code': self.CODE,
            'msg': self.MESSAGE,
            'username': username
        })


class RegisterAPI(BasicAPI):

    def post(self):
        data = json.loads(request.data)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        if username is None or password is None or email is None:
            self.setCodeAndMessage(300, "Missing required parameter!")
        elif User.query.filter(User.username == username).first() is not None:
            self.setCodeAndMessage(302, "Username is already used.")
        elif User.query.filter(User.email == email).first() is not None:
            self.setCodeAndMessage(302, "E-mail address is already used.")
        else:
            user = User(username=username, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            with open('template/verification_email.txt', 'r',
                      encoding='utf-8') as f:
                e_content = f.read()
                sendEmail(
                    "应龙情报共享订阅平台", user.username,
                    "[Yinglong] 请验证您的邮箱",
                    e_content.format(user.username, user.email, SITE_DOMAIN,
                                     user.verification_code,
                                     getTodayString()), [user.email],
                    '')
        return jsonify({
            'code': self.CODE,
            'msg': self.MESSAGE,
            'username': username
        })


class LoginAPI(BasicAPI):
    # decorators = [auth.login_required]

    def post(self):
        data = json.loads(request.data)
        email = data.get('email')
        password = data.get('password')
        if email is None or password is None:
            self.setCodeAndMessage(300, "Missing required parameter!")
        else:
            user = User.query.filter_by(email=email).first()
            if user is None:
                self.setCodeAndMessage(301, "Email does not exist!")
            elif not self.verify_password(email=email, password=password):
                self.setCodeAndMessage(301, "E-mail or password is wrong!")
            else:
                user.is_login = True
                user.last_login = int(getTime())
                self.infoLog(user_id=user.id,ip_address=request.headers['X-Forwarded-For'],content='login',action=1)
                db.session.commit()
        return jsonify({
            "code": self.CODE,
            "msg": self.MESSAGE,
            "id": user.id,
            'username': user.username
        } if self.CODE == 200 else {
            'code': self.CODE,
            'msg': self.MESSAGE
        })

    def verify_password(self, email, password):
        user = User.query.filter_by(email=email).first()
        if not user or not user.verify_password(password):
            return False
        return True


class LogoutAPI(BasicAPI):

    def post(self):
        data = json.loads(request.data)
        username = data.get('username')
        if username is None:
            self.setCodeAndMessage(300, "Missing required parameter!")
        else:
            user = User.query.filter_by(username=username).first()
            if user is None:
                self.setCodeAndMessage(301, "Username does not exist!")
            else:
                user.is_login = False
                self.infoLog(user_id=user.id,ip_address=request.headers['X-Forwarded-For'],content='logout',action=2)
                db.session.commit()
        return jsonify({'code': self.CODE, 'msg': self.MESSAGE})


class ForgetPasswd(BasicAPI):

    def post(self):
        data = json.loads(request.data)
        email = data.get('email')
        if email is None:
            self.setCodeAndMessage(300, "Missing required parameter!")
        else:
            user = User.query.filter_by(email=email).first()
            if user is None:
                self.setCodeAndMessage(301, "E-mail does not exist!")
            else:
                with open('template/forgetpswd_email.txt', 'r', encoding='utf-8') as f:
                    e_content = f.read()
                    user.verification_code = generateVerification()
                    sendEmail(
                        "应龙情报共享订阅平台", user.username,
                        "[Yinglong] 您的账户正在修改密码",
                        e_content.format(user.username, SITE_DOMAIN,
                                        user.verification_code,
                                        getTodayString()), [user.email],
                        '')
                    db.session.commit()
        return jsonify({'code': self.CODE, 'msg': self.MESSAGE})


class ResetPasswd(BasicAPI):

    def post(self):
        data = json.loads(request.data)
        code = data.get('verification_code')
        pswd = data.get('passwd')
        if code is None or pswd is None:
            self.setCodeAndMessage(300, "Missing required parameter!")
        else:
            user = User.query.filter_by(verification_code=code).first()
            if user is None:
                self.setCodeAndMessage(301, "Verification code does not exist!")
            else:
                user.password = user.hash_password(pswd)
                db.session.commit()
        return jsonify({'code': self.CODE, 'msg': self.MESSAGE})


class UserInfoAPI(BasicAPI):

    def post(self):
        data = json.loads(request.data)
        username = data.get('username')
        if username is None:
            self.setCodeAndMessage(300, "Missing required parameter!")
        else:
            user = User.query.filter_by(username=username).first()
            if user is None:
                self.setCodeAndMessage(301, "Username does not exist!")
            else:
                return jsonify(user.to_json())
        return jsonify({'code': self.CODE, 'msg': self.MESSAGE})


class SubscribeAPI(BasicAPI):

    def post(self):
        data = json.loads(request.data)
        username = data.get('username')
        sc_id = data.get('id')
        if username and sc_id:
            user = db.session.query(User).filter(
                User.username == username).first()
            if user.subscribe_content is None or user.subscribe_content == '':
                ct = []
            else:
                ct = json.loads(user.subscribe_content)['content']
            source = DataSourceInfo.query.filter_by(id=sc_id).first()
            if sc_id in ct:
                ct.remove(sc_id)
                self.infoLog(user_id=user.id,ip_address=request.headers['X-Forwarded-For'],content=source.name,action=4)
            else:
                self.infoLog(user_id=user.id,ip_address=request.headers['X-Forwarded-For'],content=source.name,action=3)
                ct.append(sc_id)
            user.subscribe_content = json.dumps({"content": ct})
            db.session.commit()
            return jsonify({'code': 200, 'msg': 'ok'})
        else:
            return jsonify({'code': 400, 'msg': 'faild'})


class GetUserSubscribeAPI(BasicAPI):

    def post(self):
        data = json.loads(request.data)
        username = data.get('username')
        if username is None:
            self.setCodeAndMessage(300, "Missing required parameter!")
        else:
            user = User.query.filter_by(username=username).first()
            if user is None:
                self.setCodeAndMessage(301, "Username does not exist!")
            else:
                itypes = IntelligenceTypeInfo.query.all()
                res = {}
                sub_content = json.loads(user.subscribe_content)['content']
                for itype in itypes:
                    sources = DataSourceInfo.query.filter_by(
                        intelligence_type=itype.id).all()
                    li = []
                    for source in sources:
                        data = source.to_json()
                        data['subscribe'] = True if str(
                            data['id']) in sub_content else False
                        li.append(data)
                    res[itype.name] = {
                        'data': li,
                        'name_zh': LANGERAGE_MAP.get(itype.name)
                    }
                return jsonify({
                    'code': self.CODE,
                    'msg': self.MESSAGE,
                    'result': res
                })
        return jsonify({'code': self.CODE, 'msg': self.MESSAGE})


class GetUserTokenAPI(BasicAPI):

    def get(self):
        username = request.args.get('username')
        if username is None:
            self.setCodeAndMessage(300, "Missing required parameter!")
        else:
            user = User.query.filter_by(username=username).first()
            if user is None:
                self.setCodeAndMessage(301, "Username does not exist!")
            else:
                return jsonify({
                    'code': self.CODE,
                    'msg': self.MESSAGE,
                    'token': user.token
                })
        return jsonify({'code': self.CODE, 'msg': self.MESSAGE})


class DownloadSourceAPI(BasicAPI):

    def post(self):
        username = request.args.get('username')
        hashCode = request.args.get('hash')
        if username is None:
            self.setCodeAndMessage(300, "Missing required parameter!")
        else:
            user = User.query.filter_by(username=username).first()
            if user is None:
                self.setCodeAndMessage(301, "Username does not exist!")
            else:
                self.infoLog(user_id=user.id,ip_address=request.headers['X-Forwarded-For'],content=hashCode,action=5)
                db.session.commit()
        return jsonify({'code': self.CODE, 'msg': self.MESSAGE})
