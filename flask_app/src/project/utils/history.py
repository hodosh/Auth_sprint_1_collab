from project import database, token_auth
from project.models.models import User, UserHistory


def log_activity(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        user_name = token_auth.current_user()
        user = User.query.filter_by(email=user_name).first()
        user_history = UserHistory(user_id=user.id, activity=func.__name__)

        database.session.add(user_history)
        database.session.commit()

    return wrapper
