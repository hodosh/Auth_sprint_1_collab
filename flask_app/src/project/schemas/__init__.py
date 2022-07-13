from project.schemas.role import RoleSchema, NewRoleSchema, PermissionSchema
from project.schemas.session import HistorySchema
from project.schemas.token import TokenSchema
from project.schemas.user import NewUserSchema, UserSchema

new_user_schema = NewUserSchema()
user_schema = UserSchema()
token_schema = TokenSchema()
history_schema = HistorySchema()
role_schema = RoleSchema()
new_role_schema = NewRoleSchema()
permission_schema = PermissionSchema()
