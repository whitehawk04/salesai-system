# 🚀 Quick Start Guide

## Prerequisites
- Python 3.8 or higher
- MongoDB Atlas account (free tier) OR local MongoDB installation

## Option 1: Automated Setup (Recommended)

Run the automated setup script:

```bash
python setup_and_run.py
```

Choose option 1 for full setup. This will:
1. Install all dependencies
2. Create sample data
3. Train the AI model
4. Start the Django server

Then open your browser to: **http://localhost:8000**

## Option 2: Manual Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure MongoDB

**Using MongoDB Atlas (Recommended):**
1. Create a free account at https://www.mongodb.com/cloud/atlas
2. Create a cluster and database named `sales_ai`
3. Get your connection string
4. Create a `.env` file:
```
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/sales_ai?retryWrites=true&w=majority
SECRET_KEY=your-secret-key-here
DEBUG=True
```

**Using Local MongoDB:**
- Just ensure MongoDB is running on localhost:27017
- No .env configuration needed

### Step 3: Create Sample Data
```bash
python manage.py setup_demo
```

Or from Python shell:
```bash
python manage.py shell
>>> from core.utils.sample_data import create_sample_data
>>> create_sample_data()
```

### Step 4: Train the AI Model

Option A - Via Web Interface:
1. Start the server: `python manage.py runserver`
2. Navigate to: http://localhost:8000/train/
3. Click "Start Training"

Option B - Via Command Line:
```bash
python manage.py shell
>>> from core.ai.trainer import AITrainer
>>> AITrainer.train_model()
```

### Step 5: Run the Server
```bash
python manage.py runserver
```

Access the dashboard at: **http://localhost:8000**

## 📊 Features

### Dashboard (/)
- View all sales agents
- See performance metrics
- AI predictions for each agent
- Risk level indicators (HIGH/MEDIUM/LOW)

### Agent Details (/agent/<agent_id>/)
- Detailed performance breakdown
- Activity metrics (calls, meetings, leads, deals)
- Sales progress
- AI prediction with confidence scores

### Train Model (/train/)
- Train or retrain the AI model
- View model accuracy
- Uses RandomForest classifier

## 🎯 Understanding the System

### Performance Calculation
The system calculates performance based on:
- **Calls** (15% weight): Target 100/month
- **Meetings** (25% weight): Target 40/month
- **Leads** (20% weight): Target 30/month
- **Deals** (20% weight): Target 15/month
- **Sales Achievement** (20% weight): Actual vs Target

### AI Prediction
The AI model predicts:
- **HIT**: Agent likely to meet/exceed target
- **MISS**: Agent at risk of missing target

Risk Levels:
- **HIGH**: >70% probability of missing target
- **MEDIUM**: 40-70% probability of missing target
- **LOW**: <40% probability of missing target

## 📝 Sample Data

The system includes 6 sample agents:
- 2 high performers (85-110% of target)
- 2 medium performers (60-85% of target)
- 2 low performers (30-60% of target)

## 🔧 Troubleshooting

### MongoDB Connection Issues
```
Error: ServerSelectionTimeoutError
```
**Solution:** Check your MongoDB URI in .env file or ensure local MongoDB is running

### Module Not Found
```
ModuleNotFoundError: No module named 'django'
```
**Solution:** Install dependencies: `pip install -r requirements.txt`

### Model Not Found
```
FileNotFoundError: Model not found
```
**Solution:** Train the model first at /train/ or run `python manage.py setup_demo`

## 📚 API Endpoints

- `GET /` - Dashboard
- `GET /agent/<agent_id>/` - Agent detail
- `GET /train/` - Training page
- `POST /train/` - Train model (returns JSON)
- `GET /api/agents/` - Get all agents data (JSON)

## 🎨 Customization

### Modify Performance Weights
Edit `core/services/performance.py`:
```python
WEIGHTS = {
    'calls': 0.15,
    'meetings': 0.25,
    'leads': 0.20,
    'deals': 0.20,
    'sales': 0.20
}
```

### Modify Activity Targets
Edit `core/services/performance.py`:
```python
MONTHLY_TARGETS = {
    'calls': 100,
    'meetings': 40,
    'leads': 30,
    'deals': 15
}
```

### Modify AI Model Parameters
Edit `core/ai/trainer.py`:
```python
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42
)
```

## 🚀 Next Steps

1. **Add Real Data**: Replace sample data with actual sales data
2. **Customize Metrics**: Adjust weights and targets for your business
3. **Train with History**: Use 6+ months of historical data for better predictions
4. **Deploy**: Use production settings and secure your MongoDB connection
5. **Extend Features**: Add email alerts, export reports, historical trends

## 📞 Support

For issues or questions:
1. Check the main README.md
2. Review the code comments
3. Verify MongoDB connection
4. Ensure all dependencies are installed

---

**Happy Tracking! 🎯**
