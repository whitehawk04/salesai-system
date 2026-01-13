"""
Advanced Sales Funnel Analyzer with AI Insights
Provides detailed stage-by-stage analysis and bottleneck detection
"""
from core.services.sales_funnel import SalesFunnelService


class FunnelAnalyzer:
    """Advanced analyzer for sales funnel with AI-driven insights"""
    
    # Benchmark conversion rates (industry standards for banking sales)
    BENCHMARKS = {
        'calls_to_leads': 25.0,  # 25% of calls should convert to leads
        'leads_to_meetings': 50.0,  # 50% of leads should convert to meetings
        'meetings_to_deals': 60.0,  # 60% of meetings should convert to deals
        'deals_to_sales': 70.0,  # 70% of deals should close
        'overall': 8.0  # 8% overall conversion from calls to sales
    }
    
    @staticmethod
    def analyze_funnel_stages(agent_id):
        """
        Perform deep analysis on each funnel stage
        Returns detailed insights for each conversion point
        """
        funnel = SalesFunnelService.get_funnel_metrics(agent_id)
        
        stages_analysis = []
        
        # Analyze each stage transition
        stages = [
            {
                'name': 'Prospecting (Calls to Leads)',
                'conversion': funnel['conversion_rates']['calls_to_leads'],
                'benchmark': FunnelAnalyzer.BENCHMARKS['calls_to_leads'],
                'from_count': funnel['counts']['calls'],
                'to_count': funnel['counts']['leads'],
                'stage_key': 'calls_to_leads'
            },
            {
                'name': 'Lead Qualification (Leads to Meetings)',
                'conversion': funnel['conversion_rates']['leads_to_meetings'],
                'benchmark': FunnelAnalyzer.BENCHMARKS['leads_to_meetings'],
                'from_count': funnel['counts']['leads'],
                'to_count': funnel['counts']['meetings'],
                'stage_key': 'leads_to_meetings'
            },
            {
                'name': 'Meeting to Proposal (Meetings to Deals)',
                'conversion': funnel['conversion_rates']['meetings_to_deals'],
                'benchmark': FunnelAnalyzer.BENCHMARKS['meetings_to_deals'],
                'from_count': funnel['counts']['meetings'],
                'to_count': funnel['counts']['deals'],
                'stage_key': 'meetings_to_deals'
            },
            {
                'name': 'Deal Closing (Deals to Sales)',
                'conversion': funnel['conversion_rates']['deals_to_sales'],
                'benchmark': FunnelAnalyzer.BENCHMARKS['deals_to_sales'],
                'from_count': funnel['counts']['deals'],
                'to_count': funnel['counts']['closed_sales'],
                'stage_key': 'deals_to_sales'
            }
        ]
        
        for stage in stages:
            analysis = FunnelAnalyzer._analyze_stage(stage)
            stages_analysis.append(analysis)
        
        # Identify primary bottleneck
        bottlenecks = [s for s in stages_analysis if s['status'] == 'CRITICAL']
        primary_bottleneck = bottlenecks[0] if bottlenecks else None
        
        # Calculate overall health
        overall_health = FunnelAnalyzer._calculate_overall_health(stages_analysis)
        
        return {
            'stages_analysis': stages_analysis,
            'primary_bottleneck': primary_bottleneck,
            'overall_health': overall_health,
            'funnel_score': FunnelAnalyzer._calculate_funnel_score(stages_analysis)
        }
    
    @staticmethod
    def _analyze_stage(stage):
        """Analyze a single funnel stage"""
        conversion = stage['conversion']
        benchmark = stage['benchmark']
        
        # Calculate performance vs benchmark
        performance_gap = conversion - benchmark
        performance_percentage = (conversion / benchmark * 100) if benchmark > 0 else 0
        
        # Determine status
        if performance_percentage >= 100:
            status = 'EXCELLENT'
            status_color = 'green'
        elif performance_percentage >= 80:
            status = 'GOOD'
            status_color = 'blue'
        elif performance_percentage >= 60:
            status = 'NEEDS IMPROVEMENT'
            status_color = 'orange'
        else:
            status = 'CRITICAL'
            status_color = 'red'
        
        # Generate insights
        insights = FunnelAnalyzer._generate_stage_insights(stage, performance_gap, status)
        
        # Calculate potential impact
        potential_improvement = FunnelAnalyzer._calculate_potential_impact(stage, benchmark)
        
        return {
            'name': stage['name'],
            'stage_key': stage['stage_key'],
            'conversion': conversion,
            'benchmark': benchmark,
            'performance_gap': performance_gap,
            'performance_percentage': performance_percentage,
            'status': status,
            'status_color': status_color,
            'from_count': stage['from_count'],
            'to_count': stage['to_count'],
            'insights': insights,
            'potential_improvement': potential_improvement
        }
    
    @staticmethod
    def _generate_stage_insights(stage, performance_gap, status):
        """Generate AI-driven insights for a stage"""
        insights = []
        
        stage_key = stage['stage_key']
        
        if status == 'CRITICAL':
            # Critical issues
            if stage_key == 'calls_to_leads':
                insights.append({
                    'type': 'warning',
                    'title': 'Low Lead Generation',
                    'message': f"Only {stage['conversion']:.1f}% of calls convert to leads (target: {stage['benchmark']:.0f}%)",
                    'action': 'Improve prospect targeting and qualification criteria'
                })
            elif stage_key == 'leads_to_meetings':
                insights.append({
                    'type': 'warning',
                    'title': 'Poor Meeting Conversion',
                    'message': f"Only {stage['conversion']:.1f}% of leads convert to meetings",
                    'action': 'Strengthen follow-up process and value proposition'
                })
            elif stage_key == 'meetings_to_deals':
                insights.append({
                    'type': 'warning',
                    'title': 'Low Proposal Rate',
                    'message': f"Only {stage['conversion']:.1f}% of meetings result in deals",
                    'action': 'Enhance needs discovery and proposal presentation skills'
                })
            elif stage_key == 'deals_to_sales':
                insights.append({
                    'type': 'warning',
                    'title': 'Weak Closing Rate',
                    'message': f"Only {stage['conversion']:.1f}% of deals close successfully",
                    'action': 'Focus on objection handling and closing techniques'
                })
        
        elif status == 'NEEDS IMPROVEMENT':
            # Moderate issues
            insights.append({
                'type': 'info',
                'title': 'Room for Improvement',
                'message': f"Conversion at {stage['conversion']:.1f}% (target: {stage['benchmark']:.0f}%)",
                'action': f"Small improvements here can yield {abs(performance_gap):.1f}% better results"
            })
        
        elif status == 'EXCELLENT':
            # Positive reinforcement
            insights.append({
                'type': 'success',
                'title': 'Strong Performance',
                'message': f"Exceeding benchmark by {performance_gap:.1f}%",
                'action': 'Maintain current practices and share best practices with team'
            })
        
        return insights
    
    @staticmethod
    def _calculate_potential_impact(stage, benchmark):
        """Calculate potential impact of improving this stage"""
        current_conversion = stage['conversion']
        from_count = stage['from_count']
        
        if from_count == 0:
            return 0
        
        # Calculate how many more conversions at benchmark
        current_conversions = stage['to_count']
        potential_conversions = int(from_count * (benchmark / 100))
        additional_conversions = max(0, potential_conversions - current_conversions)
        
        return additional_conversions
    
    @staticmethod
    def _calculate_overall_health(stages_analysis):
        """Calculate overall funnel health"""
        critical_count = sum(1 for s in stages_analysis if s['status'] == 'CRITICAL')
        needs_improvement_count = sum(1 for s in stages_analysis if s['status'] == 'NEEDS IMPROVEMENT')
        
        if critical_count >= 2:
            return 'CRITICAL'
        elif critical_count == 1:
            return 'NEEDS ATTENTION'
        elif needs_improvement_count >= 2:
            return 'FAIR'
        elif needs_improvement_count == 1:
            return 'GOOD'
        else:
            return 'EXCELLENT'
    
    @staticmethod
    def _calculate_funnel_score(stages_analysis):
        """Calculate overall funnel score (0-100)"""
        total_score = sum(s['performance_percentage'] for s in stages_analysis)
        avg_score = total_score / len(stages_analysis) if stages_analysis else 0
        return round(min(100, avg_score), 1)
    
    @staticmethod
    def get_ai_recommendations(agent_id):
        """
        Get AI-powered recommendations based on funnel analysis
        """
        analysis = FunnelAnalyzer.analyze_funnel_stages(agent_id)
        
        recommendations = []
        
        # Prioritize recommendations by impact
        stages_by_impact = sorted(
            analysis['stages_analysis'],
            key=lambda x: (x['status'] == 'CRITICAL', x['potential_improvement']),
            reverse=True
        )
        
        # Add top 3 recommendations
        for i, stage in enumerate(stages_by_impact[:3]):
            if stage['insights']:
                priority = 'HIGH' if i == 0 else 'MEDIUM' if i == 1 else 'LOW'
                for insight in stage['insights']:
                    recommendations.append({
                        'priority': priority,
                        'stage': stage['name'],
                        'issue': insight['message'],
                        'action': insight['action'],
                        'potential_impact': f"+{stage['potential_improvement']} conversions"
                    })
        
        return recommendations
