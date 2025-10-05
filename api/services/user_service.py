from fastapi import HTTPException, status
from typing import Optional
from api.database.db import(
    get_user_by_email,
    create_user,
    get_user_by_id
)

def get_or_create_user(email: str, full_name: Optional[str] = None) -> dict:
    user = get_user_by_email(email)
    if user:
        return user
    return create_user(email, full_name)
