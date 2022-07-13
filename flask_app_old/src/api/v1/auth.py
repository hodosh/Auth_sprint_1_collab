from flask import jsonify, Blueprint
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt

from flask_app_old.src.core import config
from extensions import jwt_redis_blocklist

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route("/login", methods=["POST"])
def login():
    access_token = create_access_token(identity="example_user")
    refresh_token = create_refresh_token(identity="example_user")
    return jsonify(access_token=access_token, refresh_token=refresh_token)


@auth_blueprint.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(jti, "", ex=config.ACCESS_EXPIRES)
    return jsonify(msg="Access token revoked")


@auth_blueprint.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)
