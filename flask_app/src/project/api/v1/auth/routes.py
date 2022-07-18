from http import HTTPStatus

from apifairy import response, body
from flask import abort
from flask_jwt_extended import create_access_token, get_jwt, jwt_required

from project.core.config import ACCESS_EXPIRES
from project.extensions import jwt_redis_blocklist, log_activity
from project.models.models import User
from project.schemas import token_schema, message_schema, login_schema
from . import auth_api_blueprint


@auth_api_blueprint.route('/login', methods=['POST'])
@body(login_schema)
@response(token_schema)
def login(kwargs):
    email = kwargs['email']
    password = kwargs['password']
    user = User.query.filter_by(email=email, disabled=False).first()

    if not user:
        abort(HTTPStatus.NOT_FOUND, f'user with email={email} not found')

    if not user.is_password_correct(password):
        abort(HTTPStatus.EXPECTATION_FAILED, 'old password is incorrect')

    access_token = create_access_token(identity=email)
    log_activity(user.id, 'login')
    return dict(token=access_token)


@auth_api_blueprint.route('/logout', methods=['DELETE'])
@jwt_required()
@response(message_schema)
def logout():
    jwt = get_jwt()
    jti = jwt['jti']
    jwt_redis_blocklist.set(jti, '', ex=ACCESS_EXPIRES)
    email = jwt['sub']
    user = User.query.filter_by(email=email).first()

    if not user:
        abort(HTTPStatus.NOT_FOUND, f'user with email={email} not found')
    log_activity(user.id, 'login')
    return dict(message='Access token revoked')
