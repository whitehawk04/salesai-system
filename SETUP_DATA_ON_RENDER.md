# How to Setup Data on Render (Free Tier)

Since the free tier doesn't have Shell access, we've created web endpoints to populate the database.

## Quick Start - 3 Simple Steps

### Step 1: Check Current Data
Visit this URL in your browser:
```
https://salesai-system.onrender.com/check-data/
```

This shows what data is currently in your database.

### Step 2: Setup Database with Demo Data
Visit this URL in your browser (or use curl/Postman):
```
https://salesai-system.onrender.com/setup-database/?key=demo-setup-key-2026&clear=true
```

**Important:**
- `key=demo-setup-key-2026` - Security key (change this in production!)
- `clear=true` - Clears existing data first (recommended for first-time setup)

**Wait 1-2 minutes** while it creates:
- ✅ 2 Division Heads
- ✅ 3 Area Managers
- ✅ 6 Sales Agents
- ✅ 20 Banking Products
- ✅ 66+ Leads and Sales
- ✅ AI Model Training

### Step 3: Verify and Use
Visit your dashboard:
```
https://salesai-system.onrender.com/
```

You should now see all the data populated!

---

## Security

### Change the Setup Key (Recommended)

By default, the setup key is `demo-setup-key-2026`. For production:

1. **In Render Dashboard:**
   - Go to your service → **Environment** tab
   - Add environment variable: `SETUP_KEY` = `your-secret-key-here`
   - Use a strong random key (e.g., `sk-prod-abc123xyz789`)

2. **Then use your custom key:**
   ```
   https://salesai-system.onrender.com/setup-database/?key=your-secret-key-here&clear=true
   ```

### After Setup is Complete

**Option 1: Remove the setup endpoints** (most secure)
- Comment out the setup routes in `core/urls.py`
- Redeploy

**Option 2: Keep them but use strong key**
- Set a complex `SETUP_KEY` environment variable
- Don't share the URL publicly

---

## Endpoint Details

### `/check-data/` (Public - No Key Required)
**Method:** GET  
**Purpose:** Check how many documents are in each collection

**Example Response:**
```json
{
  "counts": {
    "division_heads": 2,
    "area_managers": 3,
    "agents": 6,
    "activities": 742,
    "sales": 66,
    "products": 20,
    "leads": 66
  },
  "total_documents": 905,
  "has_data": true,
  "message": "Database has data"
}
```

### `/setup-database/` (Protected - Requires Key)
**Method:** GET or POST  
**Purpose:** Populate database with demo data

**Parameters:**
- `key` (required) - Security key (default: `demo-setup-key-2026`)
- `clear` (optional) - Set to `true` to clear existing data first

**Examples:**

1. **First time setup (recommended):**
   ```
   GET https://salesai-system.onrender.com/setup-database/?key=demo-setup-key-2026&clear=true
   ```

2. **Add data without clearing:**
   ```
   GET https://salesai-system.onrender.com/setup-database/?key=demo-setup-key-2026
   ```

**Example Response:**
```json
{
  "success": true,
  "steps": [
    {
      "step": 1,
      "name": "Create organizational hierarchy and agents",
      "status": "completed",
      "counts": {
        "division_heads": 2,
        "area_managers": 3,
        "agents": 6
      }
    },
    ...
  ],
  "summary": {
    "division_heads": 2,
    "area_managers": 3,
    "agents": 6,
    "activities": 742,
    "sales": 66,
    "products": 20,
    "leads": 66
  },
  "message": "Database setup completed successfully!"
}
```

---

## Using with curl (Command Line)

### Check data:
```bash
curl https://salesai-system.onrender.com/check-data/
```

### Setup database:
```bash
curl -X POST "https://salesai-system.onrender.com/setup-database/?key=demo-setup-key-2026&clear=true"
```

---

## Troubleshooting

### "Invalid or missing setup key"
**Problem:** The key parameter is missing or incorrect.  
**Solution:** Make sure you include `?key=demo-setup-key-2026` in the URL.

### "duplicate key error"
**Problem:** Data already exists in the database.  
**Solution:** Add `&clear=true` to the URL to clear existing data first.

### "Model training failed"
**Problem:** Not enough data or training error.  
**Solution:** 
- Check that data was created successfully in the response
- Visit `/train/` to manually train the model
- Check Render logs for detailed error messages

### Timeout or slow response
**Problem:** Setup takes longer than expected.  
**Solution:** 
- Be patient, first-time setup can take 1-2 minutes
- Render free tier may be slower
- Check `/check-data/` to see if data is being created

---

## What Data Gets Created

See full details in **RENDER_DATA_SETUP.md**

**Summary:**
- **Organizational Hierarchy:** 2 Divisions → 3 Regions → 6 Agents
- **Products:** 20 banking products (Loans, Credit Cards, Insurance, etc.)
- **Activity Data:** Realistic call logs, meetings, presentations
- **Sales Pipeline:** Leads in various stages (Qualified, Proposal, Won, Lost)
- **Performance Metrics:** Monthly targets and achievements

---

## Next Steps After Setup

1. **Explore the Dashboard**
   - View overall metrics and sales funnel
   - Check agent performance rankings

2. **Navigate Hierarchy**
   - Division Head dashboards
   - Area Manager views
   - Individual agent details

3. **Train AI Model** (if needed)
   - Visit: `/train/`
   - Model learns from populated data

4. **Customize**
   - Add more agents via Django admin
   - Adjust products and targets
   - Import real data if available

---

## Local Development

For local testing:
```bash
# Check data
curl http://localhost:8000/check-data/

# Setup data locally
curl -X POST "http://localhost:8000/setup-database/?key=demo-setup-key-2026&clear=true"

# Or use Django command
python manage.py setup_demo --clear
```
