"""
The 'journal_api' blueprint handles the API for managing journal entries.
Specifically, this blueprint allows for journal entries to be added, edited,
and deleted.
"""
from flask import Blueprint

session_api_blueprint = Blueprint('session', __name__, template_folder='templates')

from . import routes
