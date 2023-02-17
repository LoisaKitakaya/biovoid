from functools import wraps
from flask_login import current_user
from flask import redirect, url_for, flash

def admin_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if current_user.role == "superuser":

            return func(*args, **kwargs)
        
        else:

            flash("You are not authorized to access this page.", "error")
            return redirect(url_for("site.home"))
        
    return wrapper

