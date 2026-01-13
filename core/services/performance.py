"""
Performance calculation service
Calculates agent performance based on activities and sales
"""
from datetime import datetime, timedelta
from core.models import Agent, Activity, Sale


class PerformanceService:
    """Service for calculating agent performance metrics"""
    
    # Performance weights
    WEIGHTS = {
        'calls': 0.15,
        'meetings': 0.25,
        'leads': 0.20,
        'deals': 0.20,
        'sales': 0.20
    }
    
    # Expected monthly activity targets
    MONTHLY_TARGETS = {
        'calls': 100,      # 100 calls per month
        'meetings': 40,    # 40 meetings per month
        'leads': 30,       # 30 leads per month
        'deals': 15        # 15 deals per month
    }
    
    @staticmethod
    def get_current_month_range():
        """Get start and end date of current month"""
        now = datetime.now()
        start_date = datetime(now.year, now.month, 1)
        
        # Calculate next month
        if now.month == 12:
            end_date = datetime(now.year + 1, 1, 1)
        else:
            end_date = datetime(now.year, now.month + 1, 1)
        
        return start_date, end_date
    
    @staticmethod
    def calculate_activity_score(count, target):
        """Calculate score for an activity type (0-100)"""
        if target == 0:
            return 0
        score = (count / target) * 100
        return min(score, 100)  # Cap at 100
    
    @staticmethod
    def calculate_sales_score(actual_sales, target_sales):
        """Calculate sales achievement score (0-100)"""
        if target_sales == 0:
            return 0
        score = (actual_sales / target_sales) * 100
        return min(score, 100)  # Cap at 100
    
    @staticmethod
    def get_agent_performance(agent_id):
        """
        Calculate comprehensive performance for an agent
        Returns dict with scores and metrics
        """
        agent = Agent.get(agent_id)
        if not agent:
            return None
        
        start_date, end_date = PerformanceService.get_current_month_range()
        
        # Get activity counts
        calls_count = Activity.count_by_agent(agent_id, 'call', start_date, end_date)
        meetings_count = Activity.count_by_agent(agent_id, 'meeting', start_date, end_date)
        leads_count = Activity.count_by_agent(agent_id, 'lead', start_date, end_date)
        deals_count = Activity.count_by_agent(agent_id, 'deal', start_date, end_date)
        
        # Get total sales
        total_sales = Sale.get_total_by_agent(agent_id, start_date, end_date)
        target_sales = agent.get('monthly_target', 0)
        
        # Calculate individual scores
        calls_score = PerformanceService.calculate_activity_score(
            calls_count, PerformanceService.MONTHLY_TARGETS['calls']
        )
        meetings_score = PerformanceService.calculate_activity_score(
            meetings_count, PerformanceService.MONTHLY_TARGETS['meetings']
        )
        leads_score = PerformanceService.calculate_activity_score(
            leads_count, PerformanceService.MONTHLY_TARGETS['leads']
        )
        deals_score = PerformanceService.calculate_activity_score(
            deals_count, PerformanceService.MONTHLY_TARGETS['deals']
        )
        sales_score = PerformanceService.calculate_sales_score(total_sales, target_sales)
        
        # Calculate weighted overall score
        overall_score = (
            calls_score * PerformanceService.WEIGHTS['calls'] +
            meetings_score * PerformanceService.WEIGHTS['meetings'] +
            leads_score * PerformanceService.WEIGHTS['leads'] +
            deals_score * PerformanceService.WEIGHTS['deals'] +
            sales_score * PerformanceService.WEIGHTS['sales']
        )
        
        # Determine performance level
        if overall_score >= 80:
            performance_level = 'Excellent'
        elif overall_score >= 60:
            performance_level = 'Good'
        elif overall_score >= 40:
            performance_level = 'Average'
        else:
            performance_level = 'Poor'
        
        return {
            'agent_id': agent_id,
            'agent_name': agent.get('name'),
            'month': start_date.strftime('%B %Y'),
            'activities': {
                'calls': {'count': calls_count, 'target': PerformanceService.MONTHLY_TARGETS['calls'], 'score': calls_score},
                'meetings': {'count': meetings_count, 'target': PerformanceService.MONTHLY_TARGETS['meetings'], 'score': meetings_score},
                'leads': {'count': leads_count, 'target': PerformanceService.MONTHLY_TARGETS['leads'], 'score': leads_score},
                'deals': {'count': deals_count, 'target': PerformanceService.MONTHLY_TARGETS['deals'], 'score': deals_score},
            },
            'sales': {
                'actual': total_sales,
                'target': target_sales,
                'score': sales_score,
                'percentage': (total_sales / target_sales * 100) if target_sales > 0 else 0
            },
            'overall_score': round(overall_score, 2),
            'performance_level': performance_level
        }
    
    @staticmethod
    def get_all_agents_performance():
        """Get performance data for all agents"""
        agents = Agent.get_all()
        performances = []
        
        for agent in agents:
            perf = PerformanceService.get_agent_performance(agent['_id'])
            if perf:
                performances.append(perf)
        
        return performances
