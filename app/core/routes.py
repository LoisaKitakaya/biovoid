from flask import render_template
from app.core import bp

@bp.route('/')
def home():

    return render_template('home.html')

@bp.route('/admin/')
def admin():

    return render_template('admin/admin.html')

@bp.route('/sign_in/')
def sign_in():

    return render_template('admin/sign_in.html')