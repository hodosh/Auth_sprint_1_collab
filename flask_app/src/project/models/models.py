import secrets
import uuid
from datetime import datetime, timedelta

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from werkzeug.security import check_password_hash, generate_password_hash

from project import database


# ----------------
# Mixin  Classes
# ----------------


class IDMixin(object):
    id = database.Column(UUID(as_uuid=True),
                         primary_key=True,
                         default=uuid.uuid4,
                         unique=True, nullable=False)


class CreatedMixin(object):
    created = database.Column(database.DateTime,
                              default=func.now())


class CreatedModifiedMixin(CreatedMixin):
    modified = database.Column(database.DateTime,
                               server_default=func.now(),
                               onupdate=func.current_timestamp())


# ----------------
# Data  Classes
# ----------------
class User(IDMixin, CreatedModifiedMixin, database.Model):
    __tablename__ = 'users'

    email = database.Column(database.String,
                            unique=True,
                            nullable=False)

    password_hashed = database.Column(database.String(128),
                                      nullable=False)

    entries = database.relationship('Entry',
                                    backref='user',
                                    lazy='dynamic')

    auth_token = database.Column(database.String(64),
                                 index=True)

    auth_token_expiration = database.Column(database.DateTime)

    roles = database.relationship('Role',
                                  secondary='role_permission',
                                  back_populates='roles')

    def __init__(self, email: str, password_plaintext: str):
        """Create a new User object."""
        self.email = email
        self.password_hashed = self._generate_password_hash(password_plaintext)

    def is_password_correct(self, password_plaintext: str):
        return check_password_hash(self.password_hashed, password_plaintext)

    def set_password(self, password_plaintext: str):
        self.password_hashed = self._generate_password_hash(password_plaintext)

    @staticmethod
    def _generate_password_hash(password_plaintext):
        return generate_password_hash(password_plaintext)

    def generate_auth_token(self):
        self.auth_token = secrets.token_urlsafe()
        self.auth_token_expiration = datetime.utcnow() + timedelta(minutes=60)
        return self.auth_token

    @staticmethod
    def verify_auth_token(auth_token):
        user = User.query.filter_by(auth_token=auth_token).first()
        if user and user.auth_token_expiration > datetime.utcnow():
            return user

    def revoke_auth_token(self):
        self.auth_token_expiration = datetime.utcnow()

    def __repr__(self):
        return f'<User: {self.email}>'


class Role(IDMixin, CreatedModifiedMixin, database.Model):
    __tablename__ = 'roles'

    name = database.Column(database.String,
                           unique=True,
                           nullable=False)

    permissions = database.relationship('Permission',
                                        secondary='role_permission',
                                        back_populates='permissions')

    users = database.relationship('User',
                                  secondary='user_role',
                                  back_populates='users')

    def __init__(self, name: str):
        """Create a new Role object."""
        self.name = name

    def __repr__(self):
        return f'<Role {self.name}>'


class Permission(IDMixin, database.Model):
    __tablename__ = 'permissions'

    name = database.Column(database.String,
                           unique=True,
                           nullable=False)

    roles = database.relationship('Permission', secondary='role_permission', back_populates='roles')

    def __repr__(self):
        return f'<Permission {self.name}>'


class RolePermission(IDMixin, CreatedMixin, database.Model):
    __tablename__ = 'role_permission'

    role_id = database.Column(UUID(as_uuid=True),
                              database.ForeignKey('roles.id'),
                              nullable=False,
                              index=True)

    permission_id = database.Column(UUID(as_uuid=True),
                                    database.ForeignKey('permissions.id'),
                                    nullable=False,
                                    index=True)

    enabled = database.Column(database.Boolean,
                              unique=True,
                              nullable=False)

    def __init__(self, role_id: str, permission_id: str, enabled: bool = True):
        """Create a new RolePermission object."""
        self.role_id = role_id
        self.permission_id = permission_id
        self.enabled = enabled

    def __repr__(self):
        return f'<RolePermission {self.id}>'


class UserRole(IDMixin, CreatedMixin, database.Model):
    __tablename__ = 'user_role'

    role_id = database.Column(UUID(as_uuid=True),
                              database.ForeignKey('roles.id'),
                              nullable=False,
                              index=True)

    user_id = database.Column(UUID(as_uuid=True),
                              database.ForeignKey('users.id'),
                              nullable=False,
                              index=True)

    def __init__(self, role_id: str, user_id: str):
        self.role_id = role_id
        self.user_id = user_id

    def __repr__(self):
        return f'<UserRole {self.id}>'


class UserHistory(IDMixin, CreatedMixin, database.Model):
    __tablename__ = 'user_history'

    user_id = database.Column(UUID(as_uuid=True),
                              database.ForeignKey('users.id', ondelete='CASCADE'),
                              nullable=False,
                              index=True)

    activity = database.Column(database.String,
                               unique=True,
                               nullable=False)

    def __init__(self, user_id: str, activity: str):
        self.user_id = user_id
        self.activity = activity

    def __repr__(self):
        return f'<UserHistory {self.id}>'
