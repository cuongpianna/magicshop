from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager
from flask_whooshee import Whooshee
from flask_ckeditor import CKEditor
import os

db = SQLAlchemy()
lm = LoginManager()
lm.login_view = 'auth.login'
whooshe = Whooshee()
ALLOW_EXTENSIONS = set(['png','jpg','jpeg'])
UPLOAD_FOLDER = os.path.realpath('.') + '/app/static/uploads'

#hàm khởi tạo
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    ckeditor = CKEditor(app)
    lm.init_app(app)
    whooshe.init_app(app)

    #đăng ký bluebrint
    from .auth import auth as auth_blueprint
    from .admin import admin as admin_blueprint
    from .home import home as home_blueprint
    from .user import user as user_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(admin_blueprint,url_prefix='/admin')
    app.register_blueprint(home_blueprint)
    app.register_blueprint(user_blueprint,url_prefix='/user')
    return app
