"""
Generate sample Philippine banking products and sales/leads data
"""
import random
from datetime import datetime, timedelta
from core.models import Product, Lead, Sale, Agent


def create_banking_products():
    """Create Philippine banking products catalog"""
    
    print("Creating Philippine banking products...")
    
    products = [
        # Loans
        {"product_id": "LOAN-001", "name": "Personal Loan", "category": "Loan", "description": "Unsecured personal financing up to ₱2M", "commission_rate": 2.5},
        {"product_id": "LOAN-002", "name": "Auto Loan", "category": "Loan", "description": "Car financing with low interest rates", "commission_rate": 3.0},
        {"product_id": "LOAN-003", "name": "Home Loan", "category": "Loan", "description": "Housing loan up to ₱15M, 30 years to pay", "commission_rate": 1.5},
        {"product_id": "LOAN-004", "name": "Business Loan", "category": "Loan", "description": "SME financing for business growth", "commission_rate": 2.0},
        {"product_id": "LOAN-005", "name": "Salary Loan", "category": "Loan", "description": "Quick cash loan for employees", "commission_rate": 3.5},
        
        # Credit Cards
        {"product_id": "CC-001", "name": "Classic Credit Card", "category": "Credit Card", "description": "Entry-level credit card with rewards", "commission_rate": 5.0},
        {"product_id": "CC-002", "name": "Gold Credit Card", "category": "Credit Card", "description": "Premium card with travel benefits", "commission_rate": 6.0},
        {"product_id": "CC-003", "name": "Platinum Credit Card", "category": "Credit Card", "description": "Elite card with exclusive perks", "commission_rate": 7.0},
        {"product_id": "CC-004", "name": "Cashback Credit Card", "category": "Credit Card", "description": "Get 5% cashback on all purchases", "commission_rate": 5.5},
        
        # Insurance
        {"product_id": "INS-001", "name": "Life Insurance", "category": "Insurance", "description": "Whole life insurance coverage", "commission_rate": 15.0},
        {"product_id": "INS-002", "name": "Health Insurance", "category": "Insurance", "description": "Comprehensive health coverage", "commission_rate": 12.0},
        {"product_id": "INS-003", "name": "Car Insurance", "category": "Insurance", "description": "Comprehensive auto insurance", "commission_rate": 10.0},
        {"product_id": "INS-004", "name": "Travel Insurance", "category": "Insurance", "description": "Coverage for international travel", "commission_rate": 8.0},
        
        # Investments
        {"product_id": "INV-001", "name": "Time Deposit", "category": "Investment", "description": "High-yield time deposit accounts", "commission_rate": 1.0},
        {"product_id": "INV-002", "name": "Mutual Funds", "category": "Investment", "description": "Diversified investment portfolio", "commission_rate": 2.5},
        {"product_id": "INV-003", "name": "VUL Insurance", "category": "Investment", "description": "Variable Universal Life with investment", "commission_rate": 18.0},
        {"product_id": "INV-004", "name": "Treasury Bills", "category": "Investment", "description": "Government securities investment", "commission_rate": 0.5},
        
        # Accounts
        {"product_id": "ACC-001", "name": "Savings Account", "category": "Account", "description": "High-interest savings account", "commission_rate": 1.0},
        {"product_id": "ACC-002", "name": "Payroll Account", "category": "Account", "description": "Corporate payroll services", "commission_rate": 2.0},
        {"product_id": "ACC-003", "name": "Business Account", "category": "Account", "description": "Business current account", "commission_rate": 2.5},
    ]
    
    for product_data in products:
        if not Product.exists(product_data["product_id"]):
            Product.create(
                product_id=product_data["product_id"],
                name=product_data["name"],
                category=product_data["category"],
                description=product_data["description"],
                commission_rate=product_data["commission_rate"]
            )
            print(f"  ✓ Created: {product_data['name']}")
        else:
            print(f"  • Already exists: {product_data['name']}")
    
    print(f"\n✅ Total banking products: {len(products)}")
    return products


def create_sample_leads_and_sales():
    """Generate sample leads and update sales with products for each agent"""
    
    print("\n\nGenerating sample leads and sales with products...")
    
    # Get all products
    products = Product.get_all()
    if not products:
        print("No products found. Creating products first...")
        products = create_banking_products()
    
    # Get all agents
    agents = Agent.get_all()
    if not agents:
        print("No agents found. Please create agents first.")
        return
    
    # Common Filipino names for customers
    first_names = ["Juan", "Maria", "Jose", "Ana", "Pedro", "Rosa", "Carlos", "Elena", "Miguel", "Sofia", 
                   "Roberto", "Carmen", "Luis", "Isabel", "Antonio", "Teresa", "Manuel", "Patricia", "Ramon", "Angelica"]
    last_names = ["Santos", "Reyes", "Cruz", "Bautista", "Garcia", "Mendoza", "Torres", "Flores", 
                  "Ramos", "Rivera", "Gonzales", "Fernandez", "Lopez", "Valdez", "Santiago", "Morales"]
    
    # Lead statuses
    lead_statuses = ["New", "Contacted", "Qualified", "Proposal", "Negotiation", "Won", "Lost"]
    
    lead_counter = 1
    sale_counter = 1
    
    for agent in agents:
        agent_id = agent['_id']
        print(f"\n  Agent: {agent['name']} ({agent_id})")
        
        # Generate 8-15 leads per agent
        num_leads = random.randint(8, 15)
        agent_leads = []
        
        for i in range(num_leads):
            product = random.choice(products)
            customer_name = f"{random.choice(first_names)} {random.choice(last_names)}"
            status = random.choice(lead_statuses)
            
            # Calculate potential value based on product category
            if product['category'] == 'Loan':
                value = random.randint(100000, 2000000)
            elif product['category'] == 'Credit Card':
                value = random.randint(20000, 100000)
            elif product['category'] == 'Insurance':
                value = random.randint(50000, 500000)
            elif product['category'] == 'Investment':
                value = random.randint(100000, 5000000)
            else:  # Account
                value = random.randint(10000, 50000)
            
            contact = f"+639{random.randint(100000000, 999999999)}"
            
            lead = Lead.create(
                lead_id=f"LEAD{lead_counter:05d}",
                agent_id=agent_id,
                customer_name=customer_name,
                contact=contact,
                product_id=product['_id'],
                status=status,
                value=value,
                notes=f"Interested in {product['name']}"
            )
            
            agent_leads.append(lead)
            lead_counter += 1
            
            # Convert some "Won" leads to sales
            if status == "Won":
                sale_amount = int(value * (product['commission_rate'] / 100))
                Sale.create(
                    sale_id=f"SALE{sale_counter:05d}",
                    agent_id=agent_id,
                    amount=sale_amount,
                    customer=customer_name,
                    product_id=product['_id'],
                    notes=f"Commission from {product['name']}"
                )
                sale_counter += 1
        
        print(f"    ✓ Created {num_leads} leads")
        won_leads = len([l for l in agent_leads if l['status'] == 'Won'])
        print(f"    ✓ {won_leads} converted to sales")
    
    print(f"\n✅ Total leads created: {lead_counter - 1}")
    print(f"✅ Total sales created: {sale_counter - 1}")


def clear_products_and_leads():
    """Clear products and leads data"""
    from core.database import db
    
    print("⚠️  Clearing products and leads...")
    db.products.delete_many({})
    db.leads.delete_many({})
    print("✅ Data cleared!")


if __name__ == "__main__":
    create_banking_products()
    create_sample_leads_and_sales()
