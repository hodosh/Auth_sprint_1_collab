from rich.prompt import Prompt
from rich.pretty import pprint

from project.validators.password import PasswordValidator
from project.validators.email import EmailValidator
from project.core.roles import ROLE_SUPERUSER
from project.models.models import User, Role

from project import database


def create_superuser() -> bool:
    email = Prompt.ask("Enter your email")
    password1 = Prompt.ask("Enter password", password=True)
    password2 = Prompt.ask("Enter password again", password=True)

    if not EmailValidator.validate(email=email):
        pprint("Email is non valid")
        return False

    if not PasswordValidator.validate(password1=password1, password2=password2):
        pprint("Password dont match")
        return False

    role_superuser = database.session.query(Role).filter(Role.name == ROLE_SUPERUSER).first()
    new_user = User(email=email, password_plaintext=password1, role_id=role_superuser.id)
    database.session.add(new_user)
    database.session.commit()

    pprint("New user created")
    return True
