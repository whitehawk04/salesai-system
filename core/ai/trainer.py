"""
AI Model Training Module
Trains RandomForest classifier to predict agent performance
"""
import os
import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from datetime import datetime, timedelta
from core.models import Agent, Activity, Sale


class AITrainer:
    """AI Training Service using RandomForest"""
    
    MODEL_PATH = 'core/ai/model.pkl'
    
    @staticmethod
    def generate_training_data():
        """
        Generate training data from historical agent performance
        Returns DataFrame with features and labels
        """
        agents = Agent.get_all()
        training_data = []
        
        for agent in agents:
            agent_id = agent['_id']
            monthly_target = agent.get('monthly_target', 0)
            
            # Get data for the last 6 months
            for month_offset in range(6):
                # Calculate date range for this month
                now = datetime.now()
                target_month = now.month - month_offset
                target_year = now.year
                
                # Adjust year if needed
                while target_month <= 0:
                    target_month += 12
                    target_year -= 1
                
                start_date = datetime(target_year, target_month, 1)
                
                # Calculate end date
                if target_month == 12:
                    end_date = datetime(target_year + 1, 1, 1)
                else:
                    end_date = datetime(target_year, target_month + 1, 1)
                
                # Get activity counts
                calls = Activity.count_by_agent(agent_id, 'call', start_date, end_date)
                meetings = Activity.count_by_agent(agent_id, 'meeting', start_date, end_date)
                leads = Activity.count_by_agent(agent_id, 'lead', start_date, end_date)
                deals = Activity.count_by_agent(agent_id, 'deal', start_date, end_date)
                
                # Get total sales
                total_sales = Sale.get_total_by_agent(agent_id, start_date, end_date)
                
                # Calculate additional features
                sales_percentage = (total_sales / monthly_target * 100) if monthly_target > 0 else 0
                conversion_rate = (deals / leads * 100) if leads > 0 else 0
                meeting_to_deal = (deals / meetings * 100) if meetings > 0 else 0
                
                # Get funnel-specific conversion rates
                calls_to_leads = (leads / calls * 100) if calls > 0 else 0
                leads_to_meetings = (meetings / leads * 100) if leads > 0 else 0
                meetings_to_deals = (deals / meetings * 100) if meetings > 0 else 0
                
                # Calculate funnel efficiency (overall conversion from calls to deals)
                funnel_efficiency = (deals / calls * 100) if calls > 0 else 0
                
                # Calculate activity velocity (activities per day)
                days_in_month = (end_date - start_date).days
                activity_velocity = (calls + meetings + leads + deals) / days_in_month if days_in_month > 0 else 0
                
                # Determine label (HIT or MISS)
                label = 1 if total_sales >= monthly_target else 0  # 1 = HIT, 0 = MISS
                
                training_data.append({
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
                    'activity_velocity': activity_velocity,
                    'label': label
                })
        
        return pd.DataFrame(training_data)
    
    @staticmethod
    def train_model(test_size=0.2, random_state=42):
        """
        Train RandomForest model on historical data
        Returns model and accuracy metrics
        """
        print("Generating training data...")
        df = AITrainer.generate_training_data()
        
        if len(df) < 10:
            print("Warning: Insufficient training data. Need at least 10 samples.")
            print("Generating synthetic training data for demonstration...")
            df = AITrainer.generate_synthetic_data()
        
        print(f"Training data shape: {df.shape}")
        print(f"Label distribution:\n{df['label'].value_counts()}")
        
        # Separate features and labels
        X = df.drop('label', axis=1)
        y = df['label']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        print("\nTraining RandomForest model...")
        # Train model
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=random_state,
            n_jobs=-1
        )
        model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Calculate accuracy
        accuracy = accuracy_score(y_test, y_pred)
        print(f"\nModel Accuracy: {accuracy * 100:.2f}%")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['MISS', 'HIT']))
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\nFeature Importance:")
        print(feature_importance)
        
        # Save model
        os.makedirs(os.path.dirname(AITrainer.MODEL_PATH), exist_ok=True)
        with open(AITrainer.MODEL_PATH, 'wb') as f:
            pickle.dump(model, f)
        
        print(f"\nModel saved to {AITrainer.MODEL_PATH}")
        
        return model, accuracy
    
    @staticmethod
    def generate_synthetic_data(n_samples=100):
        """
        Generate synthetic training data for demonstration purposes
        """
        np.random.seed(42)
        
        data = []
        for _ in range(n_samples):
            # Generate base metrics
            calls = np.random.randint(50, 150)
            meetings = np.random.randint(20, 60)
            leads = np.random.randint(15, 50)
            deals = np.random.randint(5, 25)
            monthly_target = np.random.randint(300000, 800000)
            
            # Sales correlate with activities (but with noise)
            base_sales = (calls * 2000 + meetings * 5000 + leads * 8000 + deals * 15000) / 4
            noise = np.random.normal(0, 50000)
            total_sales = max(0, base_sales + noise)
            
            sales_percentage = (total_sales / monthly_target * 100)
            conversion_rate = (deals / leads * 100) if leads > 0 else 0
            meeting_to_deal = (deals / meetings * 100) if meetings > 0 else 0
            
            # Label: HIT if sales >= 90% of target
            label = 1 if total_sales >= (monthly_target * 0.9) else 0
            
            data.append({
                'calls': calls,
                'meetings': meetings,
                'leads': leads,
                'deals': deals,
                'total_sales': total_sales,
                'monthly_target': monthly_target,
                'sales_percentage': sales_percentage,
                'conversion_rate': conversion_rate,
                'meeting_to_deal': meeting_to_deal,
                'label': label
            })
        
        return pd.DataFrame(data)
