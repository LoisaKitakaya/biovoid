import os
from app.core import bp
from app.models.users import User
from werkzeug.security import check_password_hash
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

@bp.route('/', methods=['GET'])
def home():

    return render_template('home.html')

@bp.route('/admin/', methods=['GET', 'POST'])
@login_required
def admin():

    users = User.query.all()

    return render_template(
        'admin/admin.html',
        super_user=current_user,
        all_users=users,
    )

@bp.route('/sign_in/', methods=['GET', 'POST'])
def sign_in():

    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        try:

            this_user = User.query.filter_by(email=email).first()

        except:

            flash('Please check your login credentials.', 'error')
            return redirect(url_for('core.sign_in'))

        else:

            if this_user == None:

                flash('Such a user does not exist.', 'error')
                return redirect(url_for('core.sign_in'))

            if this_user.email != os.environ.get('ADMIN_EMAIL'):
                
                flash('You are not the site admin!', 'error')
                return redirect(url_for('core.sign_in'))
            
            if not check_password_hash(this_user.password, password):

                flash('Please check you password and try again.', 'error')
                return redirect(url_for('core.sign_in'))

            login_user(this_user, remember=remember)

            flash("Logged in successfully.", "message")
            return redirect(url_for('core.admin'))

    return render_template('admin/sign_in.html')

@bp.route('/sign_out/')
def sign_out():

    logout_user()

    flash("Logged out successfully.", "message")
    return redirect(url_for('core.sign_in'))