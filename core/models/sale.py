"""
Sale model - Represents completed sales
"""
from datetime import datetime
from core.database import db


class Sale:
    """Sale Model for tracking completed sales"""
    
    @staticmethod
    def create(sale_id, agent_id, amount, customer, product_id=None, notes=""):
        """Create a new sale"""
        sale = {
            "_id": sale_id,
            "agent_id": agent_id,
            "amount": amount,
            "customer": customer,
            "product_id": product_id,
            "date": datetime.now(),
            "notes": notes
        }
        db.sales.insert_one(sale)
        return sale
    
    @staticmethod
    def get(sale_id):
        """Get sale by ID"""
        return db.sales.find_one({"_id": sale_id})
    
    @staticmethod
    def get_by_agent(agent_id, start_date=None, end_date=None):
        """Get sales for a specific agent"""
        query = {"agent_id": agent_id}
        
        if start_date or end_date:
            date_query = {}
            if start_date:
                date_query["$gte"] = start_date
            if end_date:
                date_query["$lte"] = end_date
            query["date"] = date_query
        
        return list(db.sales.find(query))
    
    @staticmethod
    def get_total_by_agent(agent_id, start_date=None, end_date=None):
        """Get total sales amount for a specific agent"""
        query = {"agent_id": agent_id}
        
        if start_date or end_date:
            date_query = {}
            if start_date:
                date_query["$gte"] = start_date
            if end_date:
                date_query["$lte"] = end_date
            query["date"] = date_query
        
        pipeline = [
            {"$match": query},
            {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
        ]
        
        result = list(db.sales.aggregate(pipeline))
        return result[0]["total"] if result else 0
    
    @staticmethod
    def delete(sale_id):
        """Delete a sale"""
        return db.sales.delete_one({"_id": sale_id})
