from project import ma


class NewUserSchema(ma.Schema):
    """Schema defining the attributes when creating a new user."""
    email = ma.String()
    password = ma.String()
    password_confirm = ma.String()


class UserSchema(ma.Schema):
    """Schema defining the attributes of a user."""
    id = ma.Integer()
    email = ma.String()
