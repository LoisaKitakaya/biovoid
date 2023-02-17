from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

login_manager.login_view = 'core.sign_in'
login_manager.login_message_category = "info"
login_manager.login_message = "Please login to access this page."