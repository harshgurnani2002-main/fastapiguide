from typing import Any
from sqlalchemy.orm import declarative_base

# The declarative_base() factory function returns a base class. 
# All of our SQLAlchemy models will inherit from this Base class, 
# which allows SQLAlchemy to track them and create tables accordingly.
Base = declarative_base()
