from project.schemas.message import MessageSchema
from project.schemas.role import (
    RoleSchema,
    NewRoleSchema,
    PermissionSchema,
)
from project.schemas.session import HistorySchema, LoginSchema
from project.schemas.token import TokenSchema
from project.schemas.user import (
    NewUserSchema,
    UserSchema,
    UpdateUserSchema,
    UserRole,
)

new_user_schema = NewUserSchema()
update_user_schema = UpdateUserSchema()
user_schema = UserSchema()
user_role_schema = UserRole()

token_schema = TokenSchema()

login_schema = LoginSchema()
history_schema = HistorySchema()

role_schema = RoleSchema()
new_role_schema = NewRoleSchema()
permission_schema = PermissionSchema()

message_schema = MessageSchema()
