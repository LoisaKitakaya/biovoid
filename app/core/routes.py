import re
from uuid import uuid4
from app.core import bp
from app.extensions import db
from app.models.art import Image
from app.models.users import User
from app.core.decorators import admin_required
from app.models.subscription import Account, Payment
from flask import render_template, redirect, url_for, flash, request
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from app.core.handle_payment import convert_currency, mpesa_payment, payment_status

ACCOUNT_MANAGEMENT = {
    "free_account": {
        "tier": "Free",
        "max_count": 5,
        "max_images": 1,
        "quality": "256x256"
    },
    "basic_account": {
        "tier": "Basic",
        "max_count": 10,
        "max_images": 2,
        "quality": "512x512"
    },
    "standard_account": {
        "tier": "Standard",
        "max_count": 25,
        "max_images": 3,
        "quality": "512x512"
    },
    "pro_account": {
        "tier": "Pro",
        "max_count": 40,
        "max_images": 4,
        "quality": "1024x1024"
    }
}

@bp.route('/admin/', methods=['GET', 'POST'])
@login_required
@admin_required
def admin():

    users = User.query.all()
    images = Image.query.all()
    accounts = Account.query.all()
    account_payments = Payment.query.all()
    user_account = Account.query.filter_by(user_id=current_user.id).first()

    return render_template(
        'admin/admin.html',
        this_user=current_user,
        this_account=user_account,
        all_users=users,
        all_accounts=accounts,
        all_payments=account_payments,
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
        
@bp.route("/delete_user/<public_id>/")
def delete_user(public_id):

    user = User.query.filter_by(public_id=public_id).first()
    account = Account.query.filter_by(user_id=user.id).first()

    try:

        db.session.delete(account)

    except Exception as e:

        flash(f"Error: {str(e)}", "error")
        return redirect(url_for('core.admin'))
    
    else:

        db.session.commit()

        flash("User account deleted successfully.", "message")

    try:

        db.session.delete(user)

    except Exception as e:

        flash(f"Error: {str(e)}", "error")
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

@bp.route('/payment/<package>/', methods=['GET', 'POST'])
@login_required
def payment(package):

    user_account = Account.query.filter_by(user_id=current_user.id).first()

    page = package

    if package == "free":

        amount = convert_currency(0)

    elif package == "basic":

        amount = convert_currency(2)

    elif package == "standard":

        amount = convert_currency(3)

    elif package == "pro":

        amount = convert_currency(6)

    if request.method == 'POST':

        if package == "free":

            user_account.subscription = ACCOUNT_MANAGEMENT["free_account"]['tier']
            user_account.generation_count = 0

            try:

                db.session.commit()

            except Exception as e:

                flash(f"Error: {str(e)}", "error")
                return None

            else:

                flash("You are now subscribed to the Free tier", "message")
                return redirect(url_for('core.payment', package=package))

        elif package == "basic":

            mpesa_number = request.form.get('mpesa_number')
            country_code = "254"
            full_number = country_code + mpesa_number

            transaction = mpesa_payment(
                tel_number=full_number,
                amount=amount
            )

            if transaction:

                register_payment = Payment(
                    public_id=str(uuid4().hex),
                    account_id = user_account.id,
                    transaction_id = transaction['invoice']['invoice_id'],
                    provider = transaction['invoice']['provider'],
                    state = transaction['invoice']['state'],
                    amount = int(transaction['invoice']['net_amount']),
                    payed_by = transaction['customer']['phone_number'],
                )

                try:

                    db.session.add(register_payment)

                except Exception as e:

                    flash(f"Error: {str(e)}", "error")
                    return None
                
                else:

                    db.session.commit()
                    
                return redirect(url_for('core.processing', package=package))
            
            else:

                flash("Could not process payment")
                return redirect(url_for('core.payment', package=package))

        elif package == "standard":

            mpesa_number = request.form.get('mpesa_number')
            country_code = "254"
            full_number = country_code + mpesa_number

            transaction = mpesa_payment(
                tel_number=full_number,
                amount=amount
            )

            if transaction:

                register_payment = Payment(
                    public_id=str(uuid4().hex),
                    account_id = user_account.id,
                    transaction_id = transaction['invoice']['invoice_id'],
                    provider = transaction['invoice']['provider'],
                    state = transaction['invoice']['state'],
                    amount = int(transaction['invoice']['net_amount']),
                    payed_by = transaction['customer']['phone_number'],
                )

                try:

                    db.session.add(register_payment)

                except Exception as e:

                    flash(f"Error: {str(e)}", "error")
                    return None
                
                else:

                    db.session.commit()
                    
                return redirect(url_for('core.processing', package=package))
            
            else:

                flash("Could not process payment")
                return redirect(url_for('core.payment', package=package))

        elif package == "pro":

            mpesa_number = request.form.get('mpesa_number')
            country_code = "254"
            full_number = country_code + mpesa_number

            transaction = mpesa_payment(
                tel_number=full_number,
                amount=amount
            )

            if transaction:

                register_payment = Payment(
                    public_id=str(uuid4().hex),
                    account_id = user_account.id,
                    transaction_id = transaction['invoice']['invoice_id'],
                    provider = transaction['invoice']['provider'],
                    state = transaction['invoice']['state'],
                    amount = int(transaction['invoice']['net_amount']),
                    payed_by = transaction['customer']['phone_number'],
                )

                try:

                    db.session.add(register_payment)

                except Exception as e:

                    flash(f"Error: {str(e)}", "error")
                    return None
                
                else:

                    db.session.commit()
                    
                return redirect(url_for('core.processing', package=package))
            
            else:

                flash("Could not process payment")
                return redirect(url_for('core.payment', package=package))

    return render_template(
        'site/payment.html',
        this_user=current_user,
        this_account=user_account,
        this_amount=amount,
        this_page=page,
    )

@bp.route('/processing/<package>/', methods=['GET'])
@login_required
def processing(package):

    user_account = Account.query.filter_by(user_id=current_user.id).first()
    user_payment = Payment.query.filter_by(account_id=user_account.id).\
        order_by(Payment.id.desc()).first()

    page = package
    process_state = "processing"

    if package == "free":

        pass

    elif package == "basic":

        process_payment = payment_status(invoice_id=user_payment.transaction_id)

        print(process_payment)

        user_account.subscription = ACCOUNT_MANAGEMENT["basic_account"]['tier']
        user_account.generation_count = 0

        try:

            db.session.commit()

        except Exception as e:

            flash(f"Error: {str(e)}", "error")
            return None

        else:

            flash("You are now subscribed to the Basic tier", "message")

    elif package == "standard":

        process_payment = payment_status(invoice_id=user_payment.transaction_id)

        print(process_payment)

        user_account.subscription = ACCOUNT_MANAGEMENT["standard_account"]['tier']
        user_account.generation_count = 0

        try:

            db.session.commit()

        except Exception as e:

            flash(f"Error: {str(e)}", "error")
            return None

        else:

            flash("You are now subscribed to the Standard tier", "message")

    elif package == "pro":

        process_payment = payment_status(invoice_id=user_payment.transaction_id)

        print(process_payment)

        user_account.subscription = ACCOUNT_MANAGEMENT["pro_account"]['tier']
        user_account.generation_count = 0

        try:

            db.session.commit()

        except Exception as e:

            flash(f"Error: {str(e)}", "error")
            return None

        else:

            flash("You are now subscribed to the Pro tier", "message")

    return render_template(
        'site/processing.html',
        this_user=current_user,
        this_account=user_account,
        this_page=page,
        this_state=process_state,
    )