"""
Create dummy test accounts for each role type
Run this script to generate test accounts for development/testing
"""
import os
import sys
import django
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salesAI.settings')
django.setup()

from core.models import User, Company, Agent, AreaManager, DivisionHead, Subscription

def create_test_accounts():
    """Create test accounts for all 4 roles"""
    
    print("🧪 Creating Test Accounts for SalesAI System")
    print("=" * 60)
    
    # Create a test company
    company_id = "COMP-TEST001"
    
    # Check if company already exists
    if Company.exists(company_id):
        print(f"✓ Test company already exists: {company_id}")
        company = Company.get(company_id)
    else:
        print("\n📦 Creating Test Company...")
        company = Company.create(
            company_id=company_id,
            name="Test Company Inc.",
            email="test@company.com",
            phone="+63 917 123 4567",
            address="123 Test Street, Manila, Philippines",
            tin="123-456-789-000",
            business_type="Financial Services",
            contact_person="Test Admin"
        )
        print(f"✓ Created company: {company['name']} ({company_id})")
        
        # Create subscription
        subscription_id = f"SUB-{company_id}"
        subscription = Subscription.create(
            subscription_id=subscription_id,
            company_id=company_id,
            billing_email="test@company.com",
            trial_enabled=True
        )
        print(f"✓ Created subscription with 14-day trial")
    
    # Create test organizational structure
    print("\n👥 Creating Organizational Structure...")
    
    # 1. Division Head
    division_head_id = "DIV-TEST001"
    if not DivisionHead.get(division_head_id):
        division_head = DivisionHead.create(
            head_id=division_head_id,
            name="John Division",
            email="division@test.com",
            division_name="NCR Division",
            company_id=company_id
        )
        print(f"✓ Created Division Head: {division_head['name']}")
    else:
        division_head = DivisionHead.get(division_head_id)
        print(f"✓ Division Head already exists: {division_head['name']}")
    
    # 2. Area Manager
    area_manager_id = "AM-TEST001"
    if not AreaManager.get(area_manager_id):
        area_manager = AreaManager.create(
            manager_id=area_manager_id,
            name="Maria Manager",
            email="manager@test.com",
            area_name="Manila Area",
            division_head_id=division_head_id,
            company_id=company_id
        )
        print(f"✓ Created Area Manager: {area_manager['name']}")
    else:
        area_manager = AreaManager.get(area_manager_id)
        print(f"✓ Area Manager already exists: {area_manager['name']}")
    
    # 3. Sales Agent
    agent_id = "AGENT-TEST001"
    if not Agent.get(agent_id):
        agent = Agent.create(
            agent_id=agent_id,
            name="Pedro Agent",
            email="agent@test.com",
            monthly_target=100000,
            company_id=company_id,
            area_manager_id=area_manager_id
        )
        print(f"✓ Created Sales Agent: {agent['name']}")
    else:
        agent = Agent.get(agent_id)
        print(f"✓ Sales Agent already exists: {agent['name']}")
    
    # Create user accounts for each role
    print("\n🔐 Creating User Accounts...")
    
    test_accounts = [
        {
            'user_id': 'USER-ADMIN-TEST',
            'email': 'admin@test.com',
            'password': 'admin123',
            'role': User.ROLE_COMPANY_ADMIN,
            'name': 'Admin User',
            'phone': '+63 917 111 1111',
            'related_id': None
        },
        {
            'user_id': 'USER-DIV-TEST',
            'email': 'division@test.com',
            'password': 'division123',
            'role': User.ROLE_DIVISION_HEAD,
            'name': 'John Division',
            'phone': '+63 917 222 2222',
            'related_id': division_head_id
        },
        {
            'user_id': 'USER-MGR-TEST',
            'email': 'manager@test.com',
            'password': 'manager123',
            'role': User.ROLE_AREA_MANAGER,
            'name': 'Maria Manager',
            'phone': '+63 917 333 3333',
            'related_id': area_manager_id
        },
        {
            'user_id': 'USER-AGENT-TEST',
            'email': 'agent@test.com',
            'password': 'agent123',
            'role': User.ROLE_AGENT,
            'name': 'Pedro Agent',
            'phone': '+63 917 444 4444',
            'related_id': agent_id
        }
    ]
    
    created_accounts = []
    
    for account in test_accounts:
        if User.email_exists(account['email']):
            print(f"⚠ User already exists: {account['email']}")
            user = User.get_by_email(account['email'])
        else:
            user = User.create(
                user_id=account['user_id'],
                email=account['email'],
                password=account['password'],
                role=account['role'],
                company_id=company_id,
                name=account['name'],
                phone=account['phone'],
                related_id=account['related_id']
            )
            print(f"✓ Created {account['role']}: {account['email']}")
        
        created_accounts.append({
            'role': account['role'],
            'email': account['email'],
            'password': account['password'],
            'name': account['name']
        })
    
    # Print summary
    print("\n" + "=" * 60)
    print("✅ TEST ACCOUNTS CREATED SUCCESSFULLY!")
    print("=" * 60)
    print("\n📋 TEST CREDENTIALS:\n")
    
    role_icons = {
        User.ROLE_COMPANY_ADMIN: "👨‍💼",
        User.ROLE_DIVISION_HEAD: "👔",
        User.ROLE_AREA_MANAGER: "👨‍💻",
        User.ROLE_AGENT: "👤"
    }
    
    role_names = {
        User.ROLE_COMPANY_ADMIN: "Company Admin",
        User.ROLE_DIVISION_HEAD: "Division Head",
        User.ROLE_AREA_MANAGER: "Area Manager",
        User.ROLE_AGENT: "Sales Agent"
    }
    
    for account in created_accounts:
        icon = role_icons.get(account['role'], '👤')
        role_name = role_names.get(account['role'], account['role'])
        print(f"{icon} {role_name.upper()}")
        print(f"   Name:     {account['name']}")
        print(f"   Email:    {account['email']}")
        print(f"   Password: {account['password']}")
        print()
    
    print("🌐 Test at: https://salesai-system.onrender.com/login/")
    print("📝 Company: Test Company Inc.")
    print("💰 Subscription: 14-day trial (₱500/agent/month)")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    try:
        create_test_accounts()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
