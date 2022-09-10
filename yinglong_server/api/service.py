import time
from ..models import PhishingInfo, BotnetInfo
from flask_restful import Resource
from flask import jsonify


class PhishingAPI(Resource):

    def post(self):
        t = int(time.mktime((2022, 9, 8, 0, 0, 0, 0, 0, 0)))
        phishing = PhishingInfo.query.filter(
            PhishingInfo.create_time > t).all()
        return jsonify({
            'result': [{
                'ip': item.ip,
                'domain': item.domain,
                'create_time': item.create_time
            } for item in phishing]
        })


class BotnetAPI(Resource):

    def post(self):
        t = int(time.mktime((2022, 9, 8, 0, 0, 0, 0, 0, 0)))
        botnet = BotnetInfo.query.filter(BotnetInfo.last_online > t).all()
        return jsonify({
            'result': [{
                'ip': item.ip,
                'hostname': item.hostname,
                'port': item.port,
                'country': item.country,
                'as_name': item.as_name,
                'as_number': item.as_number,
                'status': item.status,
                'first_seen': item.first_seen,
                'last_online': item.last_online,
                'malware': item.malware
            } for item in botnet]
        })
