import click
from flask import Flask

from config import Config
from app.extensions import db, migrate

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

    return app