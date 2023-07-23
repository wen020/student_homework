from flask import Blueprint, request, jsonify, session
from .models import Homework, StudentHomework
import json
from . import db, responseCode, SESSION_USER_STATUS, PAGE_SIZE

studentViews = Blueprint('studentViews', __name__)

@studentViews.route('/homework/page/count', methods=['GET'])
def getPageCount():
    try:
        status = session.get(SESSION_USER_STATUS)
        if not status:
            return jsonify(
                code=responseCode.NOT_LOGGED_IN,
                message="NOT_LOGGED_IN!",
                data={},
            )
        userId = status.userId
        homeworkId = request.args.get("homeworkId")
        homeworkTitle = request.args.get("homeworkTitle")
        paginate_obj = Homework.query
        if homeworkId:
            paginate_obj = paginate_obj.filter(Homework.HomeworkId == homeworkId)
        if homeworkTitle:
            paginate_obj = paginate_obj.filter(Homework.HomeworkId.contains(homeworkTitle))
        paginate_obj = paginate_obj.paginate(page=1, per_page=PAGE_SIZE, error_out=False)  # 第一页，每页20条数据。 默认第一页。
        # 参数：error_out 设为True表示页数不是int或超过总页数时,会报错,并返回404状态码。 默认True
        # user_list = paginate_obj.items
        # 获取总页数
        total_page = paginate_obj.pages
        return jsonify(
            code=responseCode.SUCCESS,
            message="",
            data=total_page,
        )
    except Exception as e:
        print(e)
        return jsonify(
            code=responseCode.INTERNAL_SERVER_ERROR,
            message="INTERNAL_SERVER_ERROR!",
            data={},
        )


@studentViews.route('/homework/page/<index>', methods=['GET'])
def getPage(index):
    try:
        status = session.get(SESSION_USER_STATUS)
        if not status:
            return jsonify(
                code=responseCode.NOT_LOGGED_IN,
                message="NOT_LOGGED_IN!",
                data={},
            )
        userId = status.userId
        homeworkId = request.args.get("homeworkId")
        homeworkTitle = request.args.get("homeworkTitle")
        paginate_obj = Homework.query
        if homeworkId:
            paginate_obj = paginate_obj.filter(Homework.HomeworkId == homeworkId)
        if homeworkTitle:
            paginate_obj = paginate_obj.filter(Homework.HomeworkId.contains(homeworkTitle))
        paginate_obj = paginate_obj.paginate(page=int(index), per_page=PAGE_SIZE,
                                             error_out=False)  # 第一页，每页20条数据。 默认第一页。
        # 参数：error_out 设为True表示页数不是int或超过总页数时,会报错,并返回404状态码。 默认True
        homework_list = []
        for data in paginate_obj.items:
            homework_list.append({
                "homeworkId": data.HomeworkId,
                "teacherId": data.TeacherId,
                "teacherName": status.username,
                "homeworkTitle": data.HomeworkTitle,
                "homeworkContent": data.HomeworkContent,
            })

        return jsonify(
            code=responseCode.SUCCESS,
            message="",
            data=homework_list,
        )
    except Exception as e:
        print(e)
        return jsonify(
            code=responseCode.INTERNAL_SERVER_ERROR,
            message="INTERNAL_SERVER_ERROR!",
            data={},
        )

@studentViews.route('/homework/<id>', methods=['GET'])
def getHomework(id):
    try:
        status = session.get(SESSION_USER_STATUS)
        if not status:
            return jsonify(
                code=responseCode.NOT_LOGGED_IN,
                message="NOT_LOGGED_IN!",
                data={},
            )
        answer = Homework.query.filter_by(HomeworkId=id).first()
        if answer is None:
            print("{} Record not find!".format(id))
            return jsonify(
                code=responseCode.FAIL,
                message="Record not find!",
                data={},
            )
        else:
            return jsonify(
                code=responseCode.SUCCESS,
                message="",
                data={
                    "homeworkId": answer.HomeworkId,
                    "teacherId": answer.TeacherId,
                    "teacherName": status.username,
                    "homeworkTitle": answer.HomeworkTitle,
                    "homeworkContent": answer.HomeworkContent,
                },
            )
    except Exception as e:
        print(e)
        return jsonify(
            code=responseCode.INTERNAL_SERVER_ERROR,
            message="INTERNAL_SERVER_ERROR!",
            data={},
        )

@studentViews.route('/homework/', methods=['POST'])
def addHomework():
    try:
        status = session.get(SESSION_USER_STATUS)
        if not status:
            return jsonify(
                code=responseCode.NOT_LOGGED_IN,
                message="NOT_LOGGED_IN!",
                data={},
            )
        userId = status.userId
        data = request.get_data()
        data = json.loads(data)
        print(data)
        homeworkId = data['homeworkId']
        homeworkTitle = data['homeworkTitle']
        homeworkContent = data['homeworkContent']
        studentTitle = data['title']
        studentContent = data['content']
        record = StudentHomework(None,homeworkId, userId, homeworkId, homeworkTitle, studentTitle, studentContent)
        db.session.add(record)
        db.session.commit()
        return jsonify(
            code=responseCode.SUCCESS,
            message="提交作业成功",
            data={},
        )
    except Exception as e:
        print(e)
        return jsonify(
            code=responseCode.INTERNAL_SERVER_ERROR,
            message="提交作业失败!",
            data={},
        )

@studentViews.route('/submitted/page/count', methods=['GET'])
def getPageCount():
    try:
        status = session.get(SESSION_USER_STATUS)
        if not status:
            return jsonify(
                code=responseCode.NOT_LOGGED_IN,
                message="NOT_LOGGED_IN!",
                data={},
            )
        userId = status.userId
        homeworkId = request.args.get("homeworkId")
        homeworkTitle = request.args.get("homeworkTitle")
        paginate_obj = StudentHomework.query.filter(StudentHomework.StudentId == userId)
        if homeworkId:
            paginate_obj = paginate_obj.filter(StudentHomework.HomeworkId == homeworkId)
        if homeworkTitle:
            paginate_obj = paginate_obj.filter(StudentHomework.HomeworkId.contains(homeworkTitle))
        paginate_obj = paginate_obj.paginate(page=1, per_page=PAGE_SIZE, error_out=False)  # 第一页，每页20条数据。 默认第一页。
        # 参数：error_out 设为True表示页数不是int或超过总页数时,会报错,并返回404状态码。 默认True
        # user_list = paginate_obj.items
        # 获取总页数
        total_page = paginate_obj.pages
        return jsonify(
            code=responseCode.SUCCESS,
            message="",
            data=total_page,
        )
    except Exception as e:
        print(e)
        return jsonify(
            code=responseCode.INTERNAL_SERVER_ERROR,
            message="INTERNAL_SERVER_ERROR!",
            data={},
        )


@studentViews.route('/submitted/page/<index>', methods=['GET'])
def getPage(index):
    try:
        status = session.get(SESSION_USER_STATUS)
        if not status:
            return jsonify(
                code=responseCode.NOT_LOGGED_IN,
                message="NOT_LOGGED_IN!",
                data={},
            )
        userId = status.userId
        homeworkId = request.args.get("homeworkId")
        homeworkTitle = request.args.get("homeworkTitle")
        paginate_obj = StudentHomework.query.filter(StudentHomework.StudentId == userId)
        if homeworkId:
            paginate_obj = paginate_obj.filter(StudentHomework.HomeworkId == homeworkId)
        if homeworkTitle:
            paginate_obj = paginate_obj.filter(StudentHomework.HomeworkId.contains(homeworkTitle))
        paginate_obj = paginate_obj.paginate(page=int(index), per_page=PAGE_SIZE,
                                             error_out=False)  # 第一页，每页20条数据。 默认第一页。
        # 参数：error_out 设为True表示页数不是int或超过总页数时,会报错,并返回404状态码。 默认True
        homework_list = []
        for data in paginate_obj.items:
            homework_list.append({
                "homeworkId": data.HomeworkId,
                "teacherId": data.TeacherId,
                "teacherName": status.username,
                "homeworkTitle": data.HomeworkTitle,
                "homeworkContent": data.HomeworkContent,
            })

        return jsonify(
            code=responseCode.SUCCESS,
            message="",
            data=homework_list,
        )
    except Exception as e:
        print(e)
        return jsonify(
            code=responseCode.INTERNAL_SERVER_ERROR,
            message="INTERNAL_SERVER_ERROR!",
            data={},
        )
