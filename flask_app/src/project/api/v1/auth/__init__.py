"""
The 'session_api' blueprint handles the API for managing auth.
Specifically, this blueprint allows login, logout and refresh token operations.
"""
from flask import Blueprint

auth_api_blueprint = Blueprint('auth', __name__, template_folder='templates')

from . import routes
