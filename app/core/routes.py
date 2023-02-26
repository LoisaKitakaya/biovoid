import re
from uuid import uuid4
from app.core import bp
from app.extensions import db
from app.models.art import Image
from app.models.users import User
from app.models.subscription import Account, Payment
from app.core.decorators import admin_required
from flask import render_template, redirect, url_for, flash, request
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user

@bp.route('/admin/', methods=['GET', 'POST'])
@login_required
@admin_required
def admin():

    users = User.query.all()
    images = Image.query.all()
    accounts = Account.query.all()
    user_account = Account.query.filter_by(user_id=current_user.id).first()

    return render_template(
        'admin/admin.html',
        this_user=current_user,
        this_account=user_account,
        all_users=users,
        all_accounts=accounts,
        gallery=images,
    )

@bp.route('/sign_up/', methods=['GET', 'POST'])
def sign_up():

    if request.method == 'POST':

        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_2 = request.form.get('password_2')

        if not re.search("(^\w+)@([a-z]+)[.]([a-z]+\S)$", email):

            flash("Invalid email address format.", "error")
            return redirect(url_for('core.sign_up'))

        if password != password_2:

            flash("Passwords don't match", "error")
            return redirect(url_for('core.sign_up'))

        if len(password) < 8 and len(password_2) < 8:

            flash("Passwords much be at least 8 characters.", "error")
            return redirect(url_for('core.sign_up'))

        user = User(
            username=username,
            email=email,
            public_id=str(uuid4().hex),
            password=generate_password_hash(password, method='sha256')
        )

        try:

            db.session.add(user)

        except Exception as e:

            flash(f"Error: {str(e)}.", "error")
            return redirect(url_for('core.sign_up'))

        else:

            db.session.commit()

            flash("User created successfully.", "message")

            this_user = User.query.filter_by(email=email).first()

            user_account = Account(
                public_id=str(uuid4().hex),
                user_id=this_user.id
            )

            try:

                db.session.add(user_account)

            except Exception as e:

                flash(f"Error: {str(e)}", "error")
                return redirect(url_for('core.sign_up'))
            
            else:

                db.session.commit()
                flash("User account created successfully.", "message")
                return redirect(url_for('core.sign_in'))
        
    return render_template('admin/sign_up.html')

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
            
            if not check_password_hash(this_user.password, password):

                flash('Please check you password and try again.', 'error')
                return redirect(url_for('core.sign_in'))

            login_user(this_user, remember=remember)

            flash("Logged in successfully.", "message")
            return redirect(url_for('site.home'))

    return render_template('admin/sign_in.html')

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

        except Exception as e:

            flash(f"Error: {str(e)}", "error")
            return redirect(url_for('core.admin'))

        else:

            db.session.commit()

            flash("User created successfully.", "message")
            
            this_user = User.query.filter_by(email=email).first()

            user_account = Account(
                public_id=str(uuid4().hex),
                user_id=this_user.id
            )

            try:

                db.session.add(user_account)

            except Exception as e:

                flash(f"Error: {str(e)}", "error")
                return redirect(url_for('core.admin'))
            
            else:

                db.session.commit()
                flash("User account created successfully.", "message")
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
    
@bp.route('/sign_out/')
def sign_out():

    logout_user()

    flash("Logged out successfully.", "message")
    return redirect(url_for('core.sign_in'))