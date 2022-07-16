from project.core.roles import DEFAULT_ROLES
from project.core.permissions import USER_SELF, USER_ALL, ROLE_SELF, ROLE_ALL, PERMISSION, DEFAULT_PERMISSIONS
from project.models.models import User, Role, Permission, RolePermission

from project import database, ma, token_auth


def create_default():
    create_permissions()
    create_empty_roles()
    fill_roles()

def create_permissions():
    for key, value in DEFAULT_PERMISSIONS.items():
        for permit in value:
            try:
                permission_item = Permission(name=permit.value)
                database.session.add(permission_item)
                database.session.commit()
            except Exception:
                pass


def create_empty_roles():
    for key, value in DEFAULT_ROLES.items():
        try:
            role_item = Role(name=key)
            database.session.add(role_item)
            database.session.commit()
        except Exception:
            pass


def fill_roles():
    for role_key, role_value in DEFAULT_ROLES.items():
        role = database.session.query(Role).filter(Role.name == role_key).first()
        for permission_key, permission_value in role_value.items():
            try:
                permission = database.session.query(Permission).filter(Permission.name == permission_key.value).first()
                print(permission.name)
                assoc = RolePermission(role_id=role.id, permission_id=permission.id, value=permission_value)
                print(assoc)
                database.session.add(assoc)
                # database.session.commit()
            except Exception:
                pass

    database.session.commit()


