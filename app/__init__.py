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

    return app