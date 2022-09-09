import json
from flask import jsonify, request
from flask_app import flask_app
from model import db, User


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
            user = db.session.query(User).filter(
                User.username == username, User.uid == uid).first()
            user.subscribe_type = dtype
            user.subscribe_content = str(content)
            return jsonify({'code': 200, 'msg': 'ok'})
        else:
            return jsonify({'code': 400, 'msg': 'ok'})


@flask_app.route('/api/v1/threatip/')
def threatIP():
    if request.method == 'GET':
        return jsonify({'hello': 'world'})


if __name__ == '__main__':
    flask_app.run(host='127.0.0.1', port=8000, debug=True)
