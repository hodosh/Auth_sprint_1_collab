from project import ma


class HistorySchema(ma.Schema):
    activity = ma.String()
    created = ma.DateTime()


class LoginSchema(ma.Schema):
    email = ma.String()
    password = ma.String()
