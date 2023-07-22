from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    # cors = CORS(app, resources={r"/*": {"origins": "*"}})
    cors = CORS(app, resources={r"/*": {"origins": "*", "methods": ["PUT", "GET", "POST", "DELETE", "OPTIONS"],
                           "allow_headers": ["Referer", "Access-Control-Allow-Origin", "Accept", "Origin", "User-Agent", "Token"], }})

    class Config(object):
        SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:ggsddu@127.0.0.1:3306/student_homework'
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        SQLALCHEMY_ECHO = True

    app.config.from_object(Config)
    db.init_app(app)

    from .views import views
    app.register_blueprint(views, url_prefix='/')
    with app.app_context():
        db.create_all()

    return app
