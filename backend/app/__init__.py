import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import cryptocompare


# instantiate the extensions
db = SQLAlchemy()
cors = CORS()
bcrypt = Bcrypt()


def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    

    app.config.from_object(app_settings)
    cryptocompare.cryptocompare._set_api_key_parameter(app.config["CRYPTOCOMPARE_API_KEY"])
    jwt = JWTManager(app)
    

    # set up extensions
    db.init_app(app)
    cors.init_app(app, resources={r"*": {"origins": "*"}})
    bcrypt.init_app(app)

    # register api
    from app.api import api

    api.init_app(app)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
