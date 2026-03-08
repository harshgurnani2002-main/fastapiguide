from typing import Optional
from pydantic import BaseModel

# -----------------
# Shared Properties
# -----------------
# Properties common to multiple Todo operations.
class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: Optional[bool] = False

# -----------------
# Creation Schema
# -----------------
# Inherits title from base, meaning title is required.
class TodoCreate(TodoBase):
    pass

# -----------------
# Update Schema
# -----------------
# All fields are optional because a user might only update one field (e.g., just title).
class TodoUpdate(TodoBase):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None

# -----------------
# Properties shared by models stored in DB
# -----------------
class TodoInDBBase(TodoBase):
    id: int
    owner_id: int

    class Config:
        # Allows Pydantic to read data directly from the SQLAlchemy ORM model attributes.
        from_attributes = True

# -----------------
# Response Schema
# -----------------
# Used for returning Todo data to the client.
class TodoResponse(TodoInDBBase):
    pass
