from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api import deps
from app.core.config import settings
from app.core.security import create_access_token
from app.core.exceptions import BadRequestException
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserResponse
from app.services.auth import AuthService
from app.repositories.user import UserRepository

# An APIRouter groups related endpoints together.
router = APIRouter()

@router.post("/access-token", response_model=Token)
def login_access_token(
    # Depends injects the database session and the parsed OAuth2 form data
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, getting an access token for future requests.
    This is the endpoint we configured 'reusable_oauth2' to point to in deps.py.
    """
    auth_service = AuthService(db)
    
    # 1. Authenticate user
    user = auth_service.authenticate_user(form_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
        
    # 2. Setup token expiration
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # 3. Generate and return the JWT token
    return {
        "access_token": create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    *, # Forces keyword arguments for following parameters
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
) -> Any:
    """
    Register a new user.
    """
    user_repo = UserRepository(db)
    
    # 1. Check if the email is already in use
    user = user_repo.get_by_email(email=user_in.email)
    if user:
        raise BadRequestException(
            detail="The user with this username already exists in the system.",
        )
        
    # 2. Create the user in the database
    user = user_repo.create(user_in=user_in)
    return user

@router.post("/test-token", response_model=UserResponse)
def test_token(
    # This dependency ensures the user is logged in
    # AND passes the User model to the 'current_user' variable.
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Test endpoint to verify access token works. returns the current user.
    """
    return current_user
