from typing import Generator, Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import UnauthorizedException, ForbiddenException
from app.db.session import SessionLocal
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.token import TokenPayload

# Creates an OAuth2 scheme instance that will look for a Bearer token in the 'Authorization' header.
# "tokenUrl" tells tools like Swagger UI where to send the username/password to get the token.
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/access-token"
)

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
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    """
    Dependency function to verify a JWT token and extract the currently authenticated User.
    It chains two other dependencies:
    1. get_db: to fetch from the database
    2. reusable_oauth2: to extract the raw token string from the request headers
    """
    try:
        # We attempt to decode the token. Settings specifies algorithm and secret.
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
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
