# 📘 How to Use the Sales AI System

## 🎯 System Overview

This system helps sales managers:
1. **Track** agent activities in real-time
2. **Calculate** performance scores automatically
3. **Predict** which agents will miss their targets
4. **Take action** before it's too late

---

## 🚀 Getting Started in 3 Minutes

### Step 1: Run the Setup Script
```bash
python setup_and_run.py
```
Choose **option 1** (Full setup)

### Step 2: Open Your Browser
Navigate to: **http://localhost:8000**

### Step 3: View the Dashboard
You'll see 6 sample agents with their:
- Performance metrics
- Risk levels
- AI predictions

**That's it! The system is ready to use.**

---

## 📊 Understanding the Dashboard

### Agent Cards

Each card shows:

#### 🔴 Risk Badge
- **HIGH RISK** (Red) - Agent likely to miss target (>70% probability)
- **MEDIUM RISK** (Yellow) - Agent may miss target (40-70% probability)  
- **LOW RISK** (Green) - Agent on track (<40% probability of missing)

#### 📈 Metrics
- **Calls** - Phone calls made this month
- **Meetings** - Client meetings held
- **Leads** - New leads generated
- **Deals** - Deals closed

#### 💰 Sales Progress Bar
Shows: Current Sales / Monthly Target
- Green bar = progress toward goal
- Percentage = achievement rate

#### 🤖 AI Prediction
- **HIT** - Agent will meet target
- **MISS** - Agent will miss target
- **Confidence** - How sure the AI is (%)

#### 📊 Overall Score
Performance score out of 100%
- Excellent: 80-100%
- Good: 60-79%
- Average: 40-59%
- Poor: 0-39%

---

## 🎯 Common Use Cases

### Use Case 1: Weekly Performance Review

**Scenario:** Every Monday, review team performance

**Steps:**
1. Open dashboard at http://localhost:8000
2. Look for RED badges (HIGH RISK agents)
3. Click on agent name for details
4. Review their metrics
5. Take action (coaching, support, resources)

**Indicators to watch:**
- Low meeting count → Agent needs help booking meetings
- Low lead count → Marketing support needed
- Low conversion (leads to deals) → Sales training needed
- Low deal count → Need to review sales pipeline

---

### Use Case 2: Identifying At-Risk Agents

**Scenario:** Find agents who need immediate help

**Steps:**
1. Dashboard automatically sorts HIGH RISK agents first
2. Review agents with:
   - Sales < 50% of target
   - Prediction: MISS
   - Risk Level: HIGH
3. Click on agent for detailed breakdown
4. Identify root cause:
   - Not enough activity? → Time management issue
   - Activity but no sales? → Skills or process issue
   - Just started poorly? → May catch up with support

---

### Use Case 3: Monthly Planning

**Scenario:** Plan next month's strategy

**Steps:**
1. Review current month performance
2. Identify patterns:
   - Which agents consistently perform well?
   - Which need ongoing support?
   - What activities correlate with success?
3. Set expectations for next month
4. Train the model with new data: http://localhost:8000/train/

---

### Use Case 4: Coaching Sessions

**Scenario:** One-on-one meeting with agent

**Steps:**
1. Open agent detail page: `/agent/<agent_id>/`
2. Review with agent:
   - Current performance vs target
   - Activity levels (calls, meetings, leads, deals)
   - AI prediction and risk level
3. Create action plan:
   - Set weekly activity goals
   - Address skill gaps
   - Provide resources
4. Follow up weekly

---

## 🤖 Training the AI Model

### When to Retrain

Retrain the model when:
- ✅ You add 1+ months of new data
- ✅ Business conditions change significantly
- ✅ Target expectations change
- ✅ You add/remove agents
- ✅ Monthly (recommended schedule)

### How to Train

**Option 1: Web Interface**
1. Go to: http://localhost:8000/train/
2. Click "Start Training"
3. Wait 10-30 seconds
4. View accuracy results

**Option 2: Command Line**
```bash
python manage.py shell
>>> from core.ai.trainer import AITrainer
>>> AITrainer.train_model()
```

### What Makes a Good Model?

**Accuracy Levels:**
- **90%+** - Excellent (rare without lots of data)
- **80-90%** - Very Good
- **70-80%** - Good
- **60-70%** - Acceptable
- **<60%** - Needs more data or tuning

**Improving Accuracy:**
1. Add more historical data (6+ months ideal)
2. Ensure data quality (accurate activity tracking)
3. Include diverse scenarios (high/medium/low performers)
4. Retrain regularly with fresh data

---

## 📝 Adding Real Data

### Method 1: Python Shell

```python
python manage.py shell

# Add an agent
from core.models import Agent
Agent.create("A107", "Jane Doe", "jane@company.com", 650000)

# Add activities
from core.models import Activity
Activity.create("ACT001", "A107", "call", 0, "Called prospect")
Activity.create("ACT002", "A107", "meeting", 0, "Demo meeting")
Activity.create("ACT003", "A107", "lead", 0, "New lead from website")
Activity.create("ACT004", "A107", "deal", 0, "Closed deal")

# Add sales
from core.models import Sale
Sale.create("S001", "A107", 50000, "ABC Corp", "Q4 deal")
```

### Method 2: Create Your Own Import Script

```python
# import_data.py
import pandas as pd
from core.models import Agent, Activity, Sale

# Read from CSV
df = pd.read_csv('your_data.csv')

for _, row in df.iterrows():
    # Import logic here
    pass
```

### Method 3: API Integration (Future Enhancement)

Create REST API endpoints to receive data from:
- CRM systems (Salesforce, HubSpot)
- Phone systems
- Calendar systems
- Email tracking

---

## 🎨 Customizing for Your Business

### Change Activity Targets

Edit `core/services/performance.py`:

```python
MONTHLY_TARGETS = {
    'calls': 150,      # Change from 100 to 150
    'meetings': 50,    # Change from 40 to 50
    'leads': 40,       # Change from 30 to 40
    'deals': 20        # Change from 15 to 20
}
```

### Change Performance Weights

Edit `core/services/performance.py`:

```python
WEIGHTS = {
    'calls': 0.10,      # Reduce call importance
    'meetings': 0.30,   # Increase meeting importance
    'leads': 0.20,
    'deals': 0.20,
    'sales': 0.20       # Keep sales at 20%
}
```

### Change Risk Thresholds

Edit `core/services/predictor.py`:

```python
def calculate_risk_level(miss_probability):
    if miss_probability >= 0.8:  # Change from 0.7
        return 'HIGH'
    elif miss_probability >= 0.5:  # Change from 0.4
        return 'MEDIUM'
    else:
        return 'LOW'
```

---

## 🔄 Daily Workflow

### Morning (5 minutes)
1. Open dashboard
2. Check for HIGH RISK agents
3. Review overnight activities
4. Plan day's coaching priorities

### During Day (As Needed)
1. Check individual agent details
2. Monitor progress on key metrics
3. Provide real-time coaching

### End of Day (5 minutes)
1. Review team progress
2. Note any concerns for tomorrow
3. Update targets if needed

### Weekly (15 minutes)
1. Deep dive on each agent
2. Schedule coaching sessions
3. Adjust strategies as needed

### Monthly (30 minutes)
1. Review full month performance
2. Retrain AI model with new data
3. Set next month's targets
4. Analyze trends and patterns

---

## 💡 Pro Tips

### Tip 1: Early Warning System
Check dashboard daily - the AI can predict issues weeks in advance!

### Tip 2: Focus on Activities First
If sales are low but activities are high, it's a skill/process issue.
If activities are low, it's a motivation/time management issue.

### Tip 3: Use Risk Levels for Prioritization
- HIGH RISK: Daily check-ins
- MEDIUM RISK: Weekly coaching
- LOW RISK: Monthly reviews

### Tip 4: Don't Ignore Success
Study HIGH performers to learn what works. Replicate their patterns.

### Tip 5: Trust the AI, But Verify
The AI is a tool, not a replacement for your judgment. Use it to guide, not dictate decisions.

### Tip 6: Regular Model Training
Set a monthly reminder to retrain the model. Fresh data = better predictions.

### Tip 7: Track Trends
Take screenshots monthly to see improvement trends over time.

---

## ❓ FAQ

**Q: How accurate is the AI?**
A: With good historical data, 75-85% accuracy is typical. More data = better accuracy.

**Q: Can I export data?**
A: Yes, use the API endpoint `/api/agents/` to get JSON data.

**Q: How much historical data do I need?**
A: Minimum 3 months, ideal 6+ months, across multiple agents and scenarios.

**Q: Does it work offline?**
A: Yes, if using local MongoDB. With Atlas, you need internet connection.

**Q: Can I customize the dashboard?**
A: Yes! Edit the HTML templates in `core/templates/`

**Q: What if an agent's prediction is wrong?**
A: The model learns from errors. Retrain with more data to improve.

**Q: Can I track multiple teams?**
A: Yes! Add a "team" field to agents and filter in dashboard.

**Q: Is my data secure?**
A: Yes, if using MongoDB Atlas with encryption and secure passwords.

---

## 🆘 Troubleshooting

### Dashboard shows no data
→ Run: `python manage.py setup_demo`

### AI predictions show "N/A"
→ Train the model at: http://localhost:8000/train/

### MongoDB connection error
→ Check your .env file has correct MONGODB_URI

### Model accuracy is low
→ Add more historical data and retrain

### Page won't load
→ Ensure server is running: `python manage.py runserver`

---

## 📞 Next Steps

1. ✅ Explore the demo system
2. ✅ Understand the metrics
3. ✅ Add your real agents
4. ✅ Train with your data
5. ✅ Start using it daily!

**The system is ready to help you prevent missed targets and drive sales success! 🎯**
