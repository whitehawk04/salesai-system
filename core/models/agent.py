"""
Agent model - Represents a sales agent
"""
from datetime import datetime
from core.database import db


class Agent:
    """Sales Agent Model"""
    
    @staticmethod
    def create(agent_id, name, email, monthly_target, area_manager_id=None):
        """Create a new agent"""
        agent = {
            "_id": agent_id,
            "name": name,
            "email": email,
            "monthly_target": monthly_target,
            "area_manager_id": area_manager_id,
            "created_at": datetime.now()
        }
        db.agents.insert_one(agent)
        return agent
    
    @staticmethod
    def get(agent_id):
        """Get agent by ID"""
        return db.agents.find_one({"_id": agent_id})
    
    @staticmethod
    def get_all():
        """Get all agents"""
        return list(db.agents.find())
    
    @staticmethod
    def update(agent_id, **kwargs):
        """Update agent information"""
        return db.agents.update_one(
            {"_id": agent_id},
            {"$set": kwargs}
        )
    
    @staticmethod
    def delete(agent_id):
        """Delete an agent"""
        return db.agents.delete_one({"_id": agent_id})
    
    @staticmethod
    def exists(agent_id):
        """Check if agent exists"""
        return db.agents.count_documents({"_id": agent_id}) > 0
    
    @staticmethod
    def get_by_area_manager(area_manager_id):
        """Get all agents under a specific area manager"""
        return list(db.agents.find({"area_manager_id": area_manager_id}))
