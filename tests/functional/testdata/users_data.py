import uuid

session_uuid = uuid.uuid4()

register_data = {
  "password": "password",
  "password_confirm": "password",
  "email": f"{session_uuid}@admin.admin"
}

passwords_mismatch_data = {
  "password": "1",
  "password_confirm": "2",
  "email": f"{session_uuid}@admin.admin"
}

register_base_data = {
  "password": "password",
  "password_confirm": "password",
  "email": "user@admin.admin"
}
