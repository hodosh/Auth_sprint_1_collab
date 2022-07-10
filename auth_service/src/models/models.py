# flask_api/dm_models.py
import uuid
from sqlalchemy.dialects.postgresql import UUID
from models.db import db
from sqlalchemy.sql import func


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=func.now())
    # TODO проверить что при обновлении дата ставитя корректно
    modified = db.Column(db.DateTime, nullable=False, default=func.now(), onupdate=func.now())
    inactive = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<User {self.email}>'


class Role(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=func.now())
    # TODO проверить что при обновлении дата ставитя корректно
    modified = db.Column(db.DateTime, nullable=False, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f'<User {self.name}>'


class Permission(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'


class RolePermission(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Permission.id', ondelete='CASCADE'), nullable=False, index=True)
    permission_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Role.id', ondelete='CASCADE'), nullable=False, index=True)
    created = db.Column(db.DateTime, nullable=False, default=func.now())
    value = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.value}>'


class UserHistory(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('User.id', ondelete='CASCADE'), nullable=False, index=True)

    def __repr__(self):
        return f'<User {self.value}>'


