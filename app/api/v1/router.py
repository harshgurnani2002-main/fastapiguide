from fastapi import APIRouter

from app.api.v1.endpoints import auth, todos

# Creates the main APIRouter for 'v1' of our API
api_router = APIRouter()

# Include the endpoints defined in the individual files,
# prefixing the paths and organizing them under standard tags for swagger docs.
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(todos.router, prefix="/todos", tags=["todos"])
