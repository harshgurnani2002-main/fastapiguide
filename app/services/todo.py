from typing import List
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException, ForbiddenException
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate
from app.repositories.todo import TodoRepository

class TodoService:
    """
    Service layer for Todo-related business logic.
    It handles validation and authorization before passing data to the repository.
    """

    def __init__(self, session: Session):
        self.session = session
        self.todo_repo = TodoRepository(session)

    def get_user_todos(self, owner_id: int, skip: int = 0, limit: int = 100) -> List[Todo]:
        """
        Retrieves todos for a specific user.
        """
        return self.todo_repo.get_multi_by_owner(owner_id=owner_id, skip=skip, limit=limit)

    def create_user_todo(self, owner_id: int, todo_in: TodoCreate) -> Todo:
        """
        Creates a new todo for a specific user.
        """
        return self.todo_repo.create_with_owner(obj_in=todo_in, owner_id=owner_id)

    def update_user_todo(self, owner_id: int, todo_id: int, todo_in: TodoUpdate) -> Todo:
        """
        Updates a user's todo. Checks if it exists and belongs to the user first.
        """
        # First, retrieve the Todo and ensure it belongs to the user
        db_todo = self.todo_repo.get_by_id_and_owner(todo_id=todo_id, owner_id=owner_id)
        if not db_todo:
            # If it's none, either it doesn't exist or isn't owned by this user
            raise NotFoundException(detail="Todo not found")
            
        # Update and return
        return self.todo_repo.update(db_obj=db_todo, obj_in=todo_in)

    def delete_user_todo(self, owner_id: int, todo_id: int) -> Todo:
        """
        Deletes a user's todo. Checks ownership first.
        """
        # Retrieve and check ownership
        db_todo = self.todo_repo.get_by_id_and_owner(todo_id=todo_id, owner_id=owner_id)
        if not db_todo:
            raise NotFoundException(detail="Todo not found")
            
        # Delete and return (the deleted item, useful for confirmation)
        return self.todo_repo.remove(db_obj=db_todo)
