import time
import datetime
import redis
import json
import uuid
from hashlib import md5
from ..models import PhishingInfo, BotnetInfo
from flask_restful import Resource
from flask import jsonify, request
from sqlalchemy import and_
from sqlalchemy.sql import func
from utils import (commonQueryOrder, commonQueryCompare, getNoNoneItem,
                   getTodayTimestamp)

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


class BasicAPI(Resource):
    VALIDITY = ''
    MESSAGE = 'Success.'
    CODE = 200

    def __init__(self) -> None:
        super().__init__()

    def verification(self, token, secert, timestamp, signature) -> bool:
        if not token or not secert or not timestamp or not signature:
            self.setCodeAndMessage(300, 'Missing required parameter!')
            return False
        elif md5('-'.join([token, secert, str(timestamp)
                           ]).encode('utf-8')).hexdigest() == signature:
            return True  # self.detectionValidity(token=token)
        else:
            self.setCodeAndMessage(301, 'Verification failed!')
            return False

    def detectionValidity(self, token) -> bool:
        r = redis.Redis(connection_pool=redis_pool)
        validty = r.hget(self.VALIDITY, token)
        if validty is None:
            r.hset(self.VALIDITY, token,
                   json.dumps({
                       'timestamp': time.time(),
                       'times': 0
                   }))
            return True
        elif time.time() - json.loads(validty).get(
                'timestamp') >= 20 * 60 and json.loads(validty).get(
                    'times') + 1 <= 50:
            return True
        elif time.time() - json.loads(validty).get('timestamp') < 20 * 60:
            self.setCodeAndMessage(
                302,
                'The request is too frequent and can only be requested once within 20 minutes.'
            )
            return False
        elif json.loads(validty).get('times') + 1 > 50:
            self.setCodeAndMessage(
                302, 'Exceeded the maximum number of requests today.')
            return False

    def setCodeAndMessage(self, code, msg):
        self.CODE = code
        self.MESSAGE = msg


class DaliyReportAPI(BasicAPI):

    def post(self):
        today = getTodayTimestamp()
        t_phishing = PhishingInfo.query.filter(
            PhishingInfo.timestamp > today).count()
        t_botnet = BotnetInfo.query.filter(
            BotnetInfo.last_online > today).count()
        phishing = PhishingInfo.query.count()
        botnet = BotnetInfo.query.count()
        last_item = PhishingInfo.query.order_by(
            PhishingInfo.timestamp.desc()).limit(1).all()
        last_update = last_item[0].timestamp
        return jsonify({
            "phishing_total":
            phishing,
            "botnet_total":
            botnet,
            "today_phishing":
            t_phishing,
            "today_botnet":
            t_botnet,
            "last_update":
            time.strftime("%Y-%m-%d %H:%M:%S",
                          time.localtime(float(last_update))),
            "collected_source":
            "phishstats",
            "updated_source":
            "feodotracker"
        })


class PhishingAPI(BasicAPI):
    VALIDITY = 'yinglong_user_validity_phishing'

    def post(self):
        today = datetime.date.today()
        r = redis.Redis(connection_pool=redis_pool)
        data = json.loads(request.data)
        token = data.get('token')
        date = data.get('date')
        quantity = data.get('quantity')
        timestamp = data.get('timestamp')
        signature = data.get('signature')
        secret = r.hget('yinglong_authentication', token)
        print(token, secret, timestamp, signature)
        if self.verification(token=token,
                             secert=secret,
                             timestamp=timestamp,
                             signature=signature):
            index, content = getNoNoneItem([date, quantity])
            if content == str(today):
                result = self.getTodayData()
            elif index == 0:
                result = self.getDateData(content)
            elif index == 1:
                result = self.getQuantityData(content)
            else:
                result = self.getTodayData()
            self.updateCache(token=token)
            return jsonify({
                'result': result,
                'timestamp': int(time.time()),
                'total': len(result),
                'msg': self.MESSAGE,
                'code': self.CODE
            })
        else:
            return jsonify({'code': self.CODE, 'msg': self.MESSAGE})

    def updateCache(self, token) -> None:
        r = redis.Redis(connection_pool=redis_pool)
        times = json.loads(r.hget(self.VALIDITY, token)).get('times')
        r.hset(self.VALIDITY, token,
               json.dumps({
                   'timestamp': time.time(),
                   'times': times + 1
               }))

    def getTodayData(self) -> dict:
        today = datetime.date.today()
        t = int(time.mktime(time.strptime(str(today),
                                          '%Y-%m-%d'))) - 12 * 60 * 60
        r = redis.Redis(connection_pool=redis_pool)
        if r.hget('yinglong_phishing', str(today)) is not None:
            result = json.loads(r.hget('yinglong_phishing', str(today)))
        else:
            phishing = commonQueryCompare(PhishingInfo, PhishingInfo.timestamp,
                                          t, '>')
            result = [{
                'ip': item.ip,
                'domain': item.domain,
                'timestamp': item.timestamp
            } for item in phishing]
        return result

    def getDateData(self, date) -> dict:
        bt = int(time.mktime(time.strptime(str(date),
                                           '%Y-%m-%d'))) - 12 * 60 * 60
        et = bt + 24 * 3600
        phishing = PhishingInfo.query.filter(
            and_(PhishingInfo.timestamp >= bt,
                 PhishingInfo.timestamp < et)).all()
        result = [{
            'ip': item.ip,
            'domain': item.domain,
            'timestamp': item.timestamp
        } for item in phishing]
        return result

    def getQuantityData(self, quantity):
        if quantity > 10000:
            quantity = 10000
        if quantity < 0:
            quantity = 0
        phishing = commonQueryOrder(PhishingInfo, PhishingInfo.timestamp,
                                    quantity)
        result = [{
            'ip': item.ip,
            'domain': item.domain,
            'timestamp': item.timestamp
        } for item in phishing]
        return result


class BotnetAPI(BasicAPI):
    VALIDITY = 'yinglong_user_validity_botnet'

    def post(self):
        today = datetime.date.today()
        r = redis.Redis(connection_pool=redis_pool)
        data = json.loads(request.data)
        token = data.get('token')
        date = data.get('date')
        quantity = data.get('quantity')
        timestamp = data.get('timestamp')
        signature = data.get('signature')
        secret = r.hget('yinglong_authentication', token)
        if self.verification(token=token,
                             secert=secret,
                             timestamp=timestamp,
                             signature=signature):
            index, content = getNoNoneItem([date, quantity])
            if content == str(today):
                result = self.getTodayData()
            elif index == 0:
                result = self.getDateData(content)
            elif index == 1:
                result = self.getQuantityData(content)
            else:
                result = self.getTodayData()
            self.updateCache(token=token)
            return jsonify({
                'result': result,
                'timestamp': int(time.time()),
                'total': len(result),
                'code': self.CODE,
                'msg': self.MESSAGE
            })
        else:
            return jsonify({'code': self.CODE, 'msg': self.MESSAGE})

    def updateCache(self, token) -> None:
        r = redis.Redis(connection_pool=redis_pool)
        times = json.loads(r.hget(self.VALIDITY, token)).get('times')
        r.hset(self.VALIDITY, token,
               json.dumps({
                   'timestamp': time.time(),
                   'times': times + 1
               }))

    def getTodayData(self) -> dict:
        today = str(datetime.date.today())
        t = time.mktime(time.strptime(str(today), '%Y-%m-%d'))
        r = redis.Redis(connection_pool=redis_pool)
        if r.hget('yinglong_botnet', today) is not None:
            result = json.loads(r.hget('yinglong_botnet', today))
        else:
            botnet = commonQueryCompare(BotnetInfo, BotnetInfo.last_online, t,
                                        '>')
            result = [{
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
        return result

    def getDateData(self, date) -> dict:
        bt = int(time.mktime(time.strptime(str(date), '%Y-%m-%d')))
        et = bt + 24 * 3600
        botnet = BotnetInfo.query.filter(
            and_(BotnetInfo.last_online >= bt,
                 BotnetInfo.last_online < et)).all()
        result = [{
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
        return result

    def getQuantityData(self, quantity) -> dict:
        if quantity > 10000:
            quantity = 10000
        if quantity < 0:
            quantity = 0
        botnet = commonQueryOrder(BotnetInfo, BotnetInfo.last_online, quantity)
        result = [{
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
        return result
