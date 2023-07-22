from . import db

class Teacher(db.Model):
  __tablename__ = 'teachers'

  id = db.Column('id', db.String(64), primary_key=True, doc='id')
  teacher_name = db.Column('teacher_name',db.String(64), doc='teacher_name')
  password = db.Column('password',db.String(64), doc='password')