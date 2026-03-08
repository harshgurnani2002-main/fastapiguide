from fastapi import HTTPException, status

class NotFoundException(HTTPException):
    """
    Base exception for when a requested resource is not found (404).
    """
    def __init__(self, detail: str):
         # We initialize the parent HTTPException with the respective status code
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class BadRequestException(HTTPException):
    """
    Base exception for bad requests to the server (400), like missing parameters
    or trying an operation that is logically invalid.
    """
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class UnauthorizedException(HTTPException):
    """
    Exception raised when authentication fails (401), e.g., missing or invalid JWT.
    
    We include the 'WWW-Authenticate' header as the HTTP standard requires for 401.
    """
    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

class ForbiddenException(HTTPException):
    """
    Exception raised when an authenticated user attempts to access a resource
    they do not have permission for (403). For example, modifying another user's Todo.
    """
    def __init__(self, detail: str = "Not enough permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )
