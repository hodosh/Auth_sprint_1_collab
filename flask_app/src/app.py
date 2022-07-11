from flask import Flask

from core.config import *
from db.db import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app=app)


def main(flask_app):
    flask_app.run(debug=True, host='0.0.0.0', port=5001)


if __name__ == '__main__':
    main(app)