from project import ma


class HistorySchema(ma.Schema):
    """Schema defining the attributes of a history."""
    activity = ma.Dict()
    created = ma.DateTime()
