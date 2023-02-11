from flask import Flask

from config import Config

def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)

    # initialize flask extension here

    # register blueprints here

    @app.route('/hello/')
    def hello():
        return 'Hello World!'

    return app