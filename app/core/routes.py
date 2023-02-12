from flask import render_template
from app.core import bp

@bp.route('/', methods=['GET'])
def home():

    return render_template('home.html')

@bp.route('/admin/', methods=['GET', 'POST'])
def admin():

    return render_template('admin/admin.html')

@bp.route('/sign_in/', methods=['GET', 'POST'])
def sign_in():

    return render_template('admin/sign_in.html')