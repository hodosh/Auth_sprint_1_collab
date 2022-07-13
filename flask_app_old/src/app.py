from flask import Flask

from flask_app_old.src.api.v1.auth import auth_blueprint
from flask_app_old.src.api.v1.example import example_blueprint
from flask_app_old.src.core import config
from db.db import db
from extensions import jwt


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # jwt
    app.config["JWT_SECRET_KEY"] = "eyJhbGciOiJSUzI1NiIsImNsYXNzaWQiOjQ5Nn0"  # Change this!
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = config.ACCESS_EXPIRES
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = config.REFRESH_EXPIRES

    db.init_app(app=app)
    jwt.init_app(app=app)

    app.register_blueprint(auth_blueprint, url_prefix='/v1/auth')
    app.register_blueprint(example_blueprint, url_prefix='/v1/example')

    return app
