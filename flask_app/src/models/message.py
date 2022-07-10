from flask_app.src.models.base import ORJSONModel


class Message(ORJSONModel):
    head: str
    body: str
