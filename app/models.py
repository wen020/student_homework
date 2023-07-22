from . import db

class Teacher(db.Model):
  __tablename__ = 'teachers'

  id = db.Column('id', db.String, primary_key=True, doc='id')
  teacher_name = db.Column('teacher_name',db.String, doc='teacher_name')
  password = db.Column('password',db.String, doc='password')