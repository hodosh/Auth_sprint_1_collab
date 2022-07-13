import rich
from rich.prompt import Prompt
from rich.pretty import pprint

from validators.password import PasswordValidator
from validators.email import EmailValidator


def create_new_user() -> bool:
    email = Prompt.ask("Enter your email")
    password1 = Prompt.ask("Enter password", password=True)
    password2 = Prompt.ask("Enter password again", password=True)

    if not EmailValidator.validate(email=email):
        pprint("Email is non valid")
        return False

    if not PasswordValidator.validate(password1=password1, password2 = password2):
        pprint("Password dont match")
        return False

#     --------------- TODO: CREATE NEW USER HERE ---------------

    pprint("new user created")
    return True


if __name__ == '__main__':
    create_new_user()

