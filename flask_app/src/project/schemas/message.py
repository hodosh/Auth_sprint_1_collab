from project import ma


class MessageSchema(ma.Schema):
    head = ma.String()
    body = ma.String()
