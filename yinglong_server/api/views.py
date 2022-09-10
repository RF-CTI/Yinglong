import json
from flask import jsonify, request
from ..models import db, User
from flask_restful import Resource


class Subscribe(Resource):

    def post(self):
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
