"""
MongoDB connection manager
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
    
    def __init__(self):
        if self._client is None:
            self._client = MongoClient(settings.MONGODB_URI)
            self._db = self._client[settings.MONGODB_NAME]
    
    @property
    def db(self):
        return self._db
    
    @property
    def agents(self):
        return self._db.agents
    
    @property
    def activities(self):
        return self._db.activities
    
    @property
    def sales(self):
        return self._db.sales
    
    @property
    def area_managers(self):
        return self._db.area_managers
    
    @property
    def division_heads(self):
        return self._db.division_heads
    
    @property
    def products(self):
        return self._db.products
    
    @property
    def leads(self):
        return self._db.leads
    
    def close(self):
        if self._client:
            self._client.close()


# Singleton instance
db = MongoDB()
