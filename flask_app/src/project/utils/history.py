from project import database, token_auth
from project.models.models import UserHistory


def log_activity(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        user = token_auth.current_user()
        user_history = UserHistory(user_id=user.id, activity=func.__name__)

        database.session.add(user_history)
        database.session.commit()
        return result

    return wrapper
