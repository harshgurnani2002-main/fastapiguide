from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base

class User(Base):
    """
    SQLAlchemy User model that represents the 'users' table in the database.
    """
    # The name of the table in the database
    __tablename__ = "users"

    # Columns
    # Primary Key - uniquely identifies each user
    id = Column(Integer, primary_key=True, index=True)
    
    # Email, used as the username for login. Must be unique.
    email = Column(String, unique=True, index=True, nullable=False)
    
    # We store the hashed password, never the plain text password!
    hashed_password = Column(String, nullable=False)
    
    # Simple boolean flag to mark a user as active or inactive
    is_active = Column(Boolean, default=True)

    # Relationships
    # A user can have multiple Todos. 'back_populates' creates a bidirectional
    # relationship. Any Todo will have an 'owner' attribute pointing back here.
    # We also specify 'cascade="all, delete-orphan"' so that if a User is deleted,
    # all of their Todos are also deleted automatically.
    todos = relationship("Todo", back_populates="owner", cascade="all, delete-orphan")
