from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from .settings import LOGIN_PAGE, LOGIN_MESSAGE

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = LOGIN_PAGE
login_manager.login_message = LOGIN_MESSAGE