"""
Prediction service using trained AI model
"""
import os
import pickle
import pandas as pd
from datetime import datetime
from core.models import Agent, Activity, Sale
from core.ai.trainer import AITrainer
from core.services.sales_funnel import SalesFunnelService
from core.services.funnel_analyzer import FunnelAnalyzer


class PredictorService:
    """Service for making predictions using trained AI model"""
    
    _model = None
    
    @classmethod
    def load_model(cls):
        """Load trained model from disk"""
        if cls._model is None:
            if os.path.exists(AITrainer.MODEL_PATH):
                with open(AITrainer.MODEL_PATH, 'rb') as f:
                    cls._model = pickle.load(f)
            else:
                raise FileNotFoundError(
                    f"Model not found at {AITrainer.MODEL_PATH}. "
                    "Please train the model first using AITrainer.train_model()"
                )
        return cls._model
    
    @staticmethod
    def get_current_month_range():
        """Get start and end date of current month"""
        now = datetime.now()
        start_date = datetime(now.year, now.month, 1)
        
        if now.month == 12:
            end_date = datetime(now.year + 1, 1, 1)
        else:
            end_date = datetime(now.year, now.month + 1, 1)
        
        return start_date, end_date
    
    @staticmethod
    def prepare_agent_features(agent_id):
        """
        Prepare features for prediction from current month's data
        """
        agent = Agent.get(agent_id)
        if not agent:
            return None
        
        start_date, end_date = PredictorService.get_current_month_range()
        
        # Get activity counts
        calls = Activity.count_by_agent(agent_id, 'call', start_date, end_date)
        meetings = Activity.count_by_agent(agent_id, 'meeting', start_date, end_date)
        leads = Activity.count_by_agent(agent_id, 'lead', start_date, end_date)
        deals = Activity.count_by_agent(agent_id, 'deal', start_date, end_date)
        
        # Get total sales
        total_sales = Sale.get_total_by_agent(agent_id, start_date, end_date)
        monthly_target = agent.get('monthly_target', 0)
        
        # Calculate additional features
        sales_percentage = (total_sales / monthly_target * 100) if monthly_target > 0 else 0
        conversion_rate = (deals / leads * 100) if leads > 0 else 0
        meeting_to_deal = (deals / meetings * 100) if meetings > 0 else 0
        
        # Calculate funnel-specific conversion rates
        calls_to_leads = (leads / calls * 100) if calls > 0 else 0
        leads_to_meetings = (meetings / leads * 100) if leads > 0 else 0
        meetings_to_deals = (deals / meetings * 100) if meetings > 0 else 0
        
        # Calculate funnel efficiency (overall conversion from calls to deals)
        funnel_efficiency = (deals / calls * 100) if calls > 0 else 0
        
        # Calculate activity velocity
        days_in_month = (end_date - start_date).days
        activity_velocity = (calls + meetings + leads + deals) / days_in_month if days_in_month > 0 else 0
        
        features = {
            'calls': calls,
            'meetings': meetings,
            'leads': leads,
            'deals': deals,
            'total_sales': total_sales,
            'monthly_target': monthly_target,
            'sales_percentage': sales_percentage,
            'conversion_rate': conversion_rate,
            'meeting_to_deal': meeting_to_deal,
            'calls_to_leads_conversion': calls_to_leads,
            'leads_to_meetings_conversion': leads_to_meetings,
            'meetings_to_deals_conversion': meetings_to_deals,
            'funnel_efficiency': funnel_efficiency,
            'activity_velocity': activity_velocity
        }
        
        return pd.DataFrame([features])
    
    @staticmethod
    def predict_agent(agent_id):
        """
        Predict if agent will HIT or MISS their target
        Returns dict with prediction and probability
        """
        # Load model
        model = PredictorService.load_model()
        
        # Prepare features
        features = PredictorService.prepare_agent_features(agent_id)
        if features is None:
            return None
        
        # Make prediction
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0]
        
        # Get agent info
        agent = Agent.get(agent_id)
        
        # Handle probability array (may have 1 or 2 values depending on classes seen in training)
        if len(probability) == 2:
            prob_miss = probability[0]
            prob_hit = probability[1]
        else:
            # Only one class seen in training data
            prob_miss = probability[0] if prediction == 0 else 1 - probability[0]
            prob_hit = 1 - prob_miss
        
        result = {
            'agent_id': agent_id,
            'agent_name': agent.get('name'),
            'prediction': 'HIT' if prediction == 1 else 'MISS',
            'confidence': max(probability) * 100,
            'probability_hit': prob_hit * 100,
            'probability_miss': prob_miss * 100,
            'risk_level': PredictorService.calculate_risk_level(prob_miss),
            'features': features.to_dict('records')[0]
        }
        
        return result
    
    @staticmethod
    def calculate_risk_level(miss_probability):
        """Calculate risk level based on miss probability"""
        if miss_probability >= 0.7:
            return 'HIGH'
        elif miss_probability >= 0.4:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    @staticmethod
    def get_prediction_with_funnel_insights(agent_id):
        """
        Get prediction with detailed funnel insights and AI-driven analysis
        Returns prediction plus comprehensive funnel analysis
        """
        # Get standard prediction
        prediction = PredictorService.predict_agent(agent_id)
        if not prediction:
            return None
        
        # Get detailed funnel metrics
        funnel_data = SalesFunnelService.get_funnel_metrics(agent_id)
        
        # Get advanced funnel analysis
        funnel_analysis = FunnelAnalyzer.analyze_funnel_stages(agent_id)
        
        # Get AI recommendations
        ai_recommendations = FunnelAnalyzer.get_ai_recommendations(agent_id)
        
        # Combine all insights
        prediction['funnel_metrics'] = funnel_data
        prediction['funnel_health'] = funnel_data['funnel_health']
        prediction['funnel_recommendations'] = funnel_data['recommendations']
        prediction['weakest_stage'] = funnel_data['weakest_stage']
        
        # Add advanced analysis
        prediction['funnel_analysis'] = funnel_analysis
        prediction['ai_recommendations'] = ai_recommendations
        prediction['funnel_score'] = funnel_analysis['funnel_score']
        prediction['primary_bottleneck'] = funnel_analysis['primary_bottleneck']
        
        return prediction
    
    @staticmethod
    def predict_all_agents():
        """Predict for all agents"""
        agents = Agent.get_all()
        predictions = []
        
        for agent in agents:
            try:
                pred = PredictorService.predict_agent(agent['_id'])
                if pred:
                    predictions.append(pred)
            except Exception as e:
                print(f"Error predicting for agent {agent['_id']}: {e}")
        
        return predictions
