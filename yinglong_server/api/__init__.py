from flask import Blueprint
from flask_restful import Api
from .service import PhishingAPI, BotnetAPI, VerificationAPI
from .views import DaliyReportAPI, DataRecordAPI, GetDataAPI,SubscribeAPI

api_bp = Blueprint('api_bp', __name__)
api = Api()
api.init_app(api_bp)

api.add_resource(PhishingAPI, '/phishing/')
api.add_resource(BotnetAPI, '/botnet/')
api.add_resource(VerificationAPI, '/verification/')
api.add_resource(DaliyReportAPI, '/daliyreport/')
api.add_resource(DataRecordAPI, '/datarecord/')
api.add_resource(GetDataAPI, '/getdata/')
api.add_resource(SubscribeAPI, '/subscribe/')
