"""
Activity model - Represents agent activities (calls, meetings, leads, deals)
"""
from datetime import datetime
from core.database import db


class Activity:
    """Activity Model for tracking calls, meetings, leads, and deals"""
    
    TYPES = ['call', 'meeting', 'lead', 'deal']
    
    @staticmethod
    def create(activity_id, agent_id, company_id, activity_type, value=0, notes=""):
        """Create a new activity"""
        if activity_type not in Activity.TYPES:
            raise ValueError(f"Invalid activity type. Must be one of: {Activity.TYPES}")
        
        activity = {
            "_id": activity_id,
            "agent_id": agent_id,
            "company_id": company_id,  # Multi-tenant support
            "activity_type": activity_type,
            "value": value,
            "created_at": datetime.now(),  # Changed from "date" to "created_at"
            "notes": notes
        }
        db.activities.insert_one(activity)
        return activity
    
    @staticmethod
    def get(activity_id):
        """Get activity by ID"""
        return db.activities.find_one({"_id": activity_id})
    
    @staticmethod
    def get_by_agent(agent_id, activity_type=None, start_date=None, end_date=None):
        """Get activities for a specific agent"""
        query = {"agent_id": agent_id}
        
        if activity_type:
            query["activity_type"] = activity_type
        
        if start_date or end_date:
            date_query = {}
            if start_date:
                date_query["$gte"] = start_date
            if end_date:
                date_query["$lte"] = end_date
            query["created_at"] = date_query  # Changed from "date" to "created_at"
        
        return list(db.activities.find(query))
    
    @staticmethod
    def count_by_agent(agent_id, activity_type=None, start_date=None, end_date=None):
        """Count activities for a specific agent"""
        query = {"agent_id": agent_id}
        
        if activity_type:
            query["activity_type"] = activity_type
        
        if start_date or end_date:
            date_query = {}
            if start_date:
                date_query["$gte"] = start_date
            if end_date:
                date_query["$lte"] = end_date
            query["created_at"] = date_query  # Changed from "date" to "created_at"
        
        return db.activities.count_documents(query)
    
    @staticmethod
    def delete(activity_id):
        """Delete an activity"""
        return db.activities.delete_one({"_id": activity_id})
