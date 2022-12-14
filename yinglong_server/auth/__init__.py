from flask import Blueprint
from flask_restful import Api
from .view import (RegisterAPI, LoginAPI, RegisterVerificationAPI,
                    UserInfoAPI, GetUserSubscribeAPI, GetUserTokenAPI,
                    SubscribeAPI,DownloadSourceAPI,ResetPasswd,ForgetPasswd)

auth_bp = Blueprint('auth_bp', __name__)
auth = Api()
auth.init_app(auth_bp)

auth.add_resource(RegisterAPI, '/register/')
auth.add_resource(LoginAPI, '/login/')
auth.add_resource(RegisterVerificationAPI, '/verification/')
auth.add_resource(ForgetPasswd, '/forgetpswd/')
auth.add_resource(ResetPasswd, '/resetpswd/')
auth.add_resource(UserInfoAPI, '/userinfo/')
auth.add_resource(GetUserSubscribeAPI, '/getusersubscribe/')
auth.add_resource(GetUserTokenAPI, '/getusertoken/')
auth.add_resource(SubscribeAPI, '/subscribe/')
auth.add_resource(DownloadSourceAPI, '/downloadsource/')
