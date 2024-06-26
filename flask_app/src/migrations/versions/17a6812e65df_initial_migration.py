"""Initial migration.

Revision ID: 17a6812e65df
Revises: 
Create Date: 2022-07-22 21:47:57.851617

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '17a6812e65df'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('permissions',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('roles',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modified', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('role_permission',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('role_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('permission_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('value', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modified', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password_hashed', sa.String(length=128), nullable=False),
    sa.Column('auth_token', sa.String(length=64), nullable=True),
    sa.Column('auth_token_expiration', sa.DateTime(), nullable=True),
    sa.Column('disabled', sa.Boolean(), nullable=False),
    sa.Column('role_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_users_auth_token'), 'users', ['auth_token'], unique=False)
    op.create_table('user_history',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('activity', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_user_history_user_id'), 'user_history', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_history_user_id'), table_name='user_history')
    op.drop_table('user_history')
    op.drop_index(op.f('ix_users_auth_token'), table_name='users')
    op.drop_table('users')
    op.drop_table('role_permission')
    op.drop_table('roles')
    op.drop_table('permissions')
    # ### end Alembic commands ###
