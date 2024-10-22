from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class MongoConnection:
    _instance = None
    _client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoConnection, cls).__new__(cls)
        return cls._instance

    def connect(self, host: str = 'localhost', port: int = 27017, db_name: str = 'biz_directory', uri: str = None):
        """
        Connect to MongoDB using either a URI or separate host, port, and db_name parameters.
        If a URI is provided, it will override the host, port, and db_name parameters.
        """
        if self._client is None:
            try:
                # Use the URI if provided, otherwise construct a MongoDB URI from host, port, and db_name
                if uri:
                    self._client = MongoClient(uri)
                else:
                    self._client = MongoClient(f'mongodb://{host}:{port}/')
                
                # Attempt to fetch the server status to check the connection
                self._client.admin.command('ping')
                self.db = self._client[db_name]  # This creates the db instance
                print(f"Connected to database: {db_name} at {host}:{port}")
            except ConnectionFailure as e:
                raise ConnectionError(f"Cannot connect to MongoDB: {str(e)}")
        
        return self.db  # Return the MongoDB database instance

    def get_db(self):
        if self._client is not None:
            return self.db
        else:
            raise ConnectionError("MongoDB connection is not established.")
