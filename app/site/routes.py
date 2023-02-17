from app.site import bp
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

@bp.route('/', methods=['GET'])
def home():

    return render_template('site/home.html', this_user=current_user)