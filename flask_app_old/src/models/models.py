# flask_api/dm_models.py
import uuid

from sqlalchemy import Column, DateTime, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from db.db import db
from sqlalchemy.sql import func


class IDMixin(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)


class CreatedMixin(object):
    created = Column(DateTime, default=func.now())


class CreatedModifiedMixin(CreatedMixin):
    modified = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())


class User(IDMixin, CreatedModifiedMixin):
    __tablename__ = 'users'

    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    inactive = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<User {self.email}>'


class Role(IDMixin, CreatedModifiedMixin):
    __tablename__ = 'role'

    name = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'


class Permission(IDMixin):
    __tablename__ = 'permission'

    name = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'


class RolePermission(IDMixin, CreatedMixin):
    __tablename__ = 'role_permission'

    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Permission.id', ondelete='CASCADE'), nullable=False,
                        index=True)
    permission_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Role.id', ondelete='CASCADE'), nullable=False,
                              index=True)
    value = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.value}>'


class UserHistory(IDMixin):
    __tablename__ = 'user_history'

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('User.id', ondelete='CASCADE'), nullable=False, index=True)

    def __repr__(self):
        return f'<User {self.value}>'
