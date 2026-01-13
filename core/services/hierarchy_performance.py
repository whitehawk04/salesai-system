"""
Hierarchy Performance Service
Aggregates performance data for Area Managers and Division Heads
"""
from core.models import Agent, AreaManager, DivisionHead
from core.services.performance import PerformanceService
from core.services.predictor import PredictorService


class HierarchyPerformanceService:
    """Service for calculating hierarchical performance metrics"""
    
    @staticmethod
    def get_area_manager_performance(manager_id):
        """
        Get aggregated performance for an area manager's team
        Returns performance summary and list of agents
        """
        manager = AreaManager.get(manager_id)
        if not manager:
            return None
        
        # Get all agents under this manager
        agents = Agent.get_by_area_manager(manager_id)
        
        if not agents:
            return {
                'manager': manager,
                'manager_id': manager_id,
                'agents': [],
                'summary': {
                    'total_agents': 0,
                    'total_sales': 0,
                    'total_target': 0,
                    'achievement_percentage': 0,
                    'average_score': 0,
                    'high_risk_count': 0,
                    'medium_risk_count': 0,
                    'low_risk_count': 0
                }
            }
        
        # Collect agent performance data
        agents_data = []
        total_sales = 0
        total_target = 0
        total_score = 0
        risk_counts = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0, 'UNKNOWN': 0}
        
        for agent in agents:
            agent_id = agent['_id']
            
            # Get performance
            performance = PerformanceService.get_agent_performance(agent_id)
            
            # Get prediction
            try:
                prediction = PredictorService.predict_agent(agent_id)
            except:
                prediction = {
                    'prediction': 'N/A',
                    'risk_level': 'UNKNOWN',
                    'confidence': 0
                }
            
            agents_data.append({
                'agent': agent,
                'agent_id': agent_id,
                'performance': performance,
                'prediction': prediction
            })
            
            # Aggregate metrics
            if performance:
                total_sales += performance['sales']['actual']
                total_target += performance['sales']['target']
                total_score += performance['overall_score']
                risk_counts[prediction['risk_level']] += 1
        
        # Calculate summary
        achievement_percentage = (total_sales / total_target * 100) if total_target > 0 else 0
        average_score = total_score / len(agents) if agents else 0
        
        return {
            'manager': manager,
            'manager_id': manager_id,
            'agents': agents_data,
            'summary': {
                'total_agents': len(agents),
                'total_sales': total_sales,
                'total_target': total_target,
                'achievement_percentage': achievement_percentage,
                'average_score': round(average_score, 2),
                'high_risk_count': risk_counts['HIGH'],
                'medium_risk_count': risk_counts['MEDIUM'],
                'low_risk_count': risk_counts['LOW']
            }
        }
    
    @staticmethod
    def get_division_head_performance(head_id):
        """
        Get aggregated performance for a division head's areas
        Returns performance summary and list of area managers
        """
        head = DivisionHead.get(head_id)
        if not head:
            return None
        
        # Get all area managers under this division head
        area_managers = AreaManager.get_by_division_head(head_id)
        
        if not area_managers:
            return {
                'division_head': head,
                'head_id': head_id,
                'areas': [],
                'summary': {
                    'total_areas': 0,
                    'total_agents': 0,
                    'total_sales': 0,
                    'total_target': 0,
                    'achievement_percentage': 0,
                    'average_score': 0,
                    'high_risk_count': 0,
                    'medium_risk_count': 0,
                    'low_risk_count': 0
                }
            }
        
        # Collect area manager performance data
        areas_data = []
        division_total_sales = 0
        division_total_target = 0
        division_total_agents = 0
        division_total_score = 0
        division_risk_counts = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        
        for manager in area_managers:
            manager_id = manager['_id']
            
            # Get area manager's performance
            area_performance = HierarchyPerformanceService.get_area_manager_performance(manager_id)
            
            if area_performance:
                areas_data.append(area_performance)
                
                # Aggregate division metrics
                summary = area_performance['summary']
                division_total_sales += summary['total_sales']
                division_total_target += summary['total_target']
                division_total_agents += summary['total_agents']
                division_total_score += summary['average_score'] * summary['total_agents']
                division_risk_counts['HIGH'] += summary['high_risk_count']
                division_risk_counts['MEDIUM'] += summary['medium_risk_count']
                division_risk_counts['LOW'] += summary['low_risk_count']
        
        # Calculate division summary
        achievement_percentage = (division_total_sales / division_total_target * 100) if division_total_target > 0 else 0
        average_score = division_total_score / division_total_agents if division_total_agents > 0 else 0
        
        return {
            'division_head': head,
            'head_id': head_id,
            'areas': areas_data,
            'summary': {
                'total_areas': len(area_managers),
                'total_agents': division_total_agents,
                'total_sales': division_total_sales,
                'total_target': division_total_target,
                'achievement_percentage': achievement_percentage,
                'average_score': round(average_score, 2),
                'high_risk_count': division_risk_counts['HIGH'],
                'medium_risk_count': division_risk_counts['MEDIUM'],
                'low_risk_count': division_risk_counts['LOW']
            }
        }
