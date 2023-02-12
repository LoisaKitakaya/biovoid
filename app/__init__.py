import re
import click

# flask
from flask import Flask

# app factory config
from config import Config

# extensions
from app.extensions import db, migrate

# app models
from app.models.users import User

def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)

    # initialize flask extension here
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints here
    from app.core import bp as main_blueprint
    
    app.register_blueprint(main_blueprint)

    @app.cli.command("createsuperuser")
    def create_superuser():

        name = click.prompt("Enter superuser name")
        email = click.prompt("Enter superuser email")
        password = click.prompt("Enter superuser password", hide_input=True)
        password_2 = click.prompt("Confirm superuser password", hide_input=True)

        if not re.search("(^\w+)@([a-z]+)[.]([a-z]+\S)$", email):

            click.secho("Invalid email address", fg="red")

        if password != password_2:

            click.secho("Passwords do not match", fg="red")

        if len(password) < 8 and len(password_2) < 8:

            click.secho("Passwords must be at least 8 characters", fg="red")

    return app