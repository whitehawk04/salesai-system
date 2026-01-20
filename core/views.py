"""
Views for the core application
"""
from django.shortcuts import render
from django.http import JsonResponse
from core.models import Agent, AreaManager, DivisionHead, Sale, Lead, Product
from core.services.performance import PerformanceService
from core.services.predictor import PredictorService
from core.services.hierarchy_performance import HierarchyPerformanceService
from core.services.sales_funnel import SalesFunnelService
from core.ai.trainer import AITrainer


def landing_page(request):
    """
    Public landing page for the SalesAI system
    """
    return render(request, 'landing.html')


def agent_dashboard(request):
    """
    Dashboard for Sales Agents - Personal performance view
    """
    user = request.user
    
    # Check role
    if user.get('role') != 'agent':
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    # Get agent data based on related_id
    agent_id = user.get('related_id')
    company_id = user.get('company_id')
    
    if not agent_id:
        return JsonResponse({'error': 'Agent profile not linked'}, status=400)
    
    agent = Agent.get(agent_id)
    if not agent:
        return JsonResponse({'error': 'Agent not found'}, status=404)
    
    # Get performance metrics
    performance = PerformanceService.get_agent_performance(agent_id, company_id)
    predictions = PredictorService.get_agent_predictions(agent_id)
    
    context = {
        'user': user,
        'agent': agent,
        'performance': performance,
        'predictions': predictions
    }
    
    return render(request, 'agent_dashboard.html', context)


def area_manager_dashboard_view(request):
    """
    Dashboard for Area Managers - Team management view
    """
    user = request.user
    
    # Check role
    if user.get('role') != 'area_manager':
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    # Get area manager data
    manager_id = user.get('related_id')
    company_id = user.get('company_id')
    
    if not manager_id:
        return JsonResponse({'error': 'Area Manager profile not linked'}, status=400)
    
    manager = AreaManager.get(manager_id)
    if not manager:
        return JsonResponse({'error': 'Area Manager not found'}, status=404)
    
    # Get agents under this manager
    agents = Agent.get_by_area_manager(manager_id)
    
    # Get performance data
    performance_data = HierarchyPerformanceService.get_area_manager_performance(manager_id, company_id)
    
    context = {
        'user': user,
        'manager': manager,
        'agents': agents,
        'performance': performance_data
    }
    
    return render(request, 'area_manager_dashboard.html', context)


def division_head_dashboard_view(request):
    """
    Dashboard for Division Heads - Division oversight view
    """
    user = request.user
    
    # Check role
    if user.get('role') != 'division_head':
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    # Get division head data
    division_head_id = user.get('related_id')
    company_id = user.get('company_id')
    
    if not division_head_id:
        return JsonResponse({'error': 'Division Head profile not linked'}, status=400)
    
    division_head = DivisionHead.get(division_head_id)
    if not division_head:
        return JsonResponse({'error': 'Division Head not found'}, status=404)
    
    # Get area managers and agents under this division
    area_managers = AreaManager.get_by_division_head(division_head_id)
    
    # Get performance data
    performance_data = HierarchyPerformanceService.get_division_head_performance(division_head_id, company_id)
    
    context = {
        'user': user,
        'division_head': division_head,
        'area_managers': area_managers,
        'performance': performance_data
    }
    
    return render(request, 'division_head_dashboard.html', context)


def dashboard(request):
    """
    Main dashboard showing all agents with performance and predictions
    """
    try:
        # Get all agents
        agents = Agent.get_all()
        
        # Prepare dashboard data
        dashboard_data = []
        
        for agent in agents:
            agent_id = agent['_id']
            
            # Get performance data
            performance = PerformanceService.get_agent_performance(agent_id)
            
            # Get prediction (if model exists)
            try:
                prediction = PredictorService.predict_agent(agent_id)
            except FileNotFoundError:
                prediction = {
                    'prediction': 'N/A',
                    'risk_level': 'UNKNOWN',
                    'confidence': 0
                }
            except Exception as e:
                print(f"Prediction error for {agent_id}: {e}")
                prediction = {
                    'prediction': 'ERROR',
                    'risk_level': 'UNKNOWN',
                    'confidence': 0
                }
            
            # Combine data
            agent_data = {
                'agent': agent,
                'agent_id': agent_id,
                'performance': performance,
                'prediction': prediction
            }
            
            dashboard_data.append(agent_data)
        
        # Sort by risk level (HIGH first)
        risk_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2, 'UNKNOWN': 3}
        dashboard_data.sort(key=lambda x: risk_order.get(x['prediction']['risk_level'], 999))
        
        context = {
            'dashboard_data': dashboard_data,
            'total_agents': len(agents)
        }
        
        return render(request, 'dashboard.html', context)
    
    except Exception as e:
        context = {
            'error': str(e),
            'dashboard_data': [],
            'total_agents': 0
        }
        return render(request, 'dashboard.html', context)


def agent_detail(request, agent_id):
    """
    Detailed view for a specific agent with sales funnel analysis
    """
    try:
        agent = Agent.get(agent_id)
        
        if not agent:
            return render(request, 'agent_detail.html', {'error': 'Agent not found'})
        
        # Get performance data
        performance = PerformanceService.get_agent_performance(agent_id)
        
        # Get prediction with funnel insights
        try:
            prediction = PredictorService.get_prediction_with_funnel_insights(agent_id)
        except:
            prediction = None
        
        # Get sales funnel metrics
        funnel_metrics = SalesFunnelService.get_funnel_metrics(agent_id)
        
        # Get sales with product details
        sales = Sale.get_by_agent(agent_id)
        sales_with_products = []
        for sale in sales:
            sale_data = dict(sale)
            if sale.get('product_id'):
                product = Product.get(sale['product_id'])
                sale_data['product'] = product
            else:
                sale_data['product'] = None
            sales_with_products.append(sale_data)
        
        # Sort by date (newest first)
        sales_with_products.sort(key=lambda x: x['date'], reverse=True)
        
        # Get leads with product details
        leads = Lead.get_by_agent(agent_id)
        leads_with_products = []
        for lead in leads:
            lead_data = dict(lead)
            if lead.get('product_id'):
                product = Product.get(lead['product_id'])
                lead_data['product'] = product
            else:
                lead_data['product'] = None
            leads_with_products.append(lead_data)
        
        # Count leads by status
        lead_status_counts = {
            'total': len(leads),
            'new': len([l for l in leads if l['status'] == 'New']),
            'contacted': len([l for l in leads if l['status'] == 'Contacted']),
            'qualified': len([l for l in leads if l['status'] == 'Qualified']),
            'proposal': len([l for l in leads if l['status'] == 'Proposal']),
            'negotiation': len([l for l in leads if l['status'] == 'Negotiation']),
            'won': len([l for l in leads if l['status'] == 'Won']),
            'lost': len([l for l in leads if l['status'] == 'Lost'])
        }
        
        context = {
            'agent': agent,
            'performance': performance,
            'prediction': prediction,
            'funnel': funnel_metrics,
            'sales': sales_with_products[:10],  # Show last 10 sales
            'leads': leads_with_products,
            'lead_status_counts': lead_status_counts
        }
        
        return render(request, 'agent_detail.html', context)
    
    except Exception as e:
        return render(request, 'agent_detail.html', {'error': str(e)})


def train_model(request):
    """
    Train the AI model
    """
    if request.method == 'POST':
        try:
            model, accuracy = AITrainer.train_model()
            return JsonResponse({
                'success': True,
                'accuracy': accuracy,
                'message': 'Model trained successfully!'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return render(request, 'train_model.html')


def api_agents(request):
    """
    API endpoint to get all agents with their data
    """
    try:
        agents = Agent.get_all()
        performances = []
        
        for agent in agents:
            perf = PerformanceService.get_agent_performance(agent['_id'])
            try:
                pred = PredictorService.predict_agent(agent['_id'])
            except:
                pred = None
            
            performances.append({
                'agent': agent,
                'performance': perf,
                'prediction': pred
            })
        
        return JsonResponse({'agents': performances})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def area_manager_dashboard(request, manager_id):
    """
    Dashboard for Area Manager showing their team's performance
    """
    try:
        # Get area manager performance data
        data = HierarchyPerformanceService.get_area_manager_performance(manager_id)
        
        if not data:
            return render(request, 'area_manager_dashboard.html', {
                'error': 'Area Manager not found'
            })
        
        # Sort agents by risk level (HIGH first)
        risk_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2, 'UNKNOWN': 3}
        data['agents'].sort(key=lambda x: risk_order.get(x['prediction']['risk_level'], 999))
        
        return render(request, 'area_manager_dashboard.html', data)
    
    except Exception as e:
        return render(request, 'area_manager_dashboard.html', {
            'error': str(e)
        })


def division_head_dashboard(request, head_id):
    """
    Dashboard for Division Head showing all areas' performance
    """
    try:
        # Get division head performance data
        data = HierarchyPerformanceService.get_division_head_performance(head_id)
        
        if not data:
            return render(request, 'division_head_dashboard.html', {
                'error': 'Division Head not found'
            })
        
        # Sort areas by achievement percentage (lowest first to highlight issues)
        data['areas'].sort(key=lambda x: x['summary']['achievement_percentage'])
        
        return render(request, 'division_head_dashboard.html', data)
    
    except Exception as e:
        return render(request, 'division_head_dashboard.html', {
            'error': str(e)
        })


def area_managers_list(request):
    """
    List all area managers
    """
    try:
        managers = AreaManager.get_all()
        # Add manager_id to each manager dict for template
        managers_list = []
        for manager in managers:
            manager_data = dict(manager)
            manager_data['manager_id'] = manager['_id']
            managers_list.append(manager_data)
        return render(request, 'area_managers_list.html', {
            'managers': managers_list
        })
    except Exception as e:
        return render(request, 'area_managers_list.html', {
            'error': str(e),
            'managers': []
        })


def division_heads_list(request):
    """
    List all division heads
    """
    try:
        heads = DivisionHead.get_all()
        # Add head_id to each head dict for template
        heads_list = []
        for head in heads:
            head_data = dict(head)
            head_data['head_id'] = head['_id']
            heads_list.append(head_data)
        return render(request, 'division_heads_list.html', {
            'heads': heads_list
        })
    except Exception as e:
        return render(request, 'division_heads_list.html', {
            'error': str(e),
            'heads': []
        })
