# api/db.py

from mongo.mongo_connection import MongoConnection
from mongo.settings import MONGO_HOST, MONGO_PORT, MONGO_DATABASE, LONG_ERROR_MESSAGES

# Global reference for mongo_crud
mongo_crud = None

class DatabaseConnectionError(Exception):
    """Custom exception for database connection errors."""
    def __init__(self, message, host, port, long_message=False):
        super().__init__(message)
        self.host = host
        self.port = port
        self.long_message = long_message
        self.short_error_message = f"Check if MongoDB is running on {self.host}:{self.port}."

    def __str__(self):
        if self.long_message:
            # Return a long error message
            return (f"{super().__str__()}\n{self.short_error_message}")
        else:
            # Return a short error message
            return self.short_error_message

def initialize():
    global mongo_crud
    try:
        # Establish the connection once when the app starts
        mongo_conn = MongoConnection().connect(
            host=MONGO_HOST,
            port=MONGO_PORT,
            db_name=MONGO_DATABASE    
        )
        from mongo.mongo_crud import MongoCRUD
        mongo_crud = MongoCRUD(mongo_conn)
    except ConnectionError as e:
        # Raise custom error with host and port information; set long_message as needed
        raise DatabaseConnectionError(
            f"Database connection failed: {str(e)}", 
            MONGO_HOST, 
            MONGO_PORT, 
            long_message=LONG_ERROR_MESSAGES
        )
