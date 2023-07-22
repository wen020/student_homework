from . import db
import uuid
import enum
from sqlalchemy import Enum


class TagEnum(enum.Enum):
    student = 1
    teacher = 2


class User(db.Model):
    __tablename__ = 'Users'

    # Id = db.Column('id', db.String(64), primary_key=True, doc='id')
    UserId = db.Column('id', db.String(64), primary_key=True, doc='user_id')
    UserName = db.Column('user_name', db.String(64), doc='user_name')
    UserType = db.Column('user_type', Enum(TagEnum), doc='user_type')
    IsLogin = db.Column('is_login', db.Boolean, doc='is_login')
    Password = db.Column('password', db.String(64), doc='password')

    def __init__(self, userId, userName, userType, password):
        # self.Id = str(uuid.uuid4())
        self.UserId = userId
        self.UserName = userName
        self.UserType = userType
        self.Password = password
