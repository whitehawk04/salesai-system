"""
Subscription model - Manages company subscriptions with per-agent pricing
"""
from datetime import datetime, timedelta
from core.database import db


class Subscription:
    """Subscription Model - Per-agent pricing for companies"""
    
    # Pricing configuration (in PHP)
    PRICE_PER_AGENT = 500  # ₱500 per agent per month
    
    # Trial configuration
    TRIAL_DAYS = 14
    
    @staticmethod
    def create(subscription_id, company_id, billing_email, 
               trial_enabled=True, price_per_agent=None):
        """Create a new subscription for a company"""
        start_date = datetime.now()
        
        if trial_enabled:
            status = "trial"
            trial_end_date = start_date + timedelta(days=Subscription.TRIAL_DAYS)
            next_billing_date = trial_end_date
        else:
            status = "active"
            trial_end_date = None
            # Next billing date is 1 month from now
            next_billing_date = start_date + timedelta(days=30)
        
        subscription = {
            "_id": subscription_id,
            "company_id": company_id,
            "status": status,  # trial, active, past_due, cancelled, expired
            "billing_email": billing_email,
            "price_per_agent": price_per_agent or Subscription.PRICE_PER_AGENT,
            "start_date": start_date,
            "trial_end_date": trial_end_date,
            "next_billing_date": next_billing_date,
            "current_agent_count": 0,
            "billing_cycle": "monthly",  # monthly, annual
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        db.subscriptions.insert_one(subscription)
        return subscription
    
    @staticmethod
    def get(subscription_id):
        """Get subscription by ID"""
        return db.subscriptions.find_one({"_id": subscription_id})
    
    @staticmethod
    def get_by_company(company_id):
        """Get subscription for a company"""
        return db.subscriptions.find_one({"company_id": company_id})
    
    @staticmethod
    def get_all(status=None):
        """Get all subscriptions, optionally filtered by status"""
        query = {}
        if status:
            query["status"] = status
        return list(db.subscriptions.find(query))
    
    @staticmethod
    def update_agent_count(company_id):
        """Update the agent count for a company's subscription"""
        from core.models.agent import Agent
        
        # Count active agents for this company
        agent_count = db.agents.count_documents({"company_id": company_id})
        
        return db.subscriptions.update_one(
            {"company_id": company_id},
            {"$set": {
                "current_agent_count": agent_count,
                "updated_at": datetime.now()
            }}
        )
    
    @staticmethod
    def calculate_monthly_cost(company_id):
        """Calculate the monthly cost based on current agent count"""
        subscription = Subscription.get_by_company(company_id)
        if not subscription:
            return 0
        
        agent_count = subscription.get("current_agent_count", 0)
        price_per_agent = subscription.get("price_per_agent", Subscription.PRICE_PER_AGENT)
        
        return agent_count * price_per_agent
    
    @staticmethod
    def activate(company_id):
        """Activate a subscription (after trial or payment)"""
        next_billing_date = datetime.now() + timedelta(days=30)
        
        return db.subscriptions.update_one(
            {"company_id": company_id},
            {"$set": {
                "status": "active",
                "next_billing_date": next_billing_date,
                "updated_at": datetime.now()
            }}
        )
    
    @staticmethod
    def mark_past_due(company_id):
        """Mark subscription as past due (payment failed)"""
        return db.subscriptions.update_one(
            {"company_id": company_id},
            {"$set": {
                "status": "past_due",
                "past_due_since": datetime.now(),
                "updated_at": datetime.now()
            }}
        )
    
    @staticmethod
    def cancel(company_id, reason=None, immediate=False):
        """Cancel a subscription"""
        update_data = {
            "status": "cancelled",
            "cancelled_at": datetime.now(),
            "cancellation_reason": reason,
            "updated_at": datetime.now()
        }
        
        if not immediate:
            # Allow access until end of billing period
            subscription = Subscription.get_by_company(company_id)
            if subscription:
                update_data["access_until"] = subscription.get("next_billing_date")
        
        return db.subscriptions.update_one(
            {"company_id": company_id},
            {"$set": update_data}
        )
    
    @staticmethod
    def renew(company_id):
        """Renew subscription for another billing cycle"""
        next_billing_date = datetime.now() + timedelta(days=30)
        
        return db.subscriptions.update_one(
            {"company_id": company_id},
            {"$set": {
                "status": "active",
                "next_billing_date": next_billing_date,
                "updated_at": datetime.now()
            },
            "$unset": {
                "past_due_since": ""
            }}
        )
    
    @staticmethod
    def is_active(company_id):
        """Check if company has an active subscription"""
        subscription = Subscription.get_by_company(company_id)
        if not subscription:
            return False
        
        status = subscription.get("status")
        
        # Trial and active are both considered "active"
        if status in ["trial", "active"]:
            return True
        
        # Check if cancelled but still has access
        if status == "cancelled" and "access_until" in subscription:
            return datetime.now() < subscription["access_until"]
        
        return False
    
    @staticmethod
    def get_expiring_trials(days=3):
        """Get subscriptions with trials expiring in X days"""
        cutoff_date = datetime.now() + timedelta(days=days)
        
        return list(db.subscriptions.find({
            "status": "trial",
            "trial_end_date": {
                "$lte": cutoff_date,
                "$gte": datetime.now()
            }
        }))
    
    @staticmethod
    def check_and_expire_trials():
        """Check for expired trials and update their status"""
        now = datetime.now()
        
        result = db.subscriptions.update_many(
            {
                "status": "trial",
                "trial_end_date": {"$lte": now}
            },
            {"$set": {
                "status": "expired",
                "expired_at": now,
                "updated_at": now
            }}
        )
        
        return result.modified_count
