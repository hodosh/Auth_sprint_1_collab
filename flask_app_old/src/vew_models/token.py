from flask_app_old.src.models.base import ORJSONModel


class AccessToken(ORJSONModel):
    access_token: str


class RefreshToken(ORJSONModel):
    refresh_token: str


class TokenPair(AccessToken, RefreshToken):
    pass
