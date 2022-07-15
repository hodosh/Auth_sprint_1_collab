import uuid
import secrets
from datetime import datetime, timedelta

from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import func

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


class Entry(IDMixin, database.Model):
    """Class that represents a journal entry."""
    __tablename__ = 'entries'

    entry = database.Column(database.String,
                            nullable=False)

    user_id = database.Column(UUID(as_uuid=True),
                              database.ForeignKey('users.id'))

    def __init__(self, entry: str):
        self.entry = entry

    def update(self, entry: str):
        self.entry = entry

    def __repr__(self):
        return f'<Entry: {self.entry}>'


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

    def __repr__(self):
        return f'<User {self.name}>'


class Permission(IDMixin, database.Model):
    __tablename__ = 'permissions'

    name = database.Column(database.String,
                           unique=True,
                           nullable=False)

    roles = database.relationship('Permission', secondary='role_permission', back_populates='roles')

    def __repr__(self):
        return f'<User {self.name}>'


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

    value = database.Column(database.String,
                            unique=True,
                            nullable=False)

    def __repr__(self):
        return f'<User {self.value}>'


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

    def __repr__(self):
        return f'<User {self.value}>'


class UserHistory(IDMixin, CreatedMixin, database.Model):
    __tablename__ = 'user_history'

    user_id = database.Column(UUID(as_uuid=True),
                              database.ForeignKey('users.id', ondelete='CASCADE'),
                              nullable=False,
                              index=True)

    activity = database.Column(database.String,
                               unique=True,
                               nullable=False)

    def __repr__(self):
        return f'<User {self.value}>'
