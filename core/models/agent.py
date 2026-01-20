"""
Agent model - Represents a sales agent
"""
from datetime import datetime
from core.database import db


class Agent:
    """Sales Agent Model"""
    
    @staticmethod
    def create(agent_id, name, email, monthly_target, company_id, area_manager_id=None):
        """Create a new agent"""
        agent = {
            "_id": agent_id,
            "name": name,
            "email": email,
            "monthly_target": monthly_target,
            "company_id": company_id,  # Multi-tenant support
            "area_manager_id": area_manager_id,
            "created_at": datetime.now()
        }
        db.agents.insert_one(agent)
        
        # Update subscription agent count
        from core.models.subscription import Subscription
        Subscription.update_agent_count(company_id)
        
        return agent
    
    @staticmethod
    def get(agent_id):
        """Get agent by ID"""
        return db.agents.find_one({"_id": agent_id})
    
    @staticmethod
    def get_all(company_id=None):
        """Get all agents, optionally filtered by company"""
        query = {}
        if company_id:
            query["company_id"] = company_id
        return list(db.agents.find(query))
    
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
        agent = Agent.get(agent_id)
        result = db.agents.delete_one({"_id": agent_id})
        
        # Update subscription agent count
        if agent and "company_id" in agent:
            from core.models.subscription import Subscription
            Subscription.update_agent_count(agent["company_id"])
        
        return result
    
    @staticmethod
    def exists(agent_id):
        """Check if agent exists"""
        return db.agents.count_documents({"_id": agent_id}) > 0
    
    @staticmethod
    def get_by_area_manager(area_manager_id):
        """Get all agents under a specific area manager"""
        return list(db.agents.find({"area_manager_id": area_manager_id}))
    
    @staticmethod
    def get_by_company(company_id):
        """Get all agents for a specific company"""
        return list(db.agents.find({"company_id": company_id}))
