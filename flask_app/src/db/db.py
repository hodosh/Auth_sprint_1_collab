# flask_app/db.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_app.src.core.config import SQLALCHEMY_DATABASE_URI

db = SQLAlchemy()


def init_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    db.init_app(app)
