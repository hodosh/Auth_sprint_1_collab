from http import HTTPStatus

from apifairy import response, body
from flask import abort, request
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, current_user

from project.core.config import ACCESS_EXPIRES
from project.extensions import jwt_redis_blocklist
from project.models.models import User
from project.schemas import token_schema, message_schema, login_schema
from . import session_api_blueprint


@session_api_blueprint.route('/login', methods=['POST'])
@body(login_schema)
@response(token_schema)
def login(kwargs):
    email = kwargs['email']
    password = kwargs['password']
    user = User.query.filter_by(email=email).first()

    if not user:
        abort(HTTPStatus.NOT_FOUND, f'user with email={email} not found')

    if not user.is_password_correct(password):
        abort(HTTPStatus.EXPECTATION_FAILED, 'old password is incorrect')

    access_token = create_access_token(identity=email)
    return dict(token=access_token)


@session_api_blueprint.route('/logout', methods=['DELETE'])
@response(message_schema)
def logout():
    jti = get_jwt()['jti']
    jwt_redis_blocklist.set(jti, '', ex=ACCESS_EXPIRES)
    return dict(message='Access token revoked')


# @session_api_blueprint.route('/get-auth-token', methods=['POST'])
# @authenticate(basic_auth)
# @response(token_schema)
# @other_responses({401: 'Invalid username or password'})
# def get_auth_token():
#     """Get authentication token"""
#     user = basic_auth.current_user()
#     token = user.generate_auth_token()
#     database.session.add(user)
#     database.session.commit()
#     return dict(token=token)


@session_api_blueprint.route('/refresh', methods=['POST'])
# @jwt_required()
@response(token_schema, 200)
async def refresh_token_user():
    pass
