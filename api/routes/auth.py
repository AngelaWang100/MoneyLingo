from fastapi import APIRouter, HTTPException, status
from api.models.user import LoginRequest, LoginResponse
from api.services.auth_service import (
    exchange_auth0_code,
    verify_auth0_token,
    create_access_token
)
from api.services.user_service import get_or_create_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    User login via Auth0 only.
    Expects an Auth0 authorization code.
    """
    if not request.auth_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="auth_code is required for Auth0 login"
        )
    
    # Exchange Auth0 code for tokens
    auth0_data = await exchange_auth0_code(request.auth_code)
    user_info = await verify_auth0_token(auth0_data["access_token"])
    email = user_info["email"]

    # Get or create user
    user = get_or_create_user(email)

    # Generate JWT token
    access_token, expires_in = create_access_token(user["user_id"], email)

    return LoginResponse(
        access_token=access_token,
        expires_in=expires_in,
        user_id=user["user_id"]
    )


