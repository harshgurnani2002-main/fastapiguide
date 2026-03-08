from typing import Any, List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.schemas.todo import TodoCreate, TodoResponse, TodoUpdate
from app.services.todo import TodoService

router = APIRouter()

@router.get("/", response_model=List[TodoResponse])
def read_todos(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve todos for the current user. Supports pagination via skip/limit parameters.
    """
    todo_service = TodoService(db)
    # Notice we pass current_user.id to ensure users only get THEIR todos
    todos = todo_service.get_user_todos(owner_id=current_user.id, skip=skip, limit=limit)
    return todos


@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    *,
    db: Session = Depends(deps.get_db),
    todo_in: TodoCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a new todo for the current user.
    """
    todo_service = TodoService(db)
    todo = todo_service.create_user_todo(owner_id=current_user.id, todo_in=todo_in)
    return todo


@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(
    *,
    db: Session = Depends(deps.get_db),
    todo_id: int,
    todo_in: TodoUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a todo by its ID. Users can only update their own todos.
    """
    todo_service = TodoService(db)
    # The service layer handles finding the todo and checking if the user owns it
    # If not found or not owned, it throws a 404 Exception.
    todo = todo_service.update_user_todo(
        owner_id=current_user.id, todo_id=todo_id, todo_in=todo_in
    )
    return todo


@router.delete("/{todo_id}", response_model=TodoResponse)
def delete_todo(
    *,
    db: Session = Depends(deps.get_db),
    todo_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a todo by its ID. Users can only delete their own todos.
    """
    todo_service = TodoService(db)
    todo = todo_service.delete_user_todo(owner_id=current_user.id, todo_id=todo_id)
    return todo
