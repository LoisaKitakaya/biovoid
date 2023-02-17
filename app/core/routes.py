import os
import re
from uuid import uuid4
from app.core import bp
from app.extensions import db
from app.models.art import Image
from app.models.users import User
from flask import render_template, redirect, url_for, flash, request
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user

@bp.route('/', methods=['GET'])
def home():

    return render_template('home.html')

@bp.route('/admin/', methods=['GET', 'POST'])
@login_required
def admin():

    users = User.query.all()
    images = Image.query.all()

    return render_template(
        'admin/admin.html',
        super_user=current_user,
        all_users=users,
        gallery=images,
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

@bp.route('/create_user/', methods=['GET', 'POST'])
def create_user():

    if request.method == 'POST':

        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_2 = request.form.get('password_2')

        if not re.search("(^\w+)@([a-z]+)[.]([a-z]+\S)$", email):

            flash("Invalid email address format.", "error")
            return redirect(url_for('core.admin'))

        if password != password_2:

            flash("Passwords don't match", "error")
            return redirect(url_for('core.admin'))

        if len(password) < 8 and len(password_2) < 8:

            flash("Passwords much be at least 8 characters.", "error")
            return redirect(url_for('core.admin'))

        super_user = User(
            username=username,
            email=email,
            public_id=str(uuid4().hex),
            password=generate_password_hash(password, method='sha256')
        )

        try:

            db.session.add(super_user)

        except:

            flash("Something went wrong.", "error")
            return redirect(url_for('core.admin'))

        else:

            db.session.commit()

            flash("User created successfully.", "message")
            return redirect(url_for('core.admin'))
        
@bp.route("/delete_user/<public_id>/", methods=['GET', 'POST'])
def delete_user(public_id):

    user = User.query.filter_by(public_id=public_id).first()

    try:

        db.session.delete(user)

    except:

        flash("Something went wrong.", "error")
        return redirect(url_for('core.admin'))
    
    else:

        db.session.commit()

        flash("User deleted successfully.", "message")
        return redirect(url_for('core.admin'))

@bp.route('/generate_image/', methods=['GET', 'POST'])
def generate_image():

    pass