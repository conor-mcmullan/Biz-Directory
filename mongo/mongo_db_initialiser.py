# mongo/db.py

from mongo.mongo_connection import MongoConnection
from mongo.settings import MONGO_HOST, MONGO_PORT, MONGO_DATABASE

# Global reference for mongo_crud
mongo_crud = None

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
        print(f"Database connection failed: {str(e)}")
