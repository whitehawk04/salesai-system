# 📁 Project Structure

## Overview
```
salesAI/
├── manage.py                      # Django management script
├── setup_and_run.py              # Automated setup and launch script
├── requirements.txt              # Python dependencies
├── README.md                     # Main documentation
├── QUICKSTART.md                 # Quick start guide
├── DEPLOYMENT.md                 # Production deployment guide
├── .env.example                  # Environment variables template
├── .gitignore                    # Git ignore rules
│
├── salesAI/                      # Django project configuration
│   ├── __init__.py
│   ├── settings.py              # Django settings (MongoDB, apps, etc.)
│   ├── urls.py                  # Main URL routing
│   ├── wsgi.py                  # WSGI entry point
│   └── asgi.py                  # ASGI entry point
│
└── core/                         # Main application
    ├── __init__.py
    ├── apps.py                  # App configuration
    ├── views.py                 # View controllers
    ├── urls.py                  # App URL routing
    ├── database.py              # MongoDB connection manager
    │
    ├── models/                   # Data models
    │   ├── __init__.py
    │   ├── agent.py             # Agent model (sales representatives)
    │   ├── activity.py          # Activity model (calls, meetings, etc.)
    │   └── sale.py              # Sale model (transactions)
    │
    ├── services/                 # Business logic services
    │   ├── __init__.py
    │   ├── performance.py       # Performance calculation service
    │   └── predictor.py         # AI prediction service
    │
    ├── ai/                       # AI/ML components
    │   ├── __init__.py
    │   ├── trainer.py           # Model training with RandomForest
    │   └── model.pkl            # Trained model (generated)
    │
    ├── utils/                    # Utility functions
    │   ├── __init__.py
    │   └── sample_data.py       # Sample data generation
    │
    ├── management/               # Django management commands
    │   ├── __init__.py
    │   └── commands/
    │       ├── __init__.py
    │       └── setup_demo.py    # Demo setup command
    │
    └── templates/                # HTML templates
        ├── base.html            # Base template
        ├── dashboard.html       # Main dashboard
        ├── agent_detail.html    # Agent detail view
        └── train_model.html     # Model training interface
```

## 📦 Core Components

### 1. Models (`core/models/`)

#### Agent (`agent.py`)
Represents a sales agent.
```python
{
    "_id": "A101",
    "name": "Maria Santos",
    "email": "maria@company.com",
    "monthly_target": 600000,
    "created_at": datetime
}
```

**Methods:**
- `create(agent_id, name, email, monthly_target)` - Create new agent
- `get(agent_id)` - Retrieve agent by ID
- `get_all()` - Get all agents
- `update(agent_id, **kwargs)` - Update agent
- `delete(agent_id)` - Delete agent
- `exists(agent_id)` - Check if agent exists

#### Activity (`activity.py`)
Tracks agent activities (calls, meetings, leads, deals).
```python
{
    "_id": "ACT001",
    "agent_id": "A101",
    "type": "call|meeting|lead|deal",
    "value": 0,
    "date": datetime,
    "notes": "Activity description"
}
```

**Methods:**
- `create(activity_id, agent_id, activity_type, value, notes)` - Create activity
- `get(activity_id)` - Get activity by ID
- `get_by_agent(agent_id, activity_type, start_date, end_date)` - Get agent activities
- `count_by_agent(agent_id, activity_type, start_date, end_date)` - Count activities

#### Sale (`sale.py`)
Records completed sales transactions.
```python
{
    "_id": "S001",
    "agent_id": "A101",
    "amount": 50000,
    "customer": "ABC Corp",
    "date": datetime,
    "notes": "Sale details"
}
```

**Methods:**
- `create(sale_id, agent_id, amount, customer, notes)` - Create sale
- `get(sale_id)` - Get sale by ID
- `get_by_agent(agent_id, start_date, end_date)` - Get agent sales
- `get_total_by_agent(agent_id, start_date, end_date)` - Calculate total sales

### 2. Services (`core/services/`)

#### PerformanceService (`performance.py`)
Calculates agent performance scores.

**Performance Formula:**
```
Overall Score = (Calls × 0.15) + (Meetings × 0.25) + (Leads × 0.20) 
                + (Deals × 0.20) + (Sales Achievement × 0.20)
```

**Monthly Targets:**
- Calls: 100
- Meetings: 40
- Leads: 30
- Deals: 15
- Sales: Agent's monthly_target

**Methods:**
- `get_agent_performance(agent_id)` - Get comprehensive performance metrics
- `get_all_agents_performance()` - Get performance for all agents
- `calculate_activity_score(count, target)` - Calculate activity score
- `calculate_sales_score(actual, target)` - Calculate sales achievement

**Performance Levels:**
- **Excellent:** ≥80%
- **Good:** 60-79%
- **Average:** 40-59%
- **Poor:** <40%

#### PredictorService (`predictor.py`)
Makes predictions using trained AI model.

**Methods:**
- `predict_agent(agent_id)` - Predict if agent will HIT or MISS target
- `predict_all_agents()` - Predict for all agents
- `load_model()` - Load trained model from disk
- `calculate_risk_level(probability)` - Determine risk level

**Risk Levels:**
- **HIGH:** ≥70% probability of missing target
- **MEDIUM:** 40-69% probability of missing target
- **LOW:** <40% probability of missing target

### 3. AI Module (`core/ai/`)

#### AITrainer (`trainer.py`)
Trains RandomForest classifier for predictions.

**Features Used:**
1. calls - Number of calls made
2. meetings - Number of meetings held
3. leads - Number of leads generated
4. deals - Number of deals closed
5. total_sales - Total sales amount
6. monthly_target - Target amount
7. sales_percentage - Sales achievement %
8. conversion_rate - Deals/Leads ratio
9. meeting_to_deal - Deals/Meetings ratio

**Methods:**
- `train_model(test_size=0.2, random_state=42)` - Train the model
- `generate_training_data()` - Create training dataset from history
- `generate_synthetic_data(n_samples=100)` - Generate demo data

**Model Configuration:**
```python
RandomForestClassifier(
    n_estimators=100,      # 100 decision trees
    max_depth=10,          # Maximum tree depth
    random_state=42,       # For reproducibility
    n_jobs=-1             # Use all CPU cores
)
```

### 4. Views (`core/views.py`)

#### Endpoints:

**`dashboard(request)`**
- URL: `/`
- Shows all agents with performance and predictions
- Sorted by risk level (HIGH → MEDIUM → LOW)

**`agent_detail(request, agent_id)`**
- URL: `/agent/<agent_id>/`
- Detailed view of single agent
- Shows activities, sales, and AI prediction

**`train_model(request)`**
- URL: `/train/`
- GET: Shows training interface
- POST: Trains model and returns JSON response

**`api_agents(request)`**
- URL: `/api/agents/`
- Returns JSON with all agents data

### 5. Templates (`core/templates/`)

#### `base.html`
- Base template with navigation
- Gradient background design
- Responsive layout

#### `dashboard.html`
- Agent cards with metrics
- Risk badges (color-coded)
- Progress bars for sales
- Prediction results

#### `agent_detail.html`
- Comprehensive agent view
- Activity breakdown
- Sales information
- AI prediction details

#### `train_model.html`
- Model training interface
- AJAX-based training
- Shows accuracy results

## 🔧 Configuration

### Database (`core/database.py`)
MongoDB singleton connection manager.

**Collections:**
- `agents` - Sales agents
- `activities` - Agent activities
- `sales` - Sales transactions

**Usage:**
```python
from core.database import db

# Access collections
db.agents.find()
db.activities.insert_one({...})
db.sales.count_documents({...})
```

### Settings (`salesAI/settings.py`)
Django configuration with MongoDB integration.

**Key Settings:**
```python
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
MONGODB_NAME = 'sales_ai'
DATABASES = {}  # Not using Django ORM
```

## 🚀 Workflows

### 1. Initial Setup
```
Install dependencies → Configure MongoDB → Create sample data → Train model → Run server
```

### 2. Adding New Agent
```
Create agent → Add activities → Record sales → System calculates performance → AI predicts outcome
```

### 3. Model Training
```
Collect historical data → Generate features → Train RandomForest → Save model → Make predictions
```

### 4. Performance Monitoring
```
Dashboard → View agents → Check risk levels → Take action for HIGH risk agents
```

## 📊 Data Flow

```
MongoDB Atlas/Local
       ↓
   Database.py (Connection)
       ↓
   Models (Agent, Activity, Sale)
       ↓
   Services (Performance, Predictor)
       ↓
   Views (Dashboard, Detail)
       ↓
   Templates (HTML)
       ↓
   User Browser
```

## 🔐 Security Considerations

1. **Environment Variables:** Store sensitive data in `.env`
2. **MongoDB Authentication:** Use strong passwords
3. **Django Secret Key:** Generate unique key for production
4. **Debug Mode:** Disable in production
5. **HTTPS:** Use SSL certificates in production
6. **Input Validation:** Sanitize user inputs
7. **Access Control:** Implement authentication/authorization

## 🧪 Testing Strategy

1. **Unit Tests:** Test individual functions
2. **Integration Tests:** Test workflows
3. **Model Validation:** Verify prediction accuracy
4. **Load Testing:** Test with many agents
5. **Edge Cases:** Handle missing data gracefully

## 📈 Scalability

**Current Capacity:**
- Agents: Unlimited
- Activities: Millions (indexed by agent_id + date)
- Sales: Millions (indexed by agent_id + date)

**Optimization Tips:**
1. Add MongoDB indexes for frequently queried fields
2. Implement caching for dashboard data
3. Use background tasks for model training
4. Paginate large result sets
5. Use MongoDB aggregation pipelines

## 🎨 Customization Points

1. **Performance Weights:** Adjust in `performance.py`
2. **Activity Targets:** Modify in `performance.py`
3. **Model Parameters:** Change in `trainer.py`
4. **Risk Thresholds:** Update in `predictor.py`
5. **UI Styling:** Edit templates and CSS
6. **Additional Features:** Add to models/views

---

**This structure provides a solid foundation for a production-ready sales performance tracking system!**
