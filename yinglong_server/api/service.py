import redis
import json
from ..models import (PhishingInfo, BotnetInfo, C2Info, APILogInfo, DataSourceInfo)
from flask_restful import Resource
from flask import jsonify, request, current_app
from sqlalchemy import and_
from ..extensions import db
from utils.db_utils import commonQueryOrder, commonQueryCompare
from utils.other_utils import (getNoNoneItem, generateSecret, getErrorMessage, getMD5Code)
from utils.time_utils import (getToday, getTime, getTodayTimestamp, getDateTimestamp, getTodayString)

redis_pool = redis.ConnectionPool(host='127.0.0.1',
                                  port=6379,
                                  decode_responses=True)


class VerificationAPI(Resource):

    def post(self):
        token = str(request.args.get('token'))
        current_app.logger.info('ip-{} token-{}'.format(
            request.remote_addr, token))
        if token:
            r = redis.Redis(connection_pool=redis_pool)
            if r.sismember('yonglong_tokens', token):
                secret = getMD5Code('-'.join([token, generateSecret()]))
                r.hset('yinglong_authentication', token, secret)
                res = {'code': 200, 'secret': secret}
            else:
                res = {'code': 301, "msg": 'Incorrect token entered.'}
        else:
            res = {'code': 300, "msg": 'There is no "token" parameter.'}
        return jsonify(res)


class BasicAPI(Resource):
    VALIDITY = ''
    INTELLIGENCE_TYPE = None
    MESSAGE = 'Success.'
    CODE = 200

    def __init__(self) -> None:
        super().__init__()

    def verification(self, token, secert, timestamp, signature) -> bool:
        if not token or not secert or not timestamp or not signature:
            self.setCodeAndMessage(300, 'Missing required parameter!')
            return False
        elif getMD5Code('-'.join([token, secert, str(timestamp)])) == signature:
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
                       'timestamp': getTime(),
                       'times': 0
                   }))
            return True
        elif getTime() - json.loads(validty).get(
                'timestamp') >= 20 * 60 and json.loads(validty).get(
                    'times') + 1 <= 50:
            return True
        elif getTime() - json.loads(validty).get('timestamp') < 20 * 60:
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

    def infoLog(self, token, url, ip_address, parameters, result):
        current_app.logger.info('ip-{} parameters-{} result-{}'.format(
            ip_address, parameters, result))
        log = APILogInfo(token=token,
                         url=url,
                         ip_address=ip_address,
                         parameters=parameters,
                         result=result)
        db.session.add(log)
        db.session.commit()

    def errorLog(self):
        current_app.logger.error(getErrorMessage())


class DataSourceAPI(BasicAPI):

    def post(self):
        r = redis.Redis(connection_pool=redis_pool)
        parameters = json.loads(request.data)
        token = parameters.get('token')
        timestamp = parameters.get('timestamp')
        signature = parameters.get('signature')
        secret = r.hget('yinglong_authentication', token)
        if self.verification(token=token,
                             secert=secret,
                             timestamp=timestamp,
                             signature=signature):
            ds = DataSourceInfo.query.all()
            result = [item.to_json() for item in ds]
            res = {'result': result, 'msg': self.MESSAGE, 'code': self.CODE}
        else:
            res = {'msg': self.MESSAGE, 'code': self.CODE}
        self.infoLog(token, request.path, request.headers['X-Forwarded-For'],
                     json.dumps(parameters), json.dumps(res))
        return jsonify(res)


class PhishingAPI(BasicAPI):
    VALIDITY = 'yinglong_user_validity_phishing'
    INTELLIGENCE_TYPE = 1

    def post(self):
        today = getToday()
        r = redis.Redis(connection_pool=redis_pool)
        parameters = json.loads(request.data)
        token = parameters.get('token')
        date = parameters.get('date')
        quantity = parameters.get('quantity')
        timestamp = parameters.get('timestamp')
        signature = parameters.get('signature')
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
            res = {
                'result': result,
                'timestamp': int(getTime()),
                'total': len(result),
                'msg': self.MESSAGE,
                'code': self.CODE
            }
        else:
            res = {'code': self.CODE, 'msg': self.MESSAGE}
        self.infoLog(token, request.path, request.headers['X-Forwarded-For'],
                     json.dumps(parameters), json.dumps(res))
        return jsonify(res)

    def updateCache(self, token) -> None:
        r = redis.Redis(connection_pool=redis_pool)
        times = json.loads(r.hget(self.VALIDITY, token)).get('times')
        r.hset(self.VALIDITY, token,
               json.dumps({
                   'timestamp': getTime(),
                   'times': times + 1
               }))

    def getTodayData(self) -> dict:
        today = getToday()
        t = getTodayTimestamp() - 12 * 60 * 60
        r = redis.Redis(connection_pool=redis_pool)
        if r.hget('yinglong_phishing', str(today)) is not None:
            result = json.loads(r.hget('yinglong_phishing', str(today)))
        else:
            phishing = commonQueryCompare(PhishingInfo, PhishingInfo.timestamp,
                                          t, '>')
            result = [item.to_json() for item in phishing]
        return result

    def getDateData(self, date) -> dict:
        bt = getDateTimestamp(date) - 12 * 60 * 60
        et = bt + 24 * 3600
        phishing = PhishingInfo.query.filter(
            and_(PhishingInfo.timestamp >= bt,
                 PhishingInfo.timestamp < et)).all()
        result = [item.to_json() for item in phishing]
        return result

    def getQuantityData(self, quantity):
        if quantity > 10000:
            quantity = 10000
        if quantity < 0:
            quantity = 0
        phishing = commonQueryOrder(PhishingInfo, PhishingInfo.timestamp,
                                    quantity)
        result = [item.to_json() for item in phishing]
        return result


class BotnetAPI(BasicAPI):
    VALIDITY = 'yinglong_user_validity_botnet'
    INTELLIGENCE_TYPE = 2

    def post(self):
        today = getToday()
        r = redis.Redis(connection_pool=redis_pool)
        parameters = json.loads(request.data)
        token = parameters.get('token')
        date = parameters.get('date')
        quantity = parameters.get('quantity')
        timestamp = parameters.get('timestamp')
        signature = parameters.get('signature')
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
            res = {
                'result': result,
                'timestamp': int(getTime()),
                'total': len(result),
                'code': self.CODE,
                'msg': self.MESSAGE
            }
        else:
            res = {'code': self.CODE, 'msg': self.MESSAGE}
        self.infoLog(token, request.path, request.headers['X-Forwarded-For'],
                     json.dumps(parameters), json.dumps(res))
        return jsonify(res)

    def updateCache(self, token) -> None:
        r = redis.Redis(connection_pool=redis_pool)
        times = json.loads(r.hget(self.VALIDITY, token)).get('times')
        r.hset(self.VALIDITY, token,
               json.dumps({
                   'timestamp': getTime(),
                   'times': times + 1
               }))

    def getTodayData(self) -> dict:
        today = getTodayString()
        t = getTodayTimestamp()
        r = redis.Redis(connection_pool=redis_pool)
        if r.hget('yinglong_botnet', today) is not None:
            result = json.loads(r.hget('yinglong_botnet', today))
        else:
            botnet = commonQueryCompare(BotnetInfo, BotnetInfo.timestamp, t,
                                        '>')
            result = [item.to_json() for item in botnet]
        return result

    def getDateData(self, date) -> dict:
        bt = getDateTimestamp(date)
        et = bt + 24 * 3600
        botnet = BotnetInfo.query.filter(
            and_(BotnetInfo.timestamp >= bt, BotnetInfo.timestamp < et)).all()
        result = [item.to_json() for item in botnet]
        return result

    def getQuantityData(self, quantity) -> dict:
        if quantity > 10000:
            quantity = 10000
        if quantity < 0:
            quantity = 0
        botnet = commonQueryOrder(BotnetInfo, BotnetInfo.timestamp, quantity)
        result = [item.to_json() for item in botnet]
        return result


class C2API(BasicAPI):
    VALIDITY = 'yinglong_user_validity_c2'
    INTELLIGENCE_TYPE = 3

    def post(self):
        today = getToday()
        r = redis.Redis(connection_pool=redis_pool)
        parameters = json.loads(request.data)
        token = parameters.get('token')
        date = parameters.get('date')
        quantity = parameters.get('quantity')
        timestamp = parameters.get('timestamp')
        signature = parameters.get('signature')
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
            res = {
                'result': result,
                'timestamp': int(getTime()),
                'total': len(result),
                'code': self.CODE,
                'msg': self.MESSAGE
            }
        else:
            res = {'code': self.CODE, 'msg': self.MESSAGE}
        self.infoLog(token, request.path, request.headers['X-Forwarded-For'],
                     json.dumps(parameters), json.dumps(res))
        return jsonify(res)

    def updateCache(self, token) -> None:
        r = redis.Redis(connection_pool=redis_pool)
        if r.hget(self.VALIDITY, token) is not None:
            times = json.loads(r.hget(self.VALIDITY, token)).get('times')
            r.hset(self.VALIDITY, token,
                   json.dumps({
                       'timestamp': getTime(),
                       'times': times + 1
                   }))
        else:
            r.hset(self.VALIDITY, token,
                   json.dumps({
                       'timestamp': getTime(),
                       'times': 0
                   }))

    def getTodayData(self) -> dict:
        today = getTodayString()
        t = getTodayTimestamp()
        r = redis.Redis(connection_pool=redis_pool)
        if r.hget('yinglong_c2', today) is not None:
            result = json.loads(r.hget('yinglong_c2', today))
        else:
            c2 = commonQueryCompare(C2Info, C2Info.timestamp, t, '>')
            result = [item.to_json() for item in c2]
        return result

    def getDateData(self, date) -> dict:
        bt = getDateTimestamp(date)
        et = bt + 24 * 3600
        c2 = C2Info.query.filter(
            and_(C2Info.timestamp >= bt, C2Info.timestamp < et)).all()
        result = [item.to_json() for item in c2]
        return result

    def getQuantityData(self, quantity) -> dict:
        if quantity > 10000:
            quantity = 10000
        if quantity < 0:
            quantity = 0
        c2 = commonQueryOrder(C2Info, C2Info.timestamp, quantity)
        result = [item.to_json() for item in c2]
        return result
