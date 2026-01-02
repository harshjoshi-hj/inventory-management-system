def can_edit(role):
    return role in ("admin", "user")

def can_delete(role):
    return role == "admin"

def can_manage_users(role):
    return role == "admin"