from datetime import datetime, timedelta
from typing import Any, Union
from passlib.context import CryptContext
import jwt

from app.core.config import settings

# Setup Passlib's CryptContext with the standard 'bcrypt' algorithm.
# This context handles password hashing and verification efficiently and securely.
# Deprecated arg auto is removed.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    """
    Creates a new JSON Web Token (JWT) with an expiration time.
    
    Args:
        subject: The unique identifier for the user (usually their ID or email).
        expires_delta: An optional timedelta object to specify when the token
                       expires. If omitted, uses the default from settings.
                       
    Returns:
        The encoded JWT as a string.
    """
    # Use the expiration time provided, or default to what's in settings.
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    # The payload (data) to encode inside the JWT.
    # 'exp' is a standard JWT claim for expiration time.
    # 'sub' is a standard JWT claim for the subject (the user).
    to_encode = {"exp": expire, "sub": str(subject)}
    
    # Create the token using the secret key and algorithm from our config
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies that a plain text password matches a previously hashed one.
    
    Args:
        plain_password: The unhashed password attempt.
        hashed_password: The hashed password stored in the database.
        
    Returns:
        True if they match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hashes a plain text password using bcrypt.
    
    Args:
        password: The plain text password to hash.
        
    Returns:
        The hashed password string.
    """
    return pwd_context.hash(password)
