from flask_app_old.src.models.base import ORJSONModel


class Message(ORJSONModel):
    head: str
    body: str
