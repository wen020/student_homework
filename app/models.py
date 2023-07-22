from . import db
import uuid
import enum
from sqlalchemy import Enum


class UserType(enum.Enum):
    student = 1
    teacher = 2


class User(db.Model):
    __tablename__ = 'Users'

    # Id = db.Column('id', db.String(64), primary_key=True, doc='id')
    UserId = db.Column('id', db.String(64), primary_key=True, doc='user_id')
    UserName = db.Column('user_name', db.String(64), doc='user_name')
    UserType = db.Column('user_type', db.Integer, doc='user_type', default=UserType.student)
    IsLogin = db.Column('is_login', db.Boolean, doc='is_login')
    Password = db.Column('password', db.String(64), doc='password')

    def __init__(self, userId, userName, userType, password, isLogin=False):
        # self.Id = str(uuid.uuid4())
        self.UserId = userId
        self.UserName = userName
        self.UserType = userType
        self.Password = password
        self.IsLogin = isLogin

class HomeWork(db.Model):
    __tablename__ = 'homeworks'

    HomeworkId = db.Column('homework_id', db.String(64), primary_key=True, doc='homework_id')
    TeacherId = db.Column('teacher_id', db.String(64), doc='teacher_id')
    HomeworkTitle = db.Column('homework_title', db.String(128), doc='homework_title')
    HomeworkContent = db.Column('homework_content', db.String(1024), doc='homework_content')

    def __init__(self, homeworkId, teacherId, homeworkTitle, homeworkContent):
        if not homeworkId:
            homeworkId = str(uuid.uuid4())
        self.HomeworkId = homeworkId
        self.TeacherId = teacherId
        self.HomeworkTitle = homeworkTitle
        self.HomeworkContent = homeworkContent


class StudentHomework(db.Model):
    __tablename__ = 'student_homeworks'

    StudentHomeworkId = db.Column('student_homework_id', db.String(64), primary_key=True, doc='student_homework_id')
    StudentId = db.Column('student_id', db.String(64), doc='student_id')
    HomeworkId = db.Column('homework_id', db.String(128), doc='homework_id')
    Title = db.Column('title', db.String(1024), doc='title')
    Content = db.Column('title', db.String(1024), doc='content')
    TeacherComment = db.Column('teacher_comment', db.String(1024), doc='teacher_comment')
    Score = db.Column('score', db.Integer, doc='score', default=0)
    Appendix = db.Column('appendix', db.String(1024), doc='appendix')

    def __init__(self, studentHomeworkId, studentId, homeworkId, title, content, teacherComment, score, appendix):
        if not studentHomeworkId:
            studentHomeworkId = str(uuid.uuid4())
        self.StudentHomeworkId = studentHomeworkId
        self.StudentId = studentId
        self.HomeworkId = homeworkId
        self.Title = title
        self.Content = content
        self.TeacherComment = teacherComment
        self.Score = score
        self.Appendix = appendix