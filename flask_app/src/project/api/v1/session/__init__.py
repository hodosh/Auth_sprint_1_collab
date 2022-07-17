"""
The 'session_api' blueprint handles the API for managing session.
Specifically, this blueprint allows login, logout and refresh token operations.
"""
from flask import Blueprint

session_api_blueprint = Blueprint('session', __name__, template_folder='templates')

from . import routes
