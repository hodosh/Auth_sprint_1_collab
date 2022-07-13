from flask import jsonify, Blueprint
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

example_blueprint = Blueprint('test', __name__)


@example_blueprint.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
