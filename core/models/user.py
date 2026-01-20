"""
User model - Authentication and role-based access control
"""
from datetime import datetime
import hashlib
import secrets
from core.database import db


class User:
    """User Model - Authentication and authorization"""
    
    # User roles
    ROLE_SUPER_ADMIN = "super_admin"  # Platform admin (manages all companies)
    ROLE_COMPANY_ADMIN = "company_admin"  # Company owner/admin
    ROLE_DIVISION_HEAD = "division_head"
    ROLE_AREA_MANAGER = "area_manager"
    ROLE_AGENT = "agent"
    
    # Role hierarchy for permissions
    ROLE_HIERARCHY = {
        ROLE_SUPER_ADMIN: 100,
        ROLE_COMPANY_ADMIN: 80,
        ROLE_DIVISION_HEAD: 60,
        ROLE_AREA_MANAGER: 40,
        ROLE_AGENT: 20
    }
    
    @staticmethod
    def hash_password(password):
        """Hash a password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def generate_token():
        """Generate a secure random token for API access"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def create(user_id, email, password, role, company_id=None, 
               name=None, phone=None, related_id=None):
        """
        Create a new user
        related_id: Links to agent_id, area_manager_id, or division_head_id
        """
        user = {
            "_id": user_id,
            "email": email.lower(),
            "password": User.hash_password(password),
            "role": role,
            "company_id": company_id,  # None for super_admin
            "name": name,
            "phone": phone,
            "related_id": related_id,  # Link to agent, manager, or division head
            "is_active": True,
            "api_token": User.generate_token(),
            "last_login": None,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        db.users.insert_one(user)
        return user
    
    @staticmethod
    def authenticate(email, password):
        """Authenticate a user by email and password"""
        user = db.users.find_one({
            "email": email.lower(),
            "is_active": True
        })
        
        if not user:
            return None
        
        if user.get("password") == User.hash_password(password):
            # Update last login
            db.users.update_one(
                {"_id": user["_id"]},
                {"$set": {"last_login": datetime.now()}}
            )
            return user
        
        return None
    
    @staticmethod
    def authenticate_by_token(token):
        """Authenticate a user by API token"""
        user = db.users.find_one({
            "api_token": token,
            "is_active": True
        })
        
        if user:
            db.users.update_one(
                {"_id": user["_id"]},
                {"$set": {"last_login": datetime.now()}}
            )
        
        return user
    
    @staticmethod
    def get(user_id):
        """Get user by ID"""
        return db.users.find_one({"_id": user_id})
    
    @staticmethod
    def get_by_email(email):
        """Get user by email"""
        return db.users.find_one({"email": email.lower()})
    
    @staticmethod
    def get_by_company(company_id, role=None):
        """Get all users for a company, optionally filtered by role"""
        query = {"company_id": company_id}
        if role:
            query["role"] = role
        return list(db.users.find(query))
    
    @staticmethod
    def update(user_id, **kwargs):
        """Update user information"""
        # Hash password if being updated
        if "password" in kwargs:
            kwargs["password"] = User.hash_password(kwargs["password"])
        
        kwargs["updated_at"] = datetime.now()
        return db.users.update_one(
            {"_id": user_id},
            {"$set": kwargs}
        )
    
    @staticmethod
    def change_password(user_id, old_password, new_password):
        """Change user password"""
        user = User.get(user_id)
        if not user:
            return False
        
        if user.get("password") != User.hash_password(old_password):
            return False
        
        return db.users.update_one(
            {"_id": user_id},
            {"$set": {
                "password": User.hash_password(new_password),
                "updated_at": datetime.now()
            }}
        )
    
    @staticmethod
    def reset_password(user_id, new_password):
        """Reset user password (admin function)"""
        return db.users.update_one(
            {"_id": user_id},
            {"$set": {
                "password": User.hash_password(new_password),
                "updated_at": datetime.now()
            }}
        )
    
    @staticmethod
    def deactivate(user_id):
        """Deactivate a user account"""
        return db.users.update_one(
            {"_id": user_id},
            {"$set": {
                "is_active": False,
                "deactivated_at": datetime.now(),
                "updated_at": datetime.now()
            }}
        )
    
    @staticmethod
    def activate(user_id):
        """Activate a user account"""
        return db.users.update_one(
            {"_id": user_id},
            {"$set": {
                "is_active": True,
                "updated_at": datetime.now()
            },
            "$unset": {"deactivated_at": ""}}
        )
    
    @staticmethod
    def refresh_token(user_id):
        """Generate a new API token for a user"""
        new_token = User.generate_token()
        db.users.update_one(
            {"_id": user_id},
            {"$set": {
                "api_token": new_token,
                "updated_at": datetime.now()
            }}
        )
        return new_token
    
    @staticmethod
    def has_permission(user, required_role):
        """Check if user has permission based on role hierarchy"""
        user_role = user.get("role")
        user_level = User.ROLE_HIERARCHY.get(user_role, 0)
        required_level = User.ROLE_HIERARCHY.get(required_role, 0)
        
        return user_level >= required_level
    
    @staticmethod
    def can_access_company(user, company_id):
        """Check if user can access a specific company's data"""
        # Super admin can access all companies
        if user.get("role") == User.ROLE_SUPER_ADMIN:
            return True
        
        # Other users can only access their own company
        return user.get("company_id") == company_id
    
    @staticmethod
    def delete(user_id):
        """Delete a user"""
        return db.users.delete_one({"_id": user_id})
    
    @staticmethod
    def exists(user_id):
        """Check if user exists"""
        return db.users.count_documents({"_id": user_id}) > 0
    
    @staticmethod
    def email_exists(email):
        """Check if email is already registered"""
        return db.users.count_documents({"email": email.lower()}) > 0
