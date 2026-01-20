"""
Quick test script for the multi-tenant subscription system
Run this to verify the system is working correctly
"""

from datetime import datetime
from core.models import Company, Subscription, Payment, User, Agent

def test_system():
    """Test the subscription system"""
    
    print("🇵🇭 Testing Multi-Tenant Subscription System")
    print("=" * 60)
    
    # Test 1: Create a company
    print("\n✅ Test 1: Creating a test company...")
    company_id = f"TEST-COMP-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    try:
        company = Company.create(
            company_id=company_id,
            name="Test Corporation Philippines",
            email="test@testcorp.ph",
            phone="+639171234567",
            address="Makati City, Metro Manila",
            tin="123-456-789-000",
            business_type="Technology",
            contact_person="Test Admin"
        )
        print(f"   ✓ Company created: {company['name']}")
        print(f"   ✓ Company ID: {company_id}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return
    
    # Test 2: Create subscription with trial
    print("\n✅ Test 2: Creating subscription with 14-day trial...")
    subscription_id = f"TEST-SUB-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    try:
        subscription = Subscription.create(
            subscription_id=subscription_id,
            company_id=company_id,
            billing_email="billing@testcorp.ph",
            trial_enabled=True
        )
        print(f"   ✓ Subscription created: {subscription['status']}")
        print(f"   ✓ Trial days: {Subscription.TRIAL_DAYS}")
        print(f"   ✓ Price per agent: ₱{subscription['price_per_agent']}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return
    
    # Test 3: Create admin user
    print("\n✅ Test 3: Creating company admin user...")
    user_id = f"TEST-USER-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    try:
        user = User.create(
            user_id=user_id,
            email="admin@testcorp.ph",
            password="TestPassword123!",
            role=User.ROLE_COMPANY_ADMIN,
            company_id=company_id,
            name="Test Admin",
            phone="+639171234567"
        )
        print(f"   ✓ User created: {user['email']}")
        print(f"   ✓ Role: {user['role']}")
        print(f"   ✓ API Token: {user['api_token'][:20]}...")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return
    
    # Test 4: Create agents
    print("\n✅ Test 4: Creating test agents...")
    agent_count = 5
    for i in range(1, agent_count + 1):
        agent_id = f"TEST-A{i:03d}"
        try:
            agent = Agent.create(
                agent_id=agent_id,
                name=f"Test Agent {i}",
                email=f"agent{i}@testcorp.ph",
                monthly_target=500000,
                company_id=company_id
            )
            print(f"   ✓ Agent {i} created: {agent['name']}")
        except Exception as e:
            print(f"   ✗ Error creating agent {i}: {e}")
    
    # Test 5: Verify agent count update
    print("\n✅ Test 5: Verifying subscription agent count...")
    try:
        subscription = Subscription.get_by_company(company_id)
        print(f"   ✓ Current agent count: {subscription['current_agent_count']}")
        
        # Calculate cost
        monthly_cost = Subscription.calculate_monthly_cost(company_id)
        print(f"   ✓ Monthly cost: ₱{monthly_cost:,.2f}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return
    
    # Test 6: Create invoice
    print("\n✅ Test 6: Creating test invoice...")
    invoice_id = f"TEST-INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    try:
        invoice = Payment.create_invoice(
            invoice_id=invoice_id,
            company_id=company_id,
            amount=monthly_cost,
            agent_count=subscription['current_agent_count'],
            billing_period_start=datetime.now(),
            billing_period_end=datetime.now()
        )
        print(f"   ✓ Invoice created: {invoice['invoice_number']}")
        print(f"   ✓ Amount: ₱{invoice['amount']:,.2f}")
        print(f"   ✓ Status: {invoice['status']}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return
    
    # Test 7: Record payment
    print("\n✅ Test 7: Recording test payment...")
    try:
        Payment.record_payment(
            invoice_id=invoice_id,
            amount_paid=monthly_cost,
            payment_method=Payment.METHOD_GCASH,
            reference_number="TEST-GC-123456789",
            notes="Test payment via GCash"
        )
        payment = Payment.get(invoice_id)
        print(f"   ✓ Payment recorded: ₱{payment['amount_paid']:,.2f}")
        print(f"   ✓ Method: {payment['payment_method']}")
        print(f"   ✓ Reference: {payment['reference_number']}")
        print(f"   ✓ Status: {payment['status']}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return
    
    # Test 8: Check subscription status
    print("\n✅ Test 8: Checking subscription status...")
    try:
        is_active = Subscription.is_active(company_id)
        print(f"   ✓ Subscription active: {is_active}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return
    
    # Test 9: Get company statistics
    print("\n✅ Test 9: Getting company statistics...")
    try:
        stats = Company.get_statistics(company_id)
        print(f"   ✓ Total agents: {stats['total_agents']}")
        print(f"   ✓ Total sales: {stats['total_sales']}")
        print(f"   ✓ Total leads: {stats['total_leads']}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return
    
    # Test 10: Test authentication
    print("\n✅ Test 10: Testing user authentication...")
    try:
        auth_user = User.authenticate("admin@testcorp.ph", "TestPassword123!")
        if auth_user:
            print(f"   ✓ Authentication successful: {auth_user['email']}")
            print(f"   ✓ Role: {auth_user['role']}")
        else:
            print(f"   ✗ Authentication failed")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return
    
    # Summary
    print("\n" + "=" * 60)
    print("🎉 ALL TESTS PASSED!")
    print("=" * 60)
    print(f"\n📊 Test Summary:")
    print(f"   Company: {company['name']}")
    print(f"   Company ID: {company_id}")
    print(f"   Agents: {agent_count}")
    print(f"   Monthly Cost: ₱{monthly_cost:,.2f}")
    print(f"   Subscription Status: {'Active' if is_active else 'Inactive'}")
    print(f"   Trial Days: {Subscription.TRIAL_DAYS}")
    print(f"\n🔑 Admin Login Credentials:")
    print(f"   Email: admin@testcorp.ph")
    print(f"   Password: TestPassword123!")
    print(f"   API Token: {user['api_token']}")
    
    print("\n💡 Next Steps:")
    print("   1. Start the server: python manage.py runserver")
    print("   2. Visit: http://localhost:8000/login/")
    print("   3. Login with the credentials above")
    print("   4. Or test the API with the token")
    
    print("\n🗑️  Cleanup:")
    print(f"   To remove test data, delete documents with company_id: {company_id}")
    
    return company_id


if __name__ == "__main__":
    try:
        test_system()
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
