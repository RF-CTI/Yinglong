import datetime
import json
from flask import jsonify, request, g
from ..models import db, User
from yinglong_backend.celery_task import sendEmail
from flask_restful import Resource
from config import SITE_DOMAIN


class BasicAPI(Resource):
    CODE = 200
    MESSAGE = 'ok.'

    def __init__(self) -> None:
        super().__init__()

    def setCodeAndMessage(self, code, message):
        self.CODE = code
        self.MESSAGE = message


class RegisterVerificationAPI(BasicAPI):

    def get(self):
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
        return jsonify({'code': self.CODE, 'msg': self.MESSAGE})


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
                    "Yinglong", user.username,
                    "[Yinglong] Please verify your email address.",
                    e_content.format(user.username, user.email, SITE_DOMAIN,
                                     user.verification_code,
                                     str(datetime.date.today())), [user.email],
                    '')
        return jsonify({'code': self.CODE, 'msg': self.MESSAGE})


class LoginAPI(BasicAPI):
    # decorators = [auth.login_required]

    def post(self):
        data = json.loads(request.data)
        email = data.get('email')
        password = data.get('password')
        if email is None or password is None:
            self.setCodeAndMessage(300, "Missing required parameter!")
        elif not self.verify_password(email=email, password=password):
            self.setCodeAndMessage(301, "Username or password is wrong!")
        else:
            user = User.query.filter_by(email=email).first()
            if user is None:
                self.setCodeAndMessage(301, "Email does not exist!")
            else:
                user.is_login = True
                db.session.commit()
        return jsonify({
            "code": self.CODE,
            "msg": self.MESSAGE,
            "id": g.user.id,
            'username': g.user.username
        })

    def verify_password(self, email, password):
        user = User.query.filter_by(email=email).first()
        if not user or not user.verify_password(password):
            return False
        g.user = user
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
        return jsonify({'code': self.CODE, 'msg': self.MESSAGE})
