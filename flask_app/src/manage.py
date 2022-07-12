import sys
from console.user import create_new_user


def main():
    if (sys.argv[1] == "superuser"):
        create_new_user()


if __name__ == '__main__':
    main()
