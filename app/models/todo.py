from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base

class Todo(Base):
    """
    SQLAlchemy Todo model that represents the 'todos' table in the database.
    """
    __tablename__ = "todos"

    # Columns
    id = Column(Integer, primary_key=True, index=True)
    
    # The title of the Todo item
    title = Column(String, index=True, nullable=False)
    
    # Optional detailed description
    description = Column(String, index=True)
    
    # Flag to indicate if the task is completed
    is_completed = Column(Boolean, default=False)
    
    # Foreign Key pointing to the users table.
    # "users.id" references the 'id' column of the 'users' table.
    # This ensures a Todo cannot exist without a valid User.
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationship back to the User model.
    # 'back_populates' links this to the 'todos' attribute on the User model.
    owner = relationship("User", back_populates="todos")
