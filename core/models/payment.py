"""
Payment/Invoice model - Tracks payments and billing for subscriptions
"""
from datetime import datetime, timedelta
from core.database import db


class Payment:
    """Payment Model - Tracks invoices and payments"""
    
    # Payment status options
    STATUS_PENDING = "pending"
    STATUS_PAID = "paid"
    STATUS_FAILED = "failed"
    STATUS_REFUNDED = "refunded"
    STATUS_CANCELLED = "cancelled"
    
    # Payment methods
    METHOD_GCASH = "gcash"
    METHOD_PAYMAYA = "paymaya"
    METHOD_BANK_TRANSFER = "bank_transfer"
    METHOD_CREDIT_CARD = "credit_card"
    METHOD_CASH = "cash"
    METHOD_CHECK = "check"
    
    @staticmethod
    def create_invoice(invoice_id, company_id, amount, agent_count, 
                       billing_period_start, billing_period_end, due_date=None):
        """Create a new invoice for a company"""
        if not due_date:
            due_date = datetime.now() + timedelta(days=7)  # 7 days to pay
        
        invoice = {
            "_id": invoice_id,
            "company_id": company_id,
            "invoice_number": invoice_id,
            "amount": amount,
            "agent_count": agent_count,
            "billing_period_start": billing_period_start,
            "billing_period_end": billing_period_end,
            "due_date": due_date,
            "status": Payment.STATUS_PENDING,
            "currency": "PHP",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        db.payments.insert_one(invoice)
        return invoice
    
    @staticmethod
    def record_payment(invoice_id, amount_paid, payment_method, 
                       reference_number=None, notes=None):
        """Record a payment for an invoice"""
        payment_data = {
            "status": Payment.STATUS_PAID,
            "amount_paid": amount_paid,
            "payment_method": payment_method,
            "payment_date": datetime.now(),
            "reference_number": reference_number,
            "payment_notes": notes,
            "updated_at": datetime.now()
        }
        
        return db.payments.update_one(
            {"_id": invoice_id},
            {"$set": payment_data}
        )
    
    @staticmethod
    def mark_failed(invoice_id, reason=None):
        """Mark a payment as failed"""
        return db.payments.update_one(
            {"_id": invoice_id},
            {"$set": {
                "status": Payment.STATUS_FAILED,
                "failure_reason": reason,
                "failed_at": datetime.now(),
                "updated_at": datetime.now()
            }}
        )
    
    @staticmethod
    def get(invoice_id):
        """Get invoice by ID"""
        return db.payments.find_one({"_id": invoice_id})
    
    @staticmethod
    def get_by_company(company_id, status=None, limit=None):
        """Get invoices for a company"""
        query = {"company_id": company_id}
        if status:
            query["status"] = status
        
        cursor = db.payments.find(query).sort("created_at", -1)
        if limit:
            cursor = cursor.limit(limit)
        
        return list(cursor)
    
    @staticmethod
    def get_pending_invoices(company_id=None):
        """Get all pending invoices, optionally for a specific company"""
        query = {"status": Payment.STATUS_PENDING}
        if company_id:
            query["company_id"] = company_id
        
        return list(db.payments.find(query))
    
    @staticmethod
    def get_overdue_invoices(company_id=None):
        """Get overdue invoices (past due date and still pending)"""
        query = {
            "status": Payment.STATUS_PENDING,
            "due_date": {"$lt": datetime.now()}
        }
        if company_id:
            query["company_id"] = company_id
        
        return list(db.payments.find(query))
    
    @staticmethod
    def get_total_revenue(start_date=None, end_date=None):
        """Calculate total revenue from paid invoices"""
        match_query = {"status": Payment.STATUS_PAID}
        
        if start_date or end_date:
            date_query = {}
            if start_date:
                date_query["$gte"] = start_date
            if end_date:
                date_query["$lte"] = end_date
            match_query["payment_date"] = date_query
        
        pipeline = [
            {"$match": match_query},
            {"$group": {"_id": None, "total": {"$sum": "$amount_paid"}}}
        ]
        
        result = list(db.payments.aggregate(pipeline))
        return result[0]["total"] if result else 0
    
    @staticmethod
    def get_company_payment_history(company_id):
        """Get complete payment history for a company"""
        return list(db.payments.find(
            {"company_id": company_id}
        ).sort("created_at", -1))
    
    @staticmethod
    def cancel_invoice(invoice_id, reason=None):
        """Cancel an invoice"""
        return db.payments.update_one(
            {"_id": invoice_id},
            {"$set": {
                "status": Payment.STATUS_CANCELLED,
                "cancelled_at": datetime.now(),
                "cancellation_reason": reason,
                "updated_at": datetime.now()
            }}
        )
    
    @staticmethod
    def refund_payment(invoice_id, refund_amount, reason=None):
        """Process a refund for a paid invoice"""
        return db.payments.update_one(
            {"_id": invoice_id},
            {"$set": {
                "status": Payment.STATUS_REFUNDED,
                "refund_amount": refund_amount,
                "refund_reason": reason,
                "refunded_at": datetime.now(),
                "updated_at": datetime.now()
            }}
        )
    
    @staticmethod
    def get_monthly_recurring_revenue():
        """Calculate Monthly Recurring Revenue (MRR)"""
        pipeline = [
            {
                "$lookup": {
                    "from": "subscriptions",
                    "localField": "company_id",
                    "foreignField": "company_id",
                    "as": "subscription"
                }
            },
            {"$unwind": "$subscription"},
            {
                "$match": {
                    "subscription.status": {"$in": ["active", "trial"]}
                }
            },
            {
                "$group": {
                    "_id": None,
                    "mrr": {
                        "$sum": {
                            "$multiply": [
                                "$subscription.current_agent_count",
                                "$subscription.price_per_agent"
                            ]
                        }
                    }
                }
            }
        ]
        
        result = list(db.payments.aggregate(pipeline))
        return result[0]["mrr"] if result else 0


class PaymentMethod:
    """Payment Method Model - Stores company payment preferences"""
    
    @staticmethod
    def create(company_id, method_type, details):
        """Add a payment method for a company"""
        payment_method = {
            "company_id": company_id,
            "method_type": method_type,
            "details": details,  # Could include account number, GCash number, etc.
            "is_default": False,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        result = db.payment_methods.insert_one(payment_method)
        return {**payment_method, "_id": result.inserted_id}
    
    @staticmethod
    def get_by_company(company_id):
        """Get all payment methods for a company"""
        return list(db.payment_methods.find({"company_id": company_id}))
    
    @staticmethod
    def set_default(company_id, method_id):
        """Set a payment method as default"""
        # First, unset all as default
        db.payment_methods.update_many(
            {"company_id": company_id},
            {"$set": {"is_default": False}}
        )
        
        # Then set the selected one as default
        return db.payment_methods.update_one(
            {"_id": method_id, "company_id": company_id},
            {"$set": {"is_default": True, "updated_at": datetime.now()}}
        )
    
    @staticmethod
    def delete(method_id, company_id):
        """Delete a payment method"""
        return db.payment_methods.delete_one({
            "_id": method_id,
            "company_id": company_id
        })
