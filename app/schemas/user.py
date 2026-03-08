from typing import Optional
from pydantic import BaseModel, EmailStr

# -----------------
# Shared Properties
# -----------------
# These properties are common across multiple schemas (creation, updating, reading)

class UserBase(BaseModel):
    # We use EmailStr to ensure the input is exactly a valid email address.
    # It requires the 'email-validator' package (often comes with pydantic
    # or requires installation depending on the Pydantic version and setup).
    email: EmailStr
    is_active: Optional[bool] = True

# -----------------
# Creation Schema
# -----------------
# When a client wants to create a User, they MUST provide a password.
# However, this password should NEVER be returned when reading User info.
class UserCreate(UserBase):
    password: str

# -----------------
# Update Schema
# -----------------
# When updating, all fields are optional. A client might only update one field.
class UserUpdate(UserBase):
    password: Optional[str] = None

# -----------------
# Properties shared by models stored in DB
# -----------------
# This is used for data returned by our API.
class UserInDBBase(UserBase):
    id: int

    class Config:
        # 'orm_mode=True' (in Pydantic v1) or 'from_attributes=True' (in v2)
        # tells the Pydantic model to read the data even if it is not a dict,
        # but an ORM model (i.e. object attributes).
        from_attributes = True

# -----------------
# Response Schema
# -----------------
# Properties to return to client (doesn't include hashed_password).
class UserResponse(UserInDBBase):
    pass

# -----------------
# Internal DB Schema
# -----------------
# Properties stored in DB, including the hashed password (used internally).
class UserInDB(UserInDBBase):
    hashed_password: str
