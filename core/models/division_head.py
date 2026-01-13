"""
Division Head model - Oversees multiple area managers
"""
from datetime import datetime
from core.database import db


class DivisionHead:
    """Division Head Model - Oversees multiple area managers"""
    
    @staticmethod
    def create(head_id, name, email, division_name):
        """Create a new division head"""
        head = {
            "_id": head_id,
            "name": name,
            "email": email,
            "division_name": division_name,
            "created_at": datetime.now()
        }
        db.division_heads.insert_one(head)
        return head
    
    @staticmethod
    def get(head_id):
        """Get division head by ID"""
        return db.division_heads.find_one({"_id": head_id})
    
    @staticmethod
    def get_all():
        """Get all division heads"""
        return list(db.division_heads.find())
    
    @staticmethod
    def update(head_id, **kwargs):
        """Update division head information"""
        return db.division_heads.update_one(
            {"_id": head_id},
            {"$set": kwargs}
        )
    
    @staticmethod
    def delete(head_id):
        """Delete a division head"""
        return db.division_heads.delete_one({"_id": head_id})
    
    @staticmethod
    def exists(head_id):
        """Check if division head exists"""
        return db.division_heads.count_documents({"_id": head_id}) > 0
