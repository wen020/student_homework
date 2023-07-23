from flask import Blueprint, request, jsonify, session
from .models import Homework, StudentHomework, User
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
        print("error: ", e)
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
        print("error: ", e)
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
        print("error: ", e)
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
        studentTitle = data['title']
        studentContent = data['content']
        record = StudentHomework(None, userId, homeworkId, studentTitle, studentContent)
        db.session.add(record)
        db.session.commit()
        return jsonify(
            code=responseCode.SUCCESS,
            message="提交作业成功",
            data={},
        )
    except Exception as e:
        print("error: ", e)
        return jsonify(
            code=responseCode.INTERNAL_SERVER_ERROR,
            message="提交作业失败!",
            data={},
        )


@studentViews.route('/submitted/page/count', methods=['GET'])
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
        print("error: ", e)
        return jsonify(
            code=responseCode.INTERNAL_SERVER_ERROR,
            message="INTERNAL_SERVER_ERROR!",
            data={},
        )


@studentViews.route('/submitted/page/<index>', methods=['GET'])
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

@studentViews.route('/submitted/<id>', methods=['GET'])
def getSubmittedHomework(id):
    try:
        status = session.get(SESSION_USER_STATUS)
        if not status:
            return jsonify(
                code=responseCode.NOT_LOGGED_IN,
                message="NOT_LOGGED_IN!",
                data={},
            )
        answer = StudentHomework.query.filter_by(HomeworkId=id).first()
        if answer is None:
            print("{} Record not find!".format(id))
            return jsonify(
                code=responseCode.FAIL,
                message="Record not find!",
                data={},
            )
        else:
            homework = Homework.query.filter_by(HomeworkId=answer.HomeworkId).first()
            if homework is None:
                print("{} Record not find!".format(answer.HomeworkId))
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

            return jsonify(
                code=responseCode.SUCCESS,
                message="",
                data={
                "studentHomeworkId": answer.StudentHomeworkId,
                "studentId": answer.StudentId,
                "studentName": status.username,
                "homeworkId": answer.HomeworkId,
                "homeworkTitle": homework.HomeworkTitle,
                "homeworkContent": homework.HomeworkContent,
                "teacherId": teacher.UserId,
                "teacherName": teacher.UserName,
                "title": answer.Title,
                "content": answer.Content,
                "teacherComment": answer.TeacherComment,
            },
            )
    except Exception as e:
        print("error: ", e)
        return jsonify(
            code=responseCode.INTERNAL_SERVER_ERROR,
            message="INTERNAL_SERVER_ERROR!",
            data={},
        )


@studentViews.route('/submitted', methods=['PUT'])
def updateSubmittedHomework():
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
        title = data['title']
        content = data['content']
        studentHomeworkId = data['studentHomeworkId']
        answer = StudentHomework.query.filter_by(StudentHomeworkId=studentHomeworkId).first()
        if answer is None:
            print("{} Record not find!".format(id))
            return jsonify(
                code=responseCode.FAIL,
                message="Record not find!",
                data={},
            )
        else:
            if answer.TeacherComment:
                return jsonify(
                    code=responseCode.FAIL,
                    message="老师已点评，不能更新作业!",
                    data={},
                )
            answer.update(
                {'Title': title, 'Content': content})
            db.session.commit()
            return jsonify(
                code=responseCode.SUCCESS,
                message="更新作业成功",
                data={},
            )
    except Exception as e:
        print("error: ", e)
        return jsonify(
            code=responseCode.INTERNAL_SERVER_ERROR,
            message="INTERNAL_SERVER_ERROR!",
            data={},
        )