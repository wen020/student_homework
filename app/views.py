from flask import Blueprint, request, Response, make_response, jsonify
from .models import Teacher
import json
from . import db
from . import responseCode

views = Blueprint('views', __name__)


@views.route('/user/login', methods=['POST', 'OPTIONS'])
def login():
    data = request.get_data()
    print(data)
    data = json.loads(data)
    print(data)
    userId = data['userId']
    password = data['password']
    userType = data['userType']
    answer = Teacher.query.filter_by(id=userId, password=password).first()
    if answer is None:
        return jsonify(
            code=responseCode.FAIL,
            message="Record not find!",
            data={},
        )
    else:
        print(answer)
        return jsonify(
            code=responseCode.SUCCESS,
            message="",
            data={"userId": answer.id,
                  "username": answer.teacher_name,
                  "userType": 2,
                  "loggedIn": True},
        )


@views.route('/user/register', methods=['POST'])
def register():
    data = request.get_data()
    print(data)
    data = json.loads(data)
    userId = data['userId']
    username = data['username']
    password = data['password']
    userType = data['userType']
    record = Teacher(userId, username, password)
    db.session.add(record)
    db.session.commit()
    return jsonify(
        code=responseCode.SUCCESS,
        message="",
        data={},
    )
