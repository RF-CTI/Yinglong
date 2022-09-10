from flask import jsonify, request, render_template
from ..models import db, User
from flask_restful import Resource
from ..extensions import login_manager


class RegisterView(Resource):

    def post(self):
        data = request.form  # json.loads(request.data)
        print(data)
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
    
    def get(self):
        return render_template('register.html')


@login_manager.user_loader
class LoginView(Resource):

    def post(self):
        data = request.form  # json.loads(request.data)
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

    def get(self):
        return render_template('login.html')
