from flask import Blueprint
from app.extensions import login_manager

bp = Blueprint('core', __name__)

from app.core import routes

login_manager.login_view = 'core.sign_in'
login_manager.login_message_category = "info"
login_manager.login_message = "Please login to access the admin panel."