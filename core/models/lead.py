"""
Lead model - Sales leads with product interest
"""
from datetime import datetime
from core.database import db


class Lead:
    """Lead Model - Potential customers with product interests"""
    
    @staticmethod
    def create(lead_id, agent_id, company_id, customer_name, contact, product_id, status, value, notes=""):
        """Create a new lead"""
        lead = {
            "_id": lead_id,
            "agent_id": agent_id,
            "company_id": company_id,  # Multi-tenant support
            "customer_name": customer_name,
            "contact": contact,
            "product_id": product_id,
            "status": status,  # "New", "Contacted", "Qualified", "Proposal", "Negotiation", "Won", "Lost"
            "value": value,  # Potential value
            "notes": notes,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        db.leads.insert_one(lead)
        return lead
    
    @staticmethod
    def get(lead_id):
        """Get lead by ID"""
        return db.leads.find_one({"_id": lead_id})
    
    @staticmethod
    def get_by_agent(agent_id):
        """Get all leads for an agent"""
        return list(db.leads.find({"agent_id": agent_id}).sort("created_at", -1))
    
    @staticmethod
    def get_by_status(agent_id, status):
        """Get leads by status for an agent"""
        return list(db.leads.find({"agent_id": agent_id, "status": status}))
    
    @staticmethod
    def update_status(lead_id, status):
        """Update lead status"""
        return db.leads.update_one(
            {"_id": lead_id},
            {"$set": {"status": status, "updated_at": datetime.now()}}
        )
    
    @staticmethod
    def get_all(company_id=None):
        """Get all leads, optionally filtered by company"""
        query = {}
        if company_id:
            query["company_id"] = company_id
        return list(db.leads.find(query))
    
    @staticmethod
    def exists(lead_id):
        """Check if lead exists"""
        return db.leads.count_documents({"_id": lead_id}) > 0
