from flask import Blueprint, request, jsonify, session
from .models import User
import json
from . import db
from . import responseCode

views = Blueprint('views', __name__)

SESSION_USER_STATUS = "user_status"


class LoginStatus:
    def __init__(self, loggedIn=None, userId=None, username=None, userType=None):
        self.loggedIn = loggedIn
        self.userId = userId
        self.username = username
        self.userType = userType


@views.route('/user/login', methods=['POST'])
def login():
    try:
        data = request.get_data()
        data = json.loads(data)
        print(data)
        userId = data['userId']
        password = data['password']
        userType = data['userType']
        answer = User.query.filter_by(UserId=userId, Password=password).first()
        if answer is None:
            print("{} Record not find!".format(userId))
            return jsonify(
                code=responseCode.FAIL,
                message="Record not find!",
                data={},
            )
        else:
            answer.IsLogin = True
            db.session.commit()
            session[SESSION_USER_STATUS] = LoginStatus(loggedIn=answer.IsLogin, userId=answer.UserId, username=answer.UserName, userType=userType)
            return jsonify(
                code=responseCode.SUCCESS,
                message="",
                data={"userId": answer.UserId,
                      "username": answer.UserName,
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


@views.route('/user/login/status', methods=['GET'])
def getStatus():
    status = session.get(SESSION_USER_STATUS)
    if not status:
        status = LoginStatus()
        session[SESSION_USER_STATUS] = status
    return jsonify(
        code=responseCode.SUCCESS,
        message="",
        data={"userId": status.userId,
                      "username": status.username,
                      "userType": status.userType,
                      "loggedIn": status.loggedIn},
    )

@views.route('user/logout', methods=['GET'])
def logout():
    session[SESSION_USER_STATUS] = None
    return jsonify(
        code=responseCode.SUCCESS,
        message="注销成功",
        data={},
    )
