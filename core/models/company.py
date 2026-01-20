"""
Company model - Represents a subscribing organization (multi-tenant)
Each company is a separate customer that subscribes to the system
"""
from datetime import datetime
from core.database import db


class Company:
    """Company Model - Multi-tenant organization"""
    
    @staticmethod
    def create(company_id, name, email, phone, address, 
               tin=None, business_type=None, contact_person=None):
        """Create a new company"""
        company = {
            "_id": company_id,
            "name": name,
            "email": email,
            "phone": phone,
            "address": address,
            "tin": tin,  # Tax Identification Number (BIR requirement in PH)
            "business_type": business_type,
            "contact_person": contact_person,
            "status": "active",  # active, suspended, cancelled
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        db.companies.insert_one(company)
        return company
    
    @staticmethod
    def get(company_id):
        """Get company by ID"""
        return db.companies.find_one({"_id": company_id})
    
    @staticmethod
    def get_by_email(email):
        """Get company by email"""
        return db.companies.find_one({"email": email})
    
    @staticmethod
    def get_all(status=None):
        """Get all companies, optionally filtered by status"""
        query = {}
        if status:
            query["status"] = status
        return list(db.companies.find(query))
    
    @staticmethod
    def update(company_id, **kwargs):
        """Update company information"""
        kwargs["updated_at"] = datetime.now()
        return db.companies.update_one(
            {"_id": company_id},
            {"$set": kwargs}
        )
    
    @staticmethod
    def suspend(company_id, reason=None):
        """Suspend a company (e.g., non-payment)"""
        return db.companies.update_one(
            {"_id": company_id},
            {"$set": {
                "status": "suspended",
                "suspended_at": datetime.now(),
                "suspension_reason": reason,
                "updated_at": datetime.now()
            }}
        )
    
    @staticmethod
    def activate(company_id):
        """Activate or reactivate a company"""
        return db.companies.update_one(
            {"_id": company_id},
            {"$set": {
                "status": "active",
                "updated_at": datetime.now()
            },
            "$unset": {
                "suspended_at": "",
                "suspension_reason": ""
            }}
        )
    
    @staticmethod
    def cancel(company_id, reason=None):
        """Cancel a company subscription"""
        return db.companies.update_one(
            {"_id": company_id},
            {"$set": {
                "status": "cancelled",
                "cancelled_at": datetime.now(),
                "cancellation_reason": reason,
                "updated_at": datetime.now()
            }}
        )
    
    @staticmethod
    def delete(company_id):
        """Delete a company (use with caution - consider soft delete instead)"""
        return db.companies.delete_one({"_id": company_id})
    
    @staticmethod
    def exists(company_id):
        """Check if company exists"""
        return db.companies.count_documents({"_id": company_id}) > 0
    
    @staticmethod
    def get_agent_count(company_id):
        """Get the number of active agents for a company"""
        return db.agents.count_documents({"company_id": company_id})
    
    @staticmethod
    def get_statistics(company_id):
        """Get company statistics"""
        return {
            "total_agents": db.agents.count_documents({"company_id": company_id}),
            "total_area_managers": db.area_managers.count_documents({"company_id": company_id}),
            "total_division_heads": db.division_heads.count_documents({"company_id": company_id}),
            "total_sales": db.sales.count_documents({"company_id": company_id}),
            "total_leads": db.leads.count_documents({"company_id": company_id})
        }
