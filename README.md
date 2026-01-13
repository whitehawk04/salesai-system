# AI-Powered Sales Agent Performance System

A complete sales performance tracking and AI prediction system to help managers identify at-risk agents before they miss their targets.

## Features
- Track sales agents and their activities (calls, meetings, leads, sales)
- Calculate performance scores in real-time
- AI-powered predictions to identify agents at risk of missing targets
- Dashboard for easy monitoring

## Tech Stack
- Python 3.8+
- Django 4.2
- MongoDB Atlas (Free tier)
- Scikit-learn
- Pandas

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure MongoDB
Create a free MongoDB Atlas account at https://www.mongodb.com/cloud/atlas
- Create a cluster
- Create a database named `sales_ai`
- Get your connection string

### 3. Configure Environment Variables
Copy `.env.example` to `.env` and update with your MongoDB connection string:
```
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/sales_ai?retryWrites=true&w=majority
```

### 4. Run Django Server
```bash
cd salesAI
python manage.py runserver
```

### 5. Access the Dashboard
Open your browser and navigate to: http://localhost:8000

## Database Structure

### Collections

#### agents
```json
{
  "_id": "A101",
  "name": "Maria Santos",
  "email": "maria@company.com",
  "monthly_target": 600000,
  "created_at": "2024-01-01"
}
```

#### activities
```json
{
  "_id": "ACT001",
  "agent_id": "A101",
  "type": "call|meeting|lead|deal",
  "value": 0,
  "date": "2024-01-15",
  "notes": "Follow-up call"
}
```

#### sales
```json
{
  "_id": "S001",
  "agent_id": "A101",
  "amount": 50000,
  "date": "2024-01-20",
  "customer": "ABC Corp"
}
```

## Performance Formula
The system calculates performance based on:
- Number of calls made
- Number of meetings held
- Number of leads generated
- Number of deals closed
- Sales amount vs target

## AI Prediction
Uses RandomForestClassifier to predict:
- **HIT**: Agent likely to meet target
- **MISS**: Agent at risk of missing target

## Usage

### Add Sample Data
```bash
python manage.py shell
from core.utils.sample_data import create_sample_data
create_sample_data()
```

### Train AI Model
```bash
python manage.py shell
from core.ai.trainer import train_model
train_model()
```

### View Dashboard
Navigate to http://localhost:8000 to see all agents and their risk status.

## Project Structure
```
salesAI/
├── manage.py
├── salesAI/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── core/
    ├── models/
    ├── ai/
    ├── views.py
    ├── urls.py
    └── templates/
```

## License
MIT
