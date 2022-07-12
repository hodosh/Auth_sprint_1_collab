import datetime

from flask import Flask

from api.v1.auth import auth_blueprint
from api.v1.example import example_blueprint
from core.config import *
from db.db import db
from extensions import jwt


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # jwt
    app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = datetime.timedelta(days=30)

    db.init_app(app=app)
    jwt.init_app(app=app)

    app.register_blueprint(auth_blueprint, url_prefix='/v1/auth')
    app.register_blueprint(example_blueprint, url_prefix='/v1/example')

    return app
