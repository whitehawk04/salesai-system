"""
MongoDB connection manager with lazy initialization
"""
from pymongo import MongoClient
from django.conf import settings


class MongoDB:
    _instance = None
    _client = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDB, cls).__new__(cls)
        return cls._instance
    
    def _ensure_connection(self):
        """Lazy initialization of MongoDB connection"""
        if self._client is None:
            # Simple connection - let pymongo handle SSL automatically
            # MongoDB Atlas connection strings include SSL by default
            self._client = MongoClient(
                settings.MONGODB_URI,
                serverSelectionTimeoutMS=10000,  # 10 second timeout
                connectTimeoutMS=20000,  # 20 second connection timeout
                socketTimeoutMS=20000,   # 20 second socket timeout
            )
            self._db = self._client[settings.MONGODB_NAME]
    
    @property
    def db(self):
        self._ensure_connection()
        return self._db
    
    @property
    def agents(self):
        self._ensure_connection()
        return self._db.agents
    
    @property
    def activities(self):
        self._ensure_connection()
        return self._db.activities
    
    @property
    def sales(self):
        self._ensure_connection()
        return self._db.sales
    
    @property
    def area_managers(self):
        self._ensure_connection()
        return self._db.area_managers
    
    @property
    def division_heads(self):
        self._ensure_connection()
        return self._db.division_heads
    
    @property
    def products(self):
        self._ensure_connection()
        return self._db.products
    
    @property
    def leads(self):
        self._ensure_connection()
        return self._db.leads
    
    def close(self):
        if self._client:
            self._client.close()


# Singleton instance - connection is created lazily on first use
db = MongoDB()
