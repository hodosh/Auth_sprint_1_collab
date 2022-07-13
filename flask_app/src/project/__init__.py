from apifairy import APIFairy
from flask import Flask, json
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.exceptions import HTTPException

from project.core import config
# -------------
# Configuration
# -------------

# Create the instances of the Flask extensions in the global scope,
# but without any arguments passed in. These instances are not
# attached to the Flask application at this point.
apifairy = APIFairy()
ma = Marshmallow()
database = SQLAlchemy()
migrate = Migrate()
basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

# ------------


def get_api_url():
    return f"http://{config.FLASK_HOST}:{config.FLASK_PORT}/v1"


# ----------------------------
# Application Factory Function
# ----------------------------

def create_app():
    # Create the Flask application
    app = Flask(__name__)

    # Configure the API documentation
    app.config['APIFAIRY_TITLE'] = config.PROJECT_NAME
    app.config['APIFAIRY_VERSION'] = '0.1'
    app.config['APIFAIRY_UI'] = 'swagger_ui'

    # Configure the PG DB
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    initialize_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)

    return app


# ----------------
# Helper Functions
# ----------------

def initialize_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    apifairy.init_app(app)
    ma.init_app(app)
    database.init_app(app)

    import project.models
    migrate.init_app(app, database)


def register_blueprints(app):
    # Import the blueprints
    from project.api.v1.journal import journal_api_blueprint
    from project.api.v1.users import users_api_blueprint

    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    app.register_blueprint(journal_api_blueprint, url_prefix='/api/v1/journal')
    app.register_blueprint(users_api_blueprint, url_prefix='/api/v1/users')


def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        # Start with the correct headers and status code from the error
        response = e.get_response()
        # Replace the body with JSON
        response.data = json.dumps({
            'code': e.code,
            'name': e.name,
            'description': e.description,
        })
        response.content_type = 'application/json'
        return response
