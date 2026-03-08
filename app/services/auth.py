from typing import Optional
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

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

    def authenticate_user(self, form_data: OAuth2PasswordRequestForm) -> Optional[User]:
        """
        Authenticates a user based on OAuth2 form data (username and password).
        In OAuth2, 'username' is the standard field, but we mapped it to 'email'
        in our mental model, so form_data.username will contain the user's email.
        """
        
        # 1. Look up the user by email (using the username field from form)
        user = self.user_repo.get_by_email(email=form_data.username)
        if not user:
            # User not found
            return None
            
        # 2. Verify the provided password against the hashed password
        if not verify_password(form_data.password, user.hashed_password):
            # Password doesn't match
            return None
            
        # 3. If everything is correct, return the authenticated user
        return user
