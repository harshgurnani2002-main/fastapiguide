from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate

class TodoRepository:
    """
    Repository for encapsulating database operations related to the Todo model.
    """

    def __init__(self, session: Session):
        # Inject the db session
        self.session = session

    def get_multi_by_owner(
        self, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Todo]:
        """
        Retrieves a list of Todo items belonging to a specific user (owner_id).
        Supports pagination via 'skip' and 'limit'.
        """
        return (
            self.session.query(Todo)
            .filter(Todo.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id_and_owner(self, todo_id: int, owner_id: int) -> Optional[Todo]:
        """
        Retrieves a specific Todo by its ID, ensuring it belongs to the given owner.
        This provides a layer of security at the DB level.
        """
        return (
            self.session.query(Todo)
            .filter(Todo.id == todo_id, Todo.owner_id == owner_id)
            .first()
        )

    def create_with_owner(self, obj_in: TodoCreate, owner_id: int) -> Todo:
        """
        Creates a new Todo item and assigns it to an owner.
        """
        # Convert the Pydantic schema to a dictionary
        obj_in_data = obj_in.model_dump() # Note: .model_dump() is for Pydantic v2 (use .dict() for v1)
        
        # Create the SQLAlchemy model instance
        db_todo = Todo(**obj_in_data, owner_id=owner_id)
        
        self.session.add(db_todo)
        self.session.commit()
        self.session.refresh(db_todo)
        
        return db_todo

    def update(self, db_obj: Todo, obj_in: TodoUpdate) -> Todo:
        """
        Updates an existing Todo item.
        """
        # Extract only the fields that were provided in the request
        update_data = obj_in.model_dump(exclude_unset=True)
        
        # Apply changes to the SQLAlchemy model
        for field, value in update_data.items():
            setattr(db_obj, field, value)
            
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        
        return db_obj

    def remove(self, db_obj: Todo) -> Todo:
        """
        Deletes a Todo item from the database.
        """
        self.session.delete(db_obj)
        self.session.commit()
        return db_obj
