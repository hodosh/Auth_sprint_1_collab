from apifairy import authenticate, body, other_responses, response

from project import basic_auth, database, ma
from project.models.models import User
from . import users_api_blueprint


# -------
# Schemas
# -------

class NewUserSchema(ma.Schema):
    """Schema defining the attributes when creating a new user."""
    email = ma.String()
    password_plaintext = ma.String()


class UserSchema(ma.Schema):
    """Schema defining the attributes of a user."""
    id = ma.Integer()
    email = ma.String()


class TokenSchema(ma.Schema):
    """Schema defining the attributes of a token."""
    token = ma.String()


new_user_schema = NewUserSchema()
user_schema = UserSchema()
token_schema = TokenSchema()


@users_api_blueprint.route('/', methods=['POST'])
@body(new_user_schema)
@response(user_schema, 201)
def register(kwargs):
    """Create a new user"""
    new_user = User(**kwargs)
    database.session.add(new_user)
    database.session.commit()
    return new_user


@users_api_blueprint.route('/get-auth-token', methods=['POST'])
@authenticate(basic_auth)
@response(token_schema)
@other_responses({401: 'Invalid username or password'})
def get_auth_token():
    """Get authentication token"""
    user = basic_auth.current_user()
    token = user.generate_auth_token()
    database.session.add(user)
    database.session.commit()
    return dict(token=token)