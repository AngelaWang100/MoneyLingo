from fastapi import APIRouter, Depends
from api.models.user import UserProfile
from api.dependencies.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserProfile)
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    """Get authenticated user's profile"""
    return UserProfile(**current_user)
