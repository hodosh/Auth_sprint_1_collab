import redis
from flask_jwt_extended import JWTManager

from project import token_auth, database
from project.core import config
from project.models.models import UserHistory

jwt = JWTManager()

jwt_redis_blocklist = redis.StrictRedis(
    host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB, decode_responses=True
)


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None


def log_activity(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        user = token_auth.current_user()
        user_history = UserHistory(user_id=user.id, activity=func.__name__)

        database.session.add(user_history)
        database.session.commit()
        return result

    return wrapper
