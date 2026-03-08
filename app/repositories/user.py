from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

class UserRepository:
    """
    Repository for encapsulating database operations related to the User model.
    This separates the database logic from the business logic (services).
    """

    def __init__(self, session: Session):
        # We inject the SQLAlchemy Session instance here.
        # This keeps the repository stateless and testable.
        self.session = session

    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieves a user by their primary key ID.
        Returns None if no user is found.
        """
        return self.session.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """
        Retrieves a user by their email address.
        Useful for authentication and checking for duplicates during registration.
        """
        return self.session.query(User).filter(User.email == email).first()

    def create(self, user_in: UserCreate) -> User:
        """
        Creates a new User record in the database.
        Note: It handles hashing the password before saving!
        """
        # We don't want to store the plain text password, so we hash it first.
        hashed_password = get_password_hash(user_in.password)
        
        # We manually construct the User object.
        db_user = User(
            email=user_in.email,
            hashed_password=hashed_password,
            is_active=user_in.is_active,
        )
        
        # Add to session, write to DB, and refresh to get the auto-generated ID.
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        
        return db_user
