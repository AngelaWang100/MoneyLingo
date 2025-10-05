from datetime import datetime
from typing import Dict, Optional

USERS_DB: Dict[str, dict] = {}


def get_user_by_email(email: str) -> Optional[dict]:
    return USERS_DB.get(email)

def get_user_by_id(user_id: int) -> Optional[dict]:
    for user in USERS_DB.values():
        if user["user_id"] == user_id:
            return user
    return None

def create_user(email: str, full_name: Optional[str] = None) -> dict:
    user_id = f"usr_{len(USERS_DB) + 1:06d}"
    user = {
        "user_id": user_id,
        "email": email,
        "full_name": full_name,
        "created_at": datetime.utcnow(),
    }
    USERS_DB[email] = user
    return user

