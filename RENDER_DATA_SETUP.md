# How to Populate Data on Render

## Quick Setup

Once your application is deployed on Render, you need to populate the database with demo data.

### Step 1: Access Render Shell

1. Go to your Render Dashboard: https://dashboard.render.com
2. Click on your `salesai-system` service
3. Click on the **Shell** tab (top right)
4. This opens a terminal connected to your production server

### Step 2: Run the Setup Command

In the Render Shell, run:

```bash
python manage.py setup_demo --clear
```

This will:
- ✅ Clear any existing data
- ✅ Create 2 Division Heads
- ✅ Create 3 Area Managers
- ✅ Create 6 Sales Agents with performance data
- ✅ Create 20 Banking Products (Loans, Credit Cards, Insurance, etc.)
- ✅ Create 66 Leads and Sales records
- ✅ Train the AI model

**Time:** Takes about 1-2 minutes to complete.

### Step 3: Verify Data

After the command completes:
1. Visit your live site: https://salesai-system.onrender.com/
2. You should see the dashboard populated with data
3. Navigate through different sections to explore

---

## Command Options

### First Time Setup (Recommended)
```bash
python manage.py setup_demo --clear
```
Clears existing data and creates fresh demo data.

### Add Data Without Clearing
```bash
python manage.py setup_demo
```
Only use this if you want to keep existing data. May cause errors if data already exists.

---

## What Data Gets Created

### Organizational Hierarchy

**North Division** (John Smith - Division Head)
- **North Region A** (Michael Brown - Area Manager)
  - Sarah Johnson (Agent) - High Performer
  - Mike Wilson (Agent) - Average Performer
- **North Region B** (Jennifer Davis - Area Manager)
  - James Taylor (Agent) - Average Performer
  - Emma Garcia (Agent) - Low Performer

**South Division** (Maria Garcia - Division Head)
- **South Region A** (Robert Lee - Area Manager)
  - Maria Santos (Agent) - High Performer
  - Juan Dela Cruz (Agent) - Average Performer

### Banking Products (20 Products)

**Loans** (5 products)
- Personal Loan, Auto Loan, Home Loan, Business Loan, Salary Loan

**Credit Cards** (4 products)
- Classic Credit Card, Gold Credit Card, Platinum Credit Card, Cashback Credit Card

**Insurance** (4 products)
- Life Insurance, Health Insurance, Car Insurance, Travel Insurance

**Investments** (4 products)
- Time Deposit, Mutual Funds, VUL Insurance, Treasury Bills

**Accounts** (3 products)
- Savings Account, Payroll Account, Business Account

### Sales & Activity Data

- **742 Activities** - Calls, meetings, presentations
- **66 Sales** - Product sales with commissions
- **66 Leads** - Various stages (Qualified, Proposal, Negotiation, Won, Lost)

---

## Troubleshooting

### "duplicate key error"
**Problem:** Data already exists in the database.
**Solution:** Use `python manage.py setup_demo --clear` to reset.

### "MongoDB connection failed"
**Problem:** MONGODB_URI not configured correctly.
**Solution:** Check environment variables in Render dashboard.

### "Command not found"
**Problem:** Using wrong directory.
**Solution:** Make sure you're in the project root directory.

### "Module not found"
**Problem:** Dependencies not installed.
**Solution:** Trigger a redeploy in Render to reinstall dependencies.

---

## Local Development

To populate data locally:

```bash
# Clear and create fresh data
python manage.py setup_demo --clear

# Start development server
python manage.py runserver

# Visit: http://localhost:8000
```

---

## Next Steps After Data Setup

1. **Explore the Dashboard**
   - View overall metrics
   - Check sales funnel
   - Review agent performance

2. **Test Different Views**
   - Division Head dashboard
   - Area Manager dashboard
   - Agent detail pages

3. **Train/Retrain AI Model**
   - Visit: https://salesai-system.onrender.com/train/
   - Model learns from the populated data

4. **Add More Data**
   - Use the admin interface or API
   - Customize products and agents as needed

---

## Data Reset

If you need to start over:

```bash
python manage.py setup_demo --clear
```

This is safe to run multiple times. It will completely reset the database.
