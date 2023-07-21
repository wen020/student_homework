import json

from flask import Flask, render_template, request, Response, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


class Config(object):
  SQLALCHEMY_DATABASE_URI = 'mysql://root:1234@127.0.0.1:3306/student_homework'
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SQLALCHEMY_ECHO = True


app.config.from_object(Config)

# 直接实例化sqlalchemy对象，传⼊app
db = SQLAlchemy(app)


class Teacher(db.Model):
  __tablename__ = 'teachers'

  teacher_id = db.Column('teacher_id', db.String, primary_key=True, doc='teacher_id')
  teacher_name = db.Column(db.String, doc='teacher_name')
  password = db.Column(db.String, doc='password')


# 定义配置对象

@app.route('/user/login', methods=['POST', 'OPTIONS'])
def login():
  data = request.get_data()
  print(data)
  # 查询记录
  # req = request.get_json()['content']  # 获取get请求参数
  # print(req)
  data = json.loads(data)
  print(data)
  userId = data['userId']
  password = data['password']
  userType = data['userType']
  answer = Teacher.query.filter_by(teacher_id=userId, password=password).first()
  if answer is None:
    print('222')
    return Response(
      "The response record not find",
      status=500,
    )
  else:
    print(answer)
    return make_response(jsonify(
      userId=answer.teacher_id,
      username=answer.teacher_name,
      userType=2,
      loggedIn=True,
    ), 200)


if __name__ == '__main__':
  app.run()
