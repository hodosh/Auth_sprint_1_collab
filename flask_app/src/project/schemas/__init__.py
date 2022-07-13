from project.schemas.session import HistorySchema
from project.schemas.token import TokenSchema
from project.schemas.user import NewUserSchema, UserSchema

new_user_schema = NewUserSchema()
user_schema = UserSchema()
token_schema = TokenSchema()
history_schema = HistorySchema()
