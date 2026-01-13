"""
Area Manager model - Manages multiple sales agents
"""
from datetime import datetime
from core.database import db


class AreaManager:
    """Area Manager Model - Supervises multiple agents"""
    
    @staticmethod
    def create(manager_id, name, email, division_head_id, area_name):
        """Create a new area manager"""
        manager = {
            "_id": manager_id,
            "name": name,
            "email": email,
            "division_head_id": division_head_id,
            "area_name": area_name,
            "created_at": datetime.now()
        }
        db.area_managers.insert_one(manager)
        return manager
    
    @staticmethod
    def get(manager_id):
        """Get area manager by ID"""
        return db.area_managers.find_one({"_id": manager_id})
    
    @staticmethod
    def get_all():
        """Get all area managers"""
        return list(db.area_managers.find())
    
    @staticmethod
    def get_by_division_head(division_head_id):
        """Get all area managers under a division head"""
        return list(db.area_managers.find({"division_head_id": division_head_id}))
    
    @staticmethod
    def update(manager_id, **kwargs):
        """Update area manager information"""
        return db.area_managers.update_one(
            {"_id": manager_id},
            {"$set": kwargs}
        )
    
    @staticmethod
    def delete(manager_id):
        """Delete an area manager"""
        return db.area_managers.delete_one({"_id": manager_id})
    
    @staticmethod
    def exists(manager_id):
        """Check if area manager exists"""
        return db.area_managers.count_documents({"_id": manager_id}) > 0
