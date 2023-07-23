import json

from flask import Blueprint, request, jsonify, session
from .models import Homework, StudentHomework, User
from . import responseCode, PAGE_SIZE, SESSION_USER_STATUS, db

teacherViews = Blueprint('teacherViews', __name__)


@teacherViews.route('/homework/page/count', methods=['GET'])
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
        paginate_obj = Homework.query.filter(Homework.TeacherId == userId)
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
        print("error: ", e)
        return jsonify(
            code=responseCode.INTERNAL_SERVER_ERROR,
            message="INTERNAL_SERVER_ERROR!",
            data={},
        )


@teacherViews.route('/homework/page/<index>', methods=['GET'])
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
        paginate_obj = Homework.query.filter(Homework.TeacherId == userId)
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
        print("error: ", e)
        return jsonify(
            code=responseCode.INTERNAL_SERVER_ERROR,
            message="INTERNAL_SERVER_ERROR!",
            data={},
        )


@teacherViews.route('/homework', methods=['POST'])
def addHomework():
    try:
        status = session.get(SESSION_USER_STATUS)
        if not status:
            return jsonify(
                code=responseCode.NOT_LOGGED_IN,
                message="NOT_LOGGED_IN!",
                data={},
            )
        data = request.get_data()
        data = json.loads(data)
        print(data)
        homeworkId = data['homeworkId']
        homeworkTitle = data['homeworkTitle']
        homeworkContent = data['homeworkContent']
        record = Homework(homeworkId, status.userId, homeworkTitle, homeworkContent)
        db.session.add(record)
        db.session.commit()
        return jsonify(
            code=responseCode.SUCCESS,
            message="",
            data={},
        )
    except Exception as e:
        print("error: ", e)
        return jsonify(
            code=responseCode.INTERNAL_SERVER_ERROR,
            message="INTERNAL_SERVER_ERROR!",
            data={},
        )


@teacherViews.route('/homework/<id>', methods=['GET'])
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
        print("error: ", e)
        return jsonify(
            code=responseCode.INTERNAL_SERVER_ERROR,
            message="INTERNAL_SERVER_ERROR!",
            data={},
        )


@teacherViews.route('/homework', methods=['PUT'])
def updateHomework():
    try:
        status = session.get(SESSION_USER_STATUS)
        if not status:
            return jsonify(
                code=responseCode.NOT_LOGGED_IN,
                message="NOT_LOGGED_IN!",
                data={},
            )
        data = request.get_data()
        data = json.loads(data)
        print(data)
        homeworkId = data['homeworkId']
        homeworkTitle = data['homeworkTitle']
        homeworkContent = data['homeworkContent']
        Homework.query.filter(Homework.HomeworkId == homeworkId).update(
            {'HomeworkTitle': homeworkTitle, 'HomeworkContent': homeworkContent})
        db.session.commit()
        return jsonify(
            code=responseCode.SUCCESS,
            message="",
            data={},
        )
    except Exception as e:
        print("error: ", e)
        return jsonify(
            code=responseCode.INTERNAL_SERVER_ERROR,
            message="INTERNAL_SERVER_ERROR!",
            data={},
        )


@teacherViews.route('/homework/<id>', methods=['DELETE'])
def delHomework(id):
    try:
        status = session.get(SESSION_USER_STATUS)
        if not status:
            return jsonify(
                code=responseCode.NOT_LOGGED_IN,
                message="NOT_LOGGED_IN!",
                data={},
            )
        Homework.query.filter_by(HomeworkId=id).delete()
        db.session.commit()
        return jsonify(
            code=responseCode.SUCCESS,
            message="",
            data={},
        )
    except Exception as e:
        print("error: ", e)
        return jsonify(
            code=responseCode.INTERNAL_SERVER_ERROR,
            message="INTERNAL_SERVER_ERROR!",
            data={},
        )

@teacherViews.route('/submitted/page/count', methods=['GET'])
def getSubmittedPageCount():
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
        studentId = request.args.get("studentId")
        studentName = request.args.get("studentName")
        paginate_obj = StudentHomework.query.filter(StudentHomework.TeacherId == userId)
        if homeworkId:
            paginate_obj = paginate_obj.filter(StudentHomework.HomeworkId == homeworkId)
        if homeworkTitle:
            paginate_obj = paginate_obj.filter(StudentHomework.HomeworkId.contains(homeworkTitle))
        if studentId:
            paginate_obj = paginate_obj.filter(StudentHomework.StudentId == studentId)
        if studentName:
            paginate_obj = paginate_obj.filter(StudentHomework.StudentName.contains(studentName))
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
        print("error: ", e)
        return jsonify(
            code=responseCode.INTERNAL_SERVER_ERROR,
            message="INTERNAL_SERVER_ERROR!",
            data={},
        )


@teacherViews.route('/submitted/page/<index>', methods=['GET'])
def getSubmittedPage(index):
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
        studentId = request.args.get("studentId")
        studentName = request.args.get("studentName")
        paginate_obj = StudentHomework.query.filter(StudentHomework.TeacherId == userId)
        if homeworkId:
            paginate_obj = paginate_obj.filter(StudentHomework.HomeworkId == homeworkId)
        if homeworkTitle:
            paginate_obj = paginate_obj.filter(StudentHomework.HomeworkId.contains(homeworkTitle))
        if studentId:
            paginate_obj = paginate_obj.filter(StudentHomework.StudentId == studentId)
        if studentName:
            paginate_obj = paginate_obj.filter(StudentHomework.StudentName.contains(studentName))
        paginate_obj = paginate_obj.paginate(page=int(index), per_page=PAGE_SIZE,
                                             error_out=False)  # 第一页，每页20条数据。 默认第一页。
        # 参数：error_out 设为True表示页数不是int或超过总页数时,会报错,并返回404状态码。 默认True
        homework_list = []
        for data in paginate_obj.items:
            homework = Homework.query.filter_by(HomeworkId=data.HomeworkId).first()
            if homework is None:
                print("{} Record not find!".format(data.HomeworkId))
                return jsonify(
                    code=responseCode.FAIL,
                    message="Record not find!",
                    data={},
                )
            teacher = User.query.filter_by(UserId=homework.TeacherId).first()
            if teacher is None:
                print("{} Record not find!".format(homework.TeacherId))
                return jsonify(
                    code=responseCode.FAIL,
                    message="Record not find!",
                    data={},
                )
            homework_list.append({
                "studentHomeworkId": data.StudentHomeworkId,
                "studentId": data.StudentId,
                "studentName": status.username,
                "homeworkId": data.HomeworkId,
                "homeworkTitle": homework.HomeworkTitle,
                "homeworkContent": homework.HomeworkContent,
                "teacherId": teacher.UserId,
                "teacherName": teacher.UserName,
                "title": data.Title,
                "content": data.Content,
                "teacherComment": data.TeacherComment,
            })

        return jsonify(
            code=responseCode.SUCCESS,
            message="",
            data=homework_list,
        )
    except Exception as e:
        print("error: ", e)
        return jsonify(
            code=responseCode.INTERNAL_SERVER_ERROR,
            message="INTERNAL_SERVER_ERROR!",
            data={},
        )
