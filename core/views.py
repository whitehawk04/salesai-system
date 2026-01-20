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
    from core.models import Sale, Lead
    from core.database import db
    
    performance = PerformanceService.get_agent_performance(agent_id, company_id)
    
    # Get AI predictions
    try:
        predictions = PredictorService.predict_agent(agent_id)
    except:
        predictions = {
            'prediction': 'Not enough data for prediction',
            'risk_level': 'UNKNOWN',
            'confidence': 0,
            'recommendations': []
        }
    
    # Get recent sales
    recent_sales = list(db.sales.find({"agent_id": agent_id}).sort("date", -1).limit(5))
    
    # Get active leads
    active_leads = list(db.leads.find({
        "agent_id": agent_id,
        "status": {"$in": ["New", "Contacted", "Qualified", "Proposal", "Negotiation"]}
    }).limit(10))
    
    # Calculate additional metrics
    total_sales_count = db.sales.count_documents({"agent_id": agent_id})
    total_leads = db.leads.count_documents({"agent_id": agent_id})
    
    conversion_rate = (total_sales_count / total_leads * 100) if total_leads > 0 else 0
    
    # Calculate average sale amount
    pipeline = [
        {"$match": {"agent_id": agent_id}},
        {"$group": {"_id": None, "avg_amount": {"$avg": "$amount"}}}
    ]
    avg_result = list(db.sales.aggregate(pipeline))
    avg_sale_amount = avg_result[0]['avg_amount'] if avg_result else 0
    
    # Add computed fields to performance
    performance['total_sales_count'] = total_sales_count
    performance['total_leads'] = total_leads
    performance['conversion_rate'] = conversion_rate
    performance['avg_sale_amount'] = avg_sale_amount
    performance['recent_sales'] = recent_sales
    performance['active_leads'] = active_leads
    
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
    
    # Calculate performance metrics
    total_sales = 0
    total_target = 0
    high_risk_count = 0
    medium_risk_count = 0
    on_track_count = 0
    needs_support_count = 0
    
    top_performer = None
    top_achievement = 0
    
    agents_with_data = []
    
    for agent in agents:
        agent_id = agent['_id']
        perf = PerformanceService.get_agent_performance(agent_id, company_id)
        
        total_sales += perf.get('total_sales', 0)
        total_target += agent.get('monthly_target', 0)
        
        achievement = perf.get('achievement_rate', 0)
        
        # Get predictions
        try:
            pred = PredictorService.predict_agent(agent_id)
            risk_level = pred.get('risk_level', 'UNKNOWN')
        except:
            risk_level = 'UNKNOWN'
        
        if risk_level == 'HIGH':
            high_risk_count += 1
        elif risk_level == 'MEDIUM':
            medium_risk_count += 1
        
        if achievement >= 80:
            on_track_count += 1
        else:
            needs_support_count += 1
        
        # Track top performer
        if achievement > top_achievement:
            top_achievement = achievement
            top_performer = {'name': agent['name'], 'achievement': achievement}
        
        # Add data to agent
        agent_data = dict(agent)
        agent_data['current_sales'] = perf.get('total_sales', 0)
        agent_data['achievement'] = achievement
        agent_data['risk_level'] = risk_level
        agents_with_data.append(agent_data)
    
    achievement_rate = (total_sales / total_target * 100) if total_target > 0 else 0
    avg_achievement = achievement_rate
    
    performance_data = {
        'total_sales': total_sales,
        'total_target': total_target,
        'achievement_rate': achievement_rate,
        'high_risk_count': high_risk_count,
        'medium_risk_count': medium_risk_count,
        'on_track_count': on_track_count,
        'needs_support_count': needs_support_count,
        'top_performer': top_performer,
        'avg_achievement': avg_achievement
    }
    
    context = {
        'user': user,
        'manager': manager,
        'agents': agents_with_data,
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
    
    # Get area managers under this division
    area_managers = AreaManager.get_by_division_head(division_head_id)
    
    # Calculate division-wide metrics
    total_sales = 0
    total_target = 0
    total_agents = 0
    
    managers_with_data = []
    
    for manager in area_managers:
        manager_id = manager['_id']
        
        # Get agents under this manager
        agents = Agent.get_by_area_manager(manager_id)
        agent_count = len(agents)
        total_agents += agent_count
        
        # Calculate manager's team performance
        manager_sales = 0
        manager_target = 0
        
        for agent in agents:
            agent_id = agent['_id']
            perf = PerformanceService.get_agent_performance(agent_id, company_id)
            manager_sales += perf.get('total_sales', 0)
            manager_target += agent.get('monthly_target', 0)
        
        total_sales += manager_sales
        total_target += manager_target
        
        manager_achievement = (manager_sales / manager_target * 100) if manager_target > 0 else 0
        
        # Add data to manager
        manager_data = dict(manager)
        manager_data['agent_count'] = agent_count
        manager_data['sales'] = manager_sales
        manager_data['target'] = manager_target
        manager_data['achievement'] = manager_achievement
        managers_with_data.append(manager_data)
    
    achievement_rate = (total_sales / total_target * 100) if total_target > 0 else 0
    
    performance_data = {
        'total_area_managers': len(area_managers),
        'total_agents': total_agents,
        'total_sales': total_sales,
        'total_target': total_target,
        'achievement_rate': achievement_rate,
        'top_agents': []  # Could add top performing agents across division
    }
    
    context = {
        'user': user,
        'division_head': division_head,
        'area_managers': managers_with_data,
        'performance': performance_data
    }
    
    return render(request, 'division_head_dashboard.html', context)


def company_admin_dashboard(request):
    """
    Ultra-simplified Company Admin Dashboard - Minimal functionality, maximum reliability
    """
    try:
        user = request.user if hasattr(request, 'user') else None
        
        if not user:
            return render(request, 'company_admin_dashboard.html', {
                'error': 'User not authenticated',
                'user': None,
                'company': {'name': 'Unknown', 'status': 'unknown'},
                'stats': get_empty_stats(),
                'agents': [],
                'recent_sales': [],
                'subscription': {'status': 'unknown'},
                'monthly_cost': 0
            })
        
        company_id = user.get('company_id') if user else None
        
        if not company_id:
            return render(request, 'company_admin_dashboard.html', {
                'error': 'No company associated with this account',
                'user': user,
                'company': {'name': 'Unknown', 'status': 'unknown'},
                'stats': get_empty_stats(),
                'agents': [],
                'recent_sales': [],
                'subscription': {'status': 'unknown'},
                'monthly_cost': 0
            })
        
        # Import models
        from core.models import Company, Subscription
        from core.database import db
        
        # Get company
        company = Company.get(company_id)
        if not company:
            company = {'name': 'Company Not Found', 'status': 'unknown'}
        
        # Get or create subscription
        subscription = Subscription.get_by_company(company_id)
        if not subscription:
            try:
                subscription = Subscription.create(
                    subscription_id=f"SUB-{company_id}",
                    company_id=company_id,
                    billing_email=company.get('email', 'noemail@company.com'),
                    trial_enabled=True
                )
            except:
                subscription = {'status': 'trial', 'trial_end_date': None}
        
        # Get counts from database (ultra-simple, no aggregations)
        try:
            total_agents = db.agents.count_documents({"company_id": company_id})
        except:
            total_agents = 0
            
        try:
            total_area_managers = db.area_managers.count_documents({"company_id": company_id})
        except:
            total_area_managers = 0
            
        try:
            total_division_heads = db.division_heads.count_documents({"company_id": company_id})
        except:
            total_division_heads = 0
            
        try:
            total_leads = db.leads.count_documents({"company_id": company_id})
        except:
            total_leads = 0
            
        try:
            total_sales_count = db.sales.count_documents({"company_id": company_id})
        except:
            total_sales_count = 0
        
        # Simplified - just use defaults for complex calculations
        total_sales = 0
        total_target = 0
        achievement_rate = 0
        
        # Calculate monthly cost (simple)
        monthly_cost = total_agents * 500  # ₱500 per agent
        
        # Get recent sales (with error handling)
        try:
            recent_sales = list(db.sales.find({"company_id": company_id}).sort("date", -1).limit(5))
        except:
            recent_sales = []
        
        # Get agent list (with error handling)
        try:
            agents_list = list(db.agents.find({"company_id": company_id}).limit(10))
        except:
            agents_list = []
        
        # Build context
        context = {
            'user': user,
            'company': company,
            'subscription': subscription,
            'monthly_cost': monthly_cost,
            'stats': {
                'total_agents': total_agents,
                'total_area_managers': total_area_managers,
                'total_division_heads': total_division_heads,
                'total_sales': total_sales,
                'total_target': total_target,
                'achievement_rate': achievement_rate,
                'total_leads': total_leads,
                'total_sales_count': total_sales_count,
                'high_risk_agents': 0,  # We'll add this later
                'medium_risk_agents': 0,
                'low_risk_agents': 0
            },
            'agents': agents_list,
            'recent_sales': recent_sales
        }
        
        return render(request, 'company_admin_dashboard.html', context)
        
    except Exception as e:
        import traceback
        print(f"Dashboard Error: {str(e)}")
        print(traceback.format_exc())
        
        context = {
            'error': str(e),
            'traceback': traceback.format_exc(),
            'user': request.user if hasattr(request, 'user') else None,
            'company': {'name': 'Error'},
            'stats': get_empty_stats(),
            'agents': [],
            'recent_sales': [],
            'subscription': {'status': 'unknown'},
            'monthly_cost': 0
        }
        return render(request, 'company_admin_dashboard.html', context)


def get_empty_stats():
    """Return empty statistics dictionary"""
    return {
        'total_agents': 0,
        'total_area_managers': 0,
        'total_division_heads': 0,
        'total_sales': 0,
        'total_target': 0,
        'achievement_rate': 0,
        'total_leads': 0,
        'total_sales_count': 0,
        'high_risk_agents': 0,
        'medium_risk_agents': 0,
        'low_risk_agents': 0
    }


def dashboard(request):
    """
    Company Admin Dashboard - Comprehensive overview of entire organization
    """
    try:
        user = request.user
        company_id = user.get('company_id')
        
        if not company_id:
            return render(request, 'company_admin_dashboard.html', {
                'error': 'Company ID not found in user session',
                'user': user
            })
        
        # Import additional models
        from core.models import Company, Subscription, Sale, Lead
        
        # Get company info
        company = Company.get(company_id)
        if not company:
            return render(request, 'company_admin_dashboard.html', {
                'error': 'Company not found',
                'user': user
            })
        
        subscription = Subscription.get_by_company(company_id)
        if not subscription:
            # Create default subscription if it doesn't exist
            from core.models.subscription import Subscription as SubModel
            subscription = SubModel.create(
                subscription_id=f"SUB-{company_id}",
                company_id=company_id,
                billing_email=company.get('email'),
                trial_enabled=True
            )
        
        # Get all organizational data
        agents = Agent.get_all(company_id)
        area_managers = AreaManager.get_all(company_id)
        division_heads = DivisionHead.get_all(company_id)
        
        # Calculate company-wide statistics
        total_sales = 0
        total_target = 0
        total_leads = 0
        
        high_risk_agents = 0
        medium_risk_agents = 0
        low_risk_agents = 0
        
        agent_data_list = []
        
        for agent in agents:
            agent_id = agent['_id']
            
            # Get performance
            performance = PerformanceService.get_agent_performance(agent_id, company_id)
            total_sales += performance.get('total_sales', 0)
            total_target += agent.get('monthly_target', 0)
            
            # Get prediction
            try:
                prediction = PredictorService.predict_agent(agent_id)
                risk_level = prediction.get('risk_level', 'UNKNOWN')
                
                if risk_level == 'HIGH':
                    high_risk_agents += 1
                elif risk_level == 'MEDIUM':
                    medium_risk_agents += 1
                elif risk_level == 'LOW':
                    low_risk_agents += 1
            except:
                prediction = {'risk_level': 'UNKNOWN', 'confidence': 0}
            
            agent_data_list.append({
                'agent': agent,
                'performance': performance,
                'prediction': prediction
            })
        
        # Get leads count
        from core.database import db
        total_leads = db.leads.count_documents({"company_id": company_id})
        total_sales_count = db.sales.count_documents({"company_id": company_id})
        
        # Calculate achievement rate
        achievement_rate = (total_sales / total_target * 100) if total_target > 0 else 0
        
        # Calculate monthly cost
        try:
            monthly_cost = Subscription.calculate_monthly_cost(company_id)
        except:
            # If calculation fails, use agent count * price per agent
            monthly_cost = len(agents) * Subscription.PRICE_PER_AGENT
        
        # Sort agents by risk
        risk_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2, 'UNKNOWN': 3}
        agent_data_list.sort(key=lambda x: risk_order.get(x['prediction']['risk_level'], 999))
        
        # Get recent activity (last 5 sales)
        recent_sales = list(db.sales.find({"company_id": company_id}).sort("date", -1).limit(5))
        
        context = {
            'user': user,
            'company': company,
            'subscription': subscription,
            'monthly_cost': monthly_cost,
            'stats': {
                'total_agents': len(agents),
                'total_area_managers': len(area_managers),
                'total_division_heads': len(division_heads),
                'total_sales': total_sales,
                'total_target': total_target,
                'achievement_rate': achievement_rate,
                'total_leads': total_leads,
                'total_sales_count': total_sales_count,
                'high_risk_agents': high_risk_agents,
                'medium_risk_agents': medium_risk_agents,
                'low_risk_agents': low_risk_agents
            },
            'agents': agent_data_list[:10],  # Show top 10 agents
            'recent_sales': recent_sales
        }
        
        return render(request, 'company_admin_dashboard.html', context)
    
    except Exception as e:
        import traceback
        error_details = {
            'error': str(e),
            'traceback': traceback.format_exc(),
            'user': request.user if hasattr(request, 'user') else None,
            'company_id': company_id if 'company_id' in locals() else 'Not set',
            'stats': {
                'total_agents': 0,
                'total_area_managers': 0,
                'total_division_heads': 0,
                'total_sales': 0,
                'total_target': 0,
                'achievement_rate': 0,
                'total_leads': 0,
                'total_sales_count': 0,
                'high_risk_agents': 0,
                'medium_risk_agents': 0,
                'low_risk_agents': 0
            },
            'agents': [],
            'recent_sales': [],
            'company': {'name': 'Error loading company', 'status': 'unknown'},
            'subscription': {'status': 'unknown'},
            'monthly_cost': 0
        }
        
        # Log the error
        print(f"Dashboard Error: {str(e)}")
        print(traceback.format_exc())
        
        return render(request, 'company_admin_dashboard.html', error_details)


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
