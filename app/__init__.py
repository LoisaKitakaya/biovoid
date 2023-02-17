import re
import click
from uuid import uuid4
from werkzeug.security import generate_password_hash

# flask and app factory config
from flask import Flask
from config import Config

# extensions
from app.extensions import db, migrate, login_manager

# blueprints
from app.core import bp as main_blueprint
from app.site import bp as site_blueprint

# app models
from app.models.users import User
from app.models.art import Image

def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)

    # initialize flask extension here
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # register blueprints here
    app.register_blueprint(main_blueprint)
    app.register_blueprint(site_blueprint)

    # create superuser custom command
    @app.cli.command("createsuperuser")
    def create_superuser():

        name = click.prompt("Enter superuser name")
        email = click.prompt("Enter superuser email")
        password = click.prompt("Enter superuser password", hide_input=True)
        password_2 = click.prompt("Confirm superuser password", hide_input=True)

        if not re.search("(^\w+)@([a-z]+)[.]([a-z]+\S)$", email):

            return click.secho("Invalid email address format", fg="red")

        if password != password_2:

            return click.secho("Passwords do not match", fg="red")

        if len(password) < 8 and len(password_2) < 8:

            return click.secho("Passwords must be at least 8 characters", fg="red")

        super_user = User(
            username=name,
            email=email,
            public_id=str(uuid4().hex),
            password=generate_password_hash(password, method='sha256'),
            role="superuser"
        )

        try:

            db.session.add(super_user)

        except:

            click.secho('Something went wrong', fg="red")
            return None

        else:

            db.session.commit()
            click.secho('User created successfully', fg="green")

     # login manager callback
    @login_manager.user_loader
    def load_user(id):

        return User.query.get(int(id))

    return app