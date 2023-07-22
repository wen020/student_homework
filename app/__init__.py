from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    class Config(object):
        SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:ggsddu@8.142.83.101:3306/student_homework'
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        SQLALCHEMY_ECHO = True

    app.config.from_object(Config)
    db.init_app(app)

    from .views import views
    app.register_blueprint(views, url_prefix='/')
    with app.app_context():
        db.create_all()

    return app
