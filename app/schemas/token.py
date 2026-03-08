from typing import Optional
from pydantic import BaseModel

# -----------------
# Token Response Schema
# -----------------
# Represents the JSON payload returned upon successful login
class Token(BaseModel):
    # The actual JWT token string
    access_token: str
    
    # The type of token. Standard is "bearer" for OAuth2.
    token_type: str

# -----------------
# Token Payload Schema
# -----------------
# Used to extract and validate the data (payload) stored inside a decoded JWT.
class TokenPayload(BaseModel):
    # 'sub' (subject) typically holds the user ID.
    sub: Optional[int] = None
