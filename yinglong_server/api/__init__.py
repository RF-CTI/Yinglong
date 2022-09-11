from flask import Blueprint
from flask_restful import Api
from .service import PhishingAPI, BotnetAPI

api_bp = Blueprint('api_bp', __name__)
api = Api()
api.init_app(api_bp)

api.add_resource(PhishingAPI, '/phishing/')
api.add_resource(BotnetAPI, '/botnet/')