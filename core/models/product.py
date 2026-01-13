"""
Product model - Banking products catalog
"""
from datetime import datetime
from core.database import db


class Product:
    """Product Model - Banking products and services"""
    
    @staticmethod
    def create(product_id, name, category, description, commission_rate):
        """Create a new product"""
        product = {
            "_id": product_id,
            "name": name,
            "category": category,
            "description": description,
            "commission_rate": commission_rate,  # Percentage
            "created_at": datetime.now()
        }
        db.products.insert_one(product)
        return product
    
    @staticmethod
    def get(product_id):
        """Get product by ID"""
        return db.products.find_one({"_id": product_id})
    
    @staticmethod
    def get_all():
        """Get all products"""
        return list(db.products.find())
    
    @staticmethod
    def get_by_category(category):
        """Get products by category"""
        return list(db.products.find({"category": category}))
    
    @staticmethod
    def exists(product_id):
        """Check if product exists"""
        return db.products.count_documents({"_id": product_id}) > 0
