"""
Generate sample data for testing and demonstration
"""
import random
from datetime import datetime, timedelta
from core.models import Agent, Activity, Sale, AreaManager, DivisionHead


def create_sample_data():
    """Create comprehensive sample data for the system with hierarchy"""
    
    # Create Division Heads
    print("Creating Division Heads...")
    division_heads_data = [
        {"head_id": "DH01", "name": "Robert Williams", "email": "robert.w@company.com", "division_name": "North Division"},
        {"head_id": "DH02", "name": "Jennifer Martinez", "email": "jennifer.m@company.com", "division_name": "South Division"},
    ]
    
    for head_data in division_heads_data:
        if not DivisionHead.exists(head_data["head_id"]):
            DivisionHead.create(
                head_id=head_data["head_id"],
                name=head_data["name"],
                email=head_data["email"],
                division_name=head_data["division_name"]
            )
            print(f"  Created Division Head: {head_data['name']}")
        else:
            print(f"  Division Head already exists: {head_data['name']}")
    
    # Create Area Managers
    print("\nCreating Area Managers...")
    area_managers_data = [
        {"manager_id": "AM01", "name": "Carlos Thompson", "email": "carlos.t@company.com", "division_head_id": "DH01", "area_name": "North Region A"},
        {"manager_id": "AM02", "name": "Lisa Anderson", "email": "lisa.a@company.com", "division_head_id": "DH01", "area_name": "North Region B"},
        {"manager_id": "AM03", "name": "James Wilson", "email": "james.w@company.com", "division_head_id": "DH02", "area_name": "South Region A"},
    ]
    
    for manager_data in area_managers_data:
        if not AreaManager.exists(manager_data["manager_id"]):
            AreaManager.create(
                manager_id=manager_data["manager_id"],
                name=manager_data["name"],
                email=manager_data["email"],
                division_head_id=manager_data["division_head_id"],
                area_name=manager_data["area_name"]
            )
            print(f"  Created Area Manager: {manager_data['name']}")
        else:
            print(f"  Area Manager already exists: {manager_data['name']}")
    
    # Create Sample agents with hierarchy
    print("\nCreating sample agents...")
    agents_data = [
        {"agent_id": "A101", "name": "Maria Santos", "email": "maria@company.com", "monthly_target": 600000, "area_manager_id": "AM01"},
        {"agent_id": "A102", "name": "John Smith", "email": "john@company.com", "monthly_target": 550000, "area_manager_id": "AM01"},
        {"agent_id": "A103", "name": "Sarah Johnson", "email": "sarah@company.com", "monthly_target": 700000, "area_manager_id": "AM02"},
        {"agent_id": "A104", "name": "Michael Chen", "email": "michael@company.com", "monthly_target": 500000, "area_manager_id": "AM02"},
        {"agent_id": "A105", "name": "Emily Davis", "email": "emily@company.com", "monthly_target": 650000, "area_manager_id": "AM03"},
        {"agent_id": "A106", "name": "David Rodriguez", "email": "david@company.com", "monthly_target": 580000, "area_manager_id": "AM03"},
    ]
    
    for agent_data in agents_data:
        if not Agent.exists(agent_data["agent_id"]):
            Agent.create(**agent_data)
            print(f"  Created agent: {agent_data['name']} → {agent_data['area_manager_id']}")
        else:
            # Update existing agents to have area_manager_id
            Agent.update(agent_data["agent_id"], area_manager_id=agent_data["area_manager_id"])
            print(f"  Updated agent: {agent_data['name']} → {agent_data['area_manager_id']}")
    
    print("\nGenerating activities and sales for current month...")
    
    # Generate realistic activities for current month
    now = datetime.now()
    start_of_month = datetime(now.year, now.month, 1)
    
    # Activity patterns for different performance levels
    performance_patterns = {
        "high": {"calls": (80, 120), "meetings": (35, 50), "leads": (25, 40), "deals": (12, 20)},
        "medium": {"calls": (50, 80), "meetings": (20, 35), "leads": (15, 25), "deals": (8, 12)},
        "low": {"calls": (20, 50), "meetings": (10, 20), "leads": (5, 15), "deals": (2, 8)},
    }
    
    # Assign performance levels to agents
    agent_performance = {
        "A101": "high",
        "A102": "medium",
        "A103": "high",
        "A104": "low",
        "A105": "medium",
        "A106": "low",
    }
    
    activity_counter = 1
    sale_counter = 1
    
    for agent in agents_data:
        agent_id = agent["agent_id"]
        performance = agent_performance.get(agent_id, "medium")
        pattern = performance_patterns[performance]
        
        print(f"\n  Generating data for {agent['name']} ({performance} performer)...")
        
        # Generate calls
        num_calls = random.randint(*pattern["calls"])
        for i in range(num_calls):
            days_ago = random.randint(0, 28)
            activity_date = start_of_month + timedelta(days=days_ago)
            Activity.create(
                activity_id=f"ACT{activity_counter:05d}",
                agent_id=agent_id,
                activity_type="call",
                value=0,
                notes=f"Customer outreach call {i+1}"
            )
            activity_counter += 1
        
        # Generate meetings
        num_meetings = random.randint(*pattern["meetings"])
        for i in range(num_meetings):
            days_ago = random.randint(0, 28)
            activity_date = start_of_month + timedelta(days=days_ago)
            Activity.create(
                activity_id=f"ACT{activity_counter:05d}",
                agent_id=agent_id,
                activity_type="meeting",
                value=0,
                notes=f"Client meeting {i+1}"
            )
            activity_counter += 1
        
        # Generate leads
        num_leads = random.randint(*pattern["leads"])
        for i in range(num_leads):
            days_ago = random.randint(0, 28)
            activity_date = start_of_month + timedelta(days=days_ago)
            Activity.create(
                activity_id=f"ACT{activity_counter:05d}",
                agent_id=agent_id,
                activity_type="lead",
                value=0,
                notes=f"New lead {i+1}"
            )
            activity_counter += 1
        
        # Generate deals
        num_deals = random.randint(*pattern["deals"])
        for i in range(num_deals):
            days_ago = random.randint(0, 28)
            activity_date = start_of_month + timedelta(days=days_ago)
            Activity.create(
                activity_id=f"ACT{activity_counter:05d}",
                agent_id=agent_id,
                activity_type="deal",
                value=0,
                notes=f"Deal closed {i+1}"
            )
            activity_counter += 1
        
        # Generate sales based on performance
        monthly_target = agent["monthly_target"]
        if performance == "high":
            total_sales = random.randint(int(monthly_target * 0.85), int(monthly_target * 1.1))
        elif performance == "medium":
            total_sales = random.randint(int(monthly_target * 0.6), int(monthly_target * 0.85))
        else:
            total_sales = random.randint(int(monthly_target * 0.3), int(monthly_target * 0.6))
        
        # Split total sales into multiple transactions
        num_sales = num_deals
        for i in range(num_sales):
            if i < num_sales - 1:
                sale_amount = random.randint(int(total_sales / num_sales * 0.5), int(total_sales / num_sales * 1.5))
            else:
                # Last sale gets remainder
                existing_sales = Sale.get_total_by_agent(agent_id, start_of_month)
                sale_amount = max(0, total_sales - existing_sales)
            
            if sale_amount > 0:
                days_ago = random.randint(0, 28)
                Sale.create(
                    sale_id=f"S{sale_counter:05d}",
                    agent_id=agent_id,
                    amount=sale_amount,
                    customer=f"Customer #{random.randint(1000, 9999)}",
                    notes=f"Sale transaction {i+1}"
                )
                sale_counter += 1
        
        print(f"    ✓ Created {num_calls} calls, {num_meetings} meetings, {num_leads} leads, {num_deals} deals")
        print(f"    ✓ Total sales: ₱{total_sales:,}")
    
    print("\n✅ Sample data created successfully!")
    print(f"   Total Division Heads: {len(division_heads_data)}")
    print(f"   Total Area Managers: {len(area_managers_data)}")
    print(f"   Total agents: {len(agents_data)}")
    print(f"   Total activities: {activity_counter - 1}")
    print(f"   Total sales: {sale_counter - 1}")
    print("\nYou can now:")
    print("  1. View agents dashboard at: /")
    print("  2. View area managers at: /area-managers/")
    print("  3. View division heads at: /division-heads/")
    print("  4. Train the AI model at: /train/")


def clear_all_data():
    """Clear all data from collections (use with caution!)"""
    from core.database import db
    
    print("⚠️  Clearing all data...")
    db.agents.delete_many({})
    db.activities.delete_many({})
    db.sales.delete_many({})
    db.area_managers.delete_many({})
    db.division_heads.delete_many({})
    print("✅ All data cleared!")


if __name__ == "__main__":
    create_sample_data()
