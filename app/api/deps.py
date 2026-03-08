from typing import Generator, Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import UnauthorizedException, ForbiddenException, NotFoundException
from app.db.session import SessionLocal
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.token import TokenPayload

# Use HTTPBearer for simple JSON web token handling.
# This replaces the complex OAuth2PasswordBearer form.
reusable_oauth2 = HTTPBearer()

def get_db() -> Generator:
    """
    Dependency function to get a database session per request.
    It yields a session object to be used locally within an endpoint,
    and ensures it's closed correctly afterward (the 'finally' block).
    """
    db = SessionLocal()
    try:
        # yield suspends execution so the FastAPI endpoint can run.
        # After the endpoint returns a response (or throws an exception), execution resumes here.
        yield db
    finally:
        # Always close the session to release the connection back to the pool!
        db.close()

def get_current_user(
    db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Depends(reusable_oauth2)
) -> User:
    """
    Dependency function to verify a JWT token and extract the currently authenticated User.
    """
    try:
        # We attempt to decode the token. Settings specifies algorithm and secret.
        # token.credentials contains the actual string token passed in the Authorization header.
        payload = jwt.decode(
            token.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        # We parse the decoded dictionary into a Pydantic TokenPayload schema class.
        token_data = TokenPayload(**payload)
        
    except (jwt.PyJWTError, ValidationError):
        # If token decoding fails (expired, invalid signature, etc.) OR
        # if the decoded format is invalid (ValidationError), throw a 401 error.
        raise UnauthorizedException(detail="Could not validate credentials")

    # The 'sub' field of the token holds the User's ID
    user_repo = UserRepository(db)
    user = user_repo.get_by_id(user_id=token_data.sub)
    
    # If the token contains a User ID but no such user exists (e.g., they were deleted)
    if not user:
         raise NotFoundException(detail="User not found")
         
    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Further refines get_current_user by ensuring the user is explicitly marked 'active'.
    Use this dependency for most endpoints instead of plain get_current_user.
    """
    if not current_user.is_active:
        raise ForbiddenException(detail="Inactive user")
    return current_user
