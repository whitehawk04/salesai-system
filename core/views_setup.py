"""
Views for database setup via web interface
"""
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from core.utils.sample_data import create_sample_data, clear_all_data
from core.utils.banking_products_data import create_banking_products, create_sample_leads_and_sales
from core.database import db
from core.ai.trainer import AITrainer
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
