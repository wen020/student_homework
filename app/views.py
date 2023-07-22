from flask import Blueprint, request, Response, make_response, jsonify
from .models import Teacher
import json

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
    print('222')
    return Response(
      "The response record not find",
      status=500,
    )
  else:
    print(answer)
    return make_response(jsonify(
      userId=answer.id,
      username=answer.teacher_name,
      userType=2,
      loggedIn=True,
    ), 200)