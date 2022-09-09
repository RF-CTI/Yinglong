import json
import time
from flask import jsonify, request
from flask_app import flask_app
from model import db, User, PhishingInfo, BotnetInfo


@flask_app.route('/register/', methods=['POST'])
def register():
    if request.method == 'POST':
        data = json.loads(request.data)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        if not username or not email or not password:
            return jsonify({'code': 400, 'msg': 'faild'})
        else:
            try:
                user = User(username, email, password)
                db.session.add(user)
                db.session.commit()
                return {'code': 200, 'msg': 'ok'}
            except Exception:
                return {
                    'code': 401,
                    'msg': 'Username or email is already registered!'
                }


@flask_app.route('/login/')
def login():
    if request.method == 'POST':
        data = json.loads(request.data)
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user = db.session.query(User).filter(
                User.username == username, User.password == password).first()
            user.is_login = True
            db.session.commit()
            return jsonify({'code': 200, 'msg': 'ok'})
        else:
            return jsonify({'code': 400, 'msg': 'faild'})


@flask_app.route('/api/subscribe/', methods=['POST'])
def subscribe():
    if request.method == 'POST':
        data = json.loads(request.data)
        username = data.get('username')
        dtype = data.get('type')
        content = data.get('content')
        uid = data.get('uid')
        if username and dtype and content and uid:
            user = db.session.query(User).filter(User.username == username,
                                                 User.uid == uid).first()
            user.subscribe_type = dtype
            user.subscribe_content = str(content)
            return jsonify({'code': 200, 'msg': 'ok'})
        else:
            return jsonify({'code': 400, 'msg': 'ok'})


@flask_app.route('/api/v1/phishing/', methods=['POST'])
def phishing():
    if request.method == 'POST':
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


@flask_app.route('/api/v1/botnet/', methods=['POST'])
def botnet():
    if request.method == 'POST':
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


if __name__ == '__main__':
    flask_app.run(host='127.0.0.1', port=8000, debug=True)
