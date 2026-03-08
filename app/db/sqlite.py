from sqlalchemy import event
from sqlalchemy.engine import Engine

# SQLite does not enforce foreign key constraints by default.
# Foreign keys are critical for data integrity (e.g., a Todo MUST belong
# to an existing User).
# 
# This event listener connects to all SQLAlchemy Engine instances.
# When a connection is created, it executes "PRAGMA foreign_keys=ON"
# which enables foreign key checks in SQLite.
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """
    Enables foreign keys for SQLite databases.
    This hook fires automatically when SQLAlchemy establishes a new connection.
    """
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
