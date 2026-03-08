from typing import Optional
from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.models.user import User
from app.repositories.user import UserRepository

class AuthService:
    """
    Service layer for authentication-related business logic.
    It takes the database session, initializes the necessary repositories,
    and performs the required workflows.
    """

    def __init__(self, session: Session):
        self.session = session
        self.user_repo = UserRepository(session)

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Authenticates a user based on their email and password.
        """
        
        # 1. Look up the user by email
        user = self.user_repo.get_by_email(email=email)
        if not user:
            # User not found
            return None
            
        # 2. Verify the provided password against the hashed password
        if not verify_password(password, user.hashed_password):
            # Password doesn't match
            return None
            
        # 3. If everything is correct, return the authenticated user
        return user
