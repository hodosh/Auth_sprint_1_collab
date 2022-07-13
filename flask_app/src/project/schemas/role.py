from project import ma


class PermissionSchema(ma.Schema):
    name = ma.String()


class ShortRoleSchema(ma.Schema):
    name = ma.String()


class RoleSchema(ma.Schema):
    name = ma.String()
    permissions = ma.List(PermissionSchema)
    created = ma.DateTime()


class NewRoleSchema(ma.Schema):
    name = ma.String()
    permissions = ma.List(PermissionSchema)
