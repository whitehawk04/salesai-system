"""
Views for database setup via web interface
"""
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from core.utils.sample_data import create_sample_data, clear_all_data
from core.utils.banking_products_data import create_banking_products, create_sample_leads_and_sales
from core.database import db
from core.ai.trainer import AITrainer
from core.models import User, Company, Agent, AreaManager, DivisionHead, Subscription
import os


@csrf_exempt
@require_http_methods(["POST", "GET"])
def setup_database(request):
    """
    Endpoint to populate database with demo data
    Security: Only works if SETUP_KEY environment variable matches
    
    Usage:
    GET/POST to: /setup-database/?key=YOUR_SETUP_KEY
    Or: /setup-database/?key=YOUR_SETUP_KEY&clear=true
    """
    
    # Security check - require setup key from environment
    expected_key = os.getenv('SETUP_KEY', 'demo-setup-key-2026')
    provided_key = request.GET.get('key') or request.POST.get('key')
    
    if provided_key != expected_key:
        return JsonResponse({
            'success': False,
            'error': 'Invalid or missing setup key',
            'message': 'Set SETUP_KEY environment variable and provide it as ?key=YOUR_KEY'
        }, status=403)
    
    # Check if should clear data
    should_clear = request.GET.get('clear', '').lower() == 'true'
    
    results = {
        'success': True,
        'steps': []
    }
    
    try:
        # Step 0: Clear data if requested
        if should_clear:
            results['steps'].append({
                'step': 0,
                'name': 'Clear existing data',
                'status': 'started'
            })
            clear_all_data()
            db.products.delete_many({})
            db.leads.delete_many({})
            results['steps'][-1]['status'] = 'completed'
            results['steps'][-1]['message'] = 'All existing data cleared'
        
        # Step 1: Create organizational hierarchy
        results['steps'].append({
            'step': 1,
            'name': 'Create organizational hierarchy and agents',
            'status': 'started'
        })
        try:
            create_sample_data()
            results['steps'][-1]['status'] = 'completed'
            results['steps'][-1]['counts'] = {
                'division_heads': db.division_heads.count_documents({}),
                'area_managers': db.area_managers.count_documents({}),
                'agents': db.agents.count_documents({}),
                'activities': db.activities.count_documents({}),
                'sales': db.sales.count_documents({})
            }
        except Exception as e:
            results['steps'][-1]['status'] = 'error'
            results['steps'][-1]['error'] = str(e)
            if 'duplicate' in str(e).lower() and not should_clear:
                results['steps'][-1]['message'] = 'Data already exists. Add ?clear=true to reset.'
        
        # Step 2: Create banking products
        results['steps'].append({
            'step': 2,
            'name': 'Create banking products',
            'status': 'started'
        })
        try:
            create_banking_products()
            results['steps'][-1]['status'] = 'completed'
            results['steps'][-1]['counts'] = {
                'products': db.products.count_documents({})
            }
        except Exception as e:
            results['steps'][-1]['status'] = 'error'
            results['steps'][-1]['error'] = str(e)
            if 'duplicate' in str(e).lower() and not should_clear:
                results['steps'][-1]['message'] = 'Products already exist. Add ?clear=true to reset.'
        
        # Step 3: Create leads and sales
        results['steps'].append({
            'step': 3,
            'name': 'Create leads and sales data',
            'status': 'started'
        })
        try:
            create_sample_leads_and_sales()
            results['steps'][-1]['status'] = 'completed'
            results['steps'][-1]['counts'] = {
                'leads': db.leads.count_documents({}),
                'sales': db.sales.count_documents({})
            }
        except Exception as e:
            results['steps'][-1]['status'] = 'error'
            results['steps'][-1]['error'] = str(e)
        
        # Step 4: Train AI model
        results['steps'].append({
            'step': 4,
            'name': 'Train AI model',
            'status': 'started'
        })
        try:
            model, accuracy = AITrainer.train_model()
            results['steps'][-1]['status'] = 'completed'
            results['steps'][-1]['accuracy'] = f"{accuracy * 100:.2f}%"
        except Exception as e:
            results['steps'][-1]['status'] = 'warning'
            results['steps'][-1]['error'] = str(e)
            results['steps'][-1]['message'] = 'Model training failed but data was created. You can train later at /train/'
        
        # Final summary
        results['summary'] = {
            'division_heads': db.division_heads.count_documents({}),
            'area_managers': db.area_managers.count_documents({}),
            'agents': db.agents.count_documents({}),
            'activities': db.activities.count_documents({}),
            'sales': db.sales.count_documents({}),
            'products': db.products.count_documents({}),
            'leads': db.leads.count_documents({})
        }
        
        results['message'] = 'Database setup completed successfully!'
        results['next_steps'] = [
            'Visit your dashboard to see the data',
            'Train AI model at /train/ if it failed',
            'Explore different views and reports'
        ]
        
    except Exception as e:
        results['success'] = False
        results['error'] = str(e)
        import traceback
        results['traceback'] = traceback.format_exc()
    
    return JsonResponse(results, json_dumps_params={'indent': 2})


@require_http_methods(["GET"])
def check_data(request):
    """
    Endpoint to check current data counts
    No authentication required - read-only
    """
    counts = {
        'division_heads': db.division_heads.count_documents({}),
        'area_managers': db.area_managers.count_documents({}),
        'agents': db.agents.count_documents({}),
        'activities': db.activities.count_documents({}),
        'sales': db.sales.count_documents({}),
        'products': db.products.count_documents({}),
        'leads': db.leads.count_documents({})
    }
    
    total = sum(counts.values())
    
    return JsonResponse({
        'counts': counts,
        'total_documents': total,
        'has_data': total > 0,
        'message': 'Database has data' if total > 0 else 'Database is empty'
    }, json_dumps_params={'indent': 2})


@csrf_exempt
@require_http_methods(["POST", "GET"])
def create_test_accounts_endpoint(request):
    """
    Create test accounts via HTTP endpoint (for Render deployment)
    Usage: /create-test-accounts/
    """
    try:
        # Create a test company
        company_id = "COMP-TEST001"
        
        # Check if company already exists
        if Company.exists(company_id):
            company = Company.get(company_id)
            message = "Test company already exists"
        else:
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
            
            # Create subscription
            subscription_id = f"SUB-{company_id}"
            subscription = Subscription.create(
                subscription_id=subscription_id,
                company_id=company_id,
                billing_email="test@company.com",
                trial_enabled=True
            )
            message = "Created test company"
        
        # Create organizational structure
        division_head_id = "DIV-TEST001"
        if not DivisionHead.get(division_head_id):
            DivisionHead.create(
                head_id=division_head_id,
                name="John Division",
                email="division@test.com",
                division_name="NCR Division",
                company_id=company_id
            )
        
        area_manager_id = "AM-TEST001"
        if not AreaManager.get(area_manager_id):
            AreaManager.create(
                manager_id=area_manager_id,
                name="Maria Manager",
                email="manager@test.com",
                area_name="Manila Area",
                division_head_id=division_head_id,
                company_id=company_id
            )
        
        agent_id = "AGENT-TEST001"
        if not Agent.get(agent_id):
            Agent.create(
                agent_id=agent_id,
                name="Pedro Agent",
                email="agent@test.com",
                monthly_target=100000,
                company_id=company_id,
                area_manager_id=area_manager_id
            )
        
        # Create user accounts
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
                created_accounts.append({
                    'email': account['email'],
                    'role': account['role'],
                    'status': 'already_exists'
                })
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
                created_accounts.append({
                    'email': account['email'],
                    'role': account['role'],
                    'status': 'created'
                })
        
        return JsonResponse({
            'success': True,
            'message': 'Test accounts setup completed',
            'company': {
                'id': company_id,
                'name': company['name']
            },
            'accounts': created_accounts,
            'test_credentials': {
                'company_admin': {'email': 'admin@test.com', 'password': 'admin123'},
                'division_head': {'email': 'division@test.com', 'password': 'division123'},
                'area_manager': {'email': 'manager@test.com', 'password': 'manager123'},
                'agent': {'email': 'agent@test.com', 'password': 'agent123'}
            },
            'login_url': '/login/'
        }, json_dumps_params={'indent': 2})
        
    except Exception as e:
        import traceback
        return JsonResponse({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc(),
            'message': 'Failed to create test accounts'
        }, status=500)
