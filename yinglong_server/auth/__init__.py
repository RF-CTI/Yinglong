from flask import Blueprint
from flask_restful import Api
from .view import RegisterAPI, LoginAPI, RegisterVerificationAPI, UserInfoAPI, GetUserSubscribeAPI, GetUserToken

auth_bp = Blueprint('auth_bp', __name__)
auth = Api()
auth.init_app(auth_bp)

auth.add_resource(RegisterAPI, '/register/')
auth.add_resource(LoginAPI, '/login/')
auth.add_resource(RegisterVerificationAPI, '/verification/')
auth.add_resource(UserInfoAPI, '/userinfo/')
auth.add_resource(GetUserSubscribeAPI, '/getusersubscribe/')
auth.add_resource(GetUserToken, '/getusertoken/')
