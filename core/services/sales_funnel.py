"""
Sales Funnel Service
Analyzes agent performance through sales funnel stages and conversion rates
"""
from core.models import Activity, Sale
from datetime import datetime


class SalesFunnelService:
    """Service for analyzing sales funnel metrics and conversion rates"""
    
    @staticmethod
    def get_funnel_metrics(agent_id, start_date=None):
        """
        Calculate sales funnel metrics for an agent
        
        Funnel Stages:
        1. Prospects (Calls) - Initial outreach
        2. Qualified Leads - Interested prospects  
        3. Meetings - Face-to-face engagement
        4. Proposals (Deals) - Deals in negotiation
        5. Closed Sales - Successful sales
        
        Returns conversion rates and bottleneck analysis
        """
        if start_date is None:
            # Default to current month
            now = datetime.now()
            start_date = datetime(now.year, now.month, 1)
        
        # Get activity counts by type
        activities = Activity.get_by_agent(agent_id)
        
        calls_count = 0
        leads_count = 0
        meetings_count = 0
        deals_count = 0
        
        for activity in activities:
            activity_type = activity.get('type', '')  # Activity model stores as 'type' not 'activity_type'
            if activity_type == 'call':
                calls_count += 1
            elif activity_type == 'lead':
                leads_count += 1
            elif activity_type == 'meeting':
                meetings_count += 1
            elif activity_type == 'deal':
                deals_count += 1
        
        # Get closed sales count
        sales = Sale.get_by_agent(agent_id)
        closed_sales = len(sales)
        
        # Calculate conversion rates
        def safe_percentage(numerator, denominator):
            """Calculate percentage safely, avoiding division by zero"""
            if denominator == 0:
                return 0.0
            return round((numerator / denominator) * 100, 2)
        
        # Conversion rates
        calls_to_leads = safe_percentage(leads_count, calls_count)
        leads_to_meetings = safe_percentage(meetings_count, leads_count)
        meetings_to_deals = safe_percentage(deals_count, meetings_count)
        deals_to_sales = safe_percentage(closed_sales, deals_count)
        
        # Overall funnel efficiency (calls to closed sales)
        overall_conversion = safe_percentage(closed_sales, calls_count)
        
        # Identify bottlenecks (stages with lowest conversion rates)
        conversion_rates = {
            'calls_to_leads': calls_to_leads,
            'leads_to_meetings': leads_to_meetings,
            'meetings_to_deals': meetings_to_deals,
            'deals_to_sales': deals_to_sales
        }
        
        # Find weakest stage
        if conversion_rates:
            weakest_stage = min(conversion_rates, key=conversion_rates.get)
            weakest_rate = conversion_rates[weakest_stage]
        else:
            weakest_stage = None
            weakest_rate = 0
        
        # Determine funnel health
        if overall_conversion >= 10:
            funnel_health = 'EXCELLENT'
            health_color = 'green'
        elif overall_conversion >= 5:
            funnel_health = 'GOOD'
            health_color = 'blue'
        elif overall_conversion >= 2:
            funnel_health = 'FAIR'
            health_color = 'orange'
        else:
            funnel_health = 'NEEDS IMPROVEMENT'
            health_color = 'red'
        
        # Calculate funnel stage counts
        funnel_stages = [
            {
                'name': 'Prospects',
                'label': 'Calls Made',
                'count': calls_count,
                'percentage': 100,
                'color': '#667eea'
            },
            {
                'name': 'Qualified Leads',
                'label': 'Leads Generated',
                'count': leads_count,
                'percentage': safe_percentage(leads_count, calls_count),
                'conversion_from_previous': calls_to_leads,
                'color': '#764ba2'
            },
            {
                'name': 'Meetings',
                'label': 'Meetings Held',
                'count': meetings_count,
                'percentage': safe_percentage(meetings_count, calls_count),
                'conversion_from_previous': leads_to_meetings,
                'color': '#f093fb'
            },
            {
                'name': 'Proposals',
                'label': 'Deals in Progress',
                'count': deals_count,
                'percentage': safe_percentage(deals_count, calls_count),
                'conversion_from_previous': meetings_to_deals,
                'color': '#f5576c'
            },
            {
                'name': 'Closed Sales',
                'label': 'Sales Closed',
                'count': closed_sales,
                'percentage': safe_percentage(closed_sales, calls_count),
                'conversion_from_previous': deals_to_sales,
                'color': '#15803d'
            }
        ]
        
        # Recommendations based on bottlenecks
        recommendations = []
        
        if calls_to_leads < 20:
            recommendations.append({
                'stage': 'Lead Qualification',
                'issue': 'Low call-to-lead conversion',
                'suggestion': 'Improve prospect targeting and qualification criteria'
            })
        
        if leads_to_meetings < 40:
            recommendations.append({
                'stage': 'Meeting Booking',
                'issue': 'Low lead-to-meeting conversion',
                'suggestion': 'Enhance follow-up process and value proposition'
            })
        
        if meetings_to_deals < 50:
            recommendations.append({
                'stage': 'Deal Creation',
                'issue': 'Low meeting-to-deal conversion',
                'suggestion': 'Strengthen needs assessment and proposal skills'
            })
        
        if deals_to_sales < 60:
            recommendations.append({
                'stage': 'Deal Closing',
                'issue': 'Low deal-to-sale conversion',
                'suggestion': 'Focus on objection handling and closing techniques'
            })
        
        return {
            'stages': funnel_stages,
            'conversion_rates': {
                'calls_to_leads': calls_to_leads,
                'leads_to_meetings': leads_to_meetings,
                'meetings_to_deals': meetings_to_deals,
                'deals_to_sales': deals_to_sales,
                'overall': overall_conversion
            },
            'counts': {
                'calls': calls_count,
                'leads': leads_count,
                'meetings': meetings_count,
                'deals': deals_count,
                'closed_sales': closed_sales
            },
            'funnel_health': funnel_health,
            'health_color': health_color,
            'weakest_stage': weakest_stage,
            'weakest_rate': weakest_rate,
            'recommendations': recommendations,
            'funnel_efficiency_score': overall_conversion
        }
    
    @staticmethod
    def get_funnel_analysis_for_ai(agent_id):
        """
        Get funnel metrics formatted for AI analysis
        Returns key metrics that indicate sales process health
        """
        metrics = SalesFunnelService.get_funnel_metrics(agent_id)
        
        return {
            'overall_conversion': metrics['conversion_rates']['overall'],
            'calls_to_leads_conversion': metrics['conversion_rates']['calls_to_leads'],
            'leads_to_meetings_conversion': metrics['conversion_rates']['leads_to_meetings'],
            'meetings_to_deals_conversion': metrics['conversion_rates']['meetings_to_deals'],
            'deals_to_sales_conversion': metrics['conversion_rates']['deals_to_sales'],
            'funnel_efficiency_score': metrics['funnel_efficiency_score'],
            'has_bottleneck': len(metrics['recommendations']) > 0,
            'bottleneck_stage': metrics['weakest_stage']
        }
