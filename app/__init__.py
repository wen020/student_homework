from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_session import Session

db = SQLAlchemy()
PAGE_SIZE = 7
SESSION_USER_STATUS = "user_status"
def create_app():
    app = Flask(__name__)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)
    # cors = CORS(app, resources={r"/*": {"origins": "*"}})
    cors = CORS(app, supports_credentials=True,
                resources={r"/*": {"origins": "*", "methods": ["PUT", "GET", "POST", "DELETE", "OPTIONS"],
                                   "allow_headers": ["Referer", "Access-Control-Allow-Origin", "Accept", "Origin",
                                                     "User-Agent", "Token"], }})

    class Config(object):
        SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:ggsddu@127.0.0.1:3306/student_homework'
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        SQLALCHEMY_ECHO = True

    app.config.from_object(Config)
    db.init_app(app)

    from .userViews import userViews
    from .studentViews import studentViews
    from .teacherViews import teacherViews
    app.register_blueprint(userViews, url_prefix='/user')
    app.register_blueprint(studentViews, url_prefix='/student')
    app.register_blueprint(teacherViews, url_prefix='/teacher')
    with app.app_context():
        db.create_all()

    return app
