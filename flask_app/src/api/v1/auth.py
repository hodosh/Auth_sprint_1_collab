from flask import jsonify, Blueprint
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route("/login", methods=["POST"])
def login():
    access_token = create_access_token(identity="example_user")
    refresh_token = create_refresh_token(identity="example_user")
    return jsonify(access_token=access_token, refresh_token=refresh_token)


@auth_blueprint.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)
