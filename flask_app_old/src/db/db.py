# flask_app_old/db.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_app_old.src.core.config import SQLALCHEMY_DATABASE_URI

db = SQLAlchemy()


def init_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    db.init_app(app)
