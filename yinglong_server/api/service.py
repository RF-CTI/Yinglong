import time
import datetime
import redis
import json
import uuid
from hashlib import md5
from ..models import PhishingInfo, BotnetInfo
from flask_restful import Resource
from flask import jsonify, request

redis_pool = redis.ConnectionPool(host='127.0.0.1',
                                  port=6379,
                                  decode_responses=True)


class VerificationAPI(Resource):

    def post(self):
        token = str(request.args.get('token'))
        if token:
            r = redis.Redis(connection_pool=redis_pool)
            if r.sismember('yonglong_tokens', token):
                secret = md5('-'.join([token, str(uuid.uuid1())
                                       ]).encode('utf-8')).hexdigest()
                r.hset('yinglong_authentication', token, secret)
                return jsonify({'code': 200, 'secret': secret})
            else:
                return jsonify({
                    'code': 301,
                    "msg": 'Incorrect token entered.'
                })
        else:
            return jsonify({
                'code': 300,
                "msg": 'There is no "token" parameter.'
            })


class PhishingAPI(Resource):

    def post(self):
        today = datetime.date.today()
        r = redis.Redis(connection_pool=redis_pool)
        print(request.data)
        data = json.loads(request.data)
        token = data.get('token')
        # date = data.get('date')
        # quantity = data.get('quantity')
        timestamp = data.get('timestamp')
        signature = data.get('signature')
        secret = r.hget('yinglong_authentication', token)
        if self.verification(token=token,
                             secert=secret,
                             timestamp=timestamp,
                             signature=signature):
            return jsonify({'code': 200})
            if r.hget('yinglong_phishing', str(today)) is None:
                t = time.mktime(time.strptime(str(today), '%Y-%m-%d'))
                phishing = PhishingInfo.query.filter(
                    PhishingInfo.timestamp > t).all()
                result = [{
                    'ip': item.ip,
                    'domain': item.domain,
                    'timestamp': item.timestamp
                } for item in phishing]
                r.hset('yinglong_phishing', str(today), str(result))
            else:
                result = eval(r.hget('yinglong_phishing', str(today)))
            return jsonify({
                'result': result,
                'timestamp': int(time.time()),
                'code': 200
            })
        else:
            return jsonify({'code': 300, 'msg': 'Verification failed!'})

    def verification(self, token, secert, timestamp, signature):
        if not token or not secert or not timestamp or not signature:
            return False
        elif md5('-'.join([token, secert, str(timestamp)
                           ]).encode('utf-8')).hexdigest() == signature:
            return True
        else:
            return False


class BotnetAPI(Resource):

    def post(self):
        today = datetime.date.today()
        t = time.mktime(time.strptime(str(today), '%Y-%m-%d'))
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
