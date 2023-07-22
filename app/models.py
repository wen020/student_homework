from . import db

class Teacher(db.Model):
  __tablename__ = 'teachers'

  teacher_id = db.Column('teacher_id', db.String, primary_key=True, doc='teacher_id')
  teacher_name = db.Column(db.String, doc='teacher_name')
  password = db.Column(db.String, doc='password')