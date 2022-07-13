from project import ma


class HistorySchema(ma.Schema):
    """Schema defining the attributes of a history."""
    user_agent = ma.Dict()
    ip = ma.String()
    created = ma.DateTime()
    expires_at = ma.DateTime()
