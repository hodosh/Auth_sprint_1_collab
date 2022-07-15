from flask import Blueprint

role_api_blueprint = Blueprint('role', __name__, template_folder='templates')

from . import routes
