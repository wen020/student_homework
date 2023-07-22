from flask import Blueprint, request, Response, make_response, jsonify
from .models import User
import json
from . import db
from . import responseCode
from flask_session import Session

views = Blueprint('views', __name__)


@views.route('/user/login', methods=['POST'])
def login():
    try:
        data = request.get_data()
        print(data)
        data = json.loads(data)
        print(data)
        userId = data['userId']
        password = data['password']
        userType = data['userType']
        answer = User.query.filter_by(UserId=userId, password=password, UserType=userType).first()
        if answer is None:
            return jsonify(
                code=responseCode.FAIL,
                message="Record not find!",
                data={},
            )
        else:
            answer.IsLogin = True
            db.session.commit()
            return jsonify(
                code=responseCode.SUCCESS,
                message="",
                data={"userId": answer.id,
                      "username": answer.teacher_name,
                      "userType": userType,
                      "loggedIn": answer.IsLogin},
            )
    except Exception as e:
        print(e)
        return jsonify(
            code=responseCode.INTERNAL_SERVER_ERROR,
            message="INTERNAL_SERVER_ERROR!",
            data={},
        )


@views.route('/user/register', methods=['POST'])
def register():
    try:
        data = request.get_data()
        print(data)
        data = json.loads(data)
        userId = data['userId']
        userName = data['username']
        password = data['password']
        userType = data['userType']
        record = User(userId, userName, userType, password)
        db.session.add(record)
        db.session.commit()
        return jsonify(
            code=responseCode.SUCCESS,
            message="",
            data={},
        )
    except Exception as e:
        print(e)
        return jsonify(
            code=responseCode.INTERNAL_SERVER_ERROR,
            message="INTERNAL_SERVER_ERROR!",
            data={},
        )

class LoginStatus:
    def __init__(self):
        pass
@views.route('/user/login/status', methods=['GET'])
def GetStatus():
    SESSION_USER_STATUS = "user_status"
    if not Session.get(SESSION_USER_STATUS):
        Session[SESSION_USER_STATUS] = LoginStatus()