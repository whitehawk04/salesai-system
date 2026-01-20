# Render Environment Variables - Exact Names

## Add These 4 Environment Variables

In Render dashboard, scroll to **"Environment Variables"** section.

Click **"Add Environment Variable"** button 4 times to add each variable:

---

## Variable 1: SECRET_KEY

**Key** (exact name):
```
SECRET_KEY
```

**Value**: 
1. Open this URL: https://djecrety.ir/
2. Copy the generated key (looks like: `django-insecure-abc123xyz...`)
3. Paste as the value

**Example**:
```
Key: SECRET_KEY
Value: django-insecure-7k$m2@n8p!q3r4s5t6u7v8w9x0y1z2a3b4c5d6e7f8g9h0
```

---

## Variable 2: DEBUG

**Key** (exact name):
```
DEBUG
```

**Value** (exactly as shown):
```
False
```

**Example**:
```
Key: DEBUG
Value: False
```

**⚠️ Important**: Use capital `F` in `False`

---

## Variable 3: MONGODB_URI

**Key** (exact name):
```
MONGODB_URI
```

**Value** (for now, use this placeholder):
```
mongodb://localhost:27017/
```

**Example**:
```
Key: MONGODB_URI
Value: mongodb://localhost:27017/
```

**Note**: We'll update this value later with your MongoDB Atlas connection string

---

## Variable 4: PYTHON_VERSION

**Key** (exact name):
```
PYTHON_VERSION
```

**Value** (exactly as shown):
```
3.11.0
```

**Example**:
```
Key: PYTHON_VERSION
Value: 3.11.0
```

---

## Quick Copy-Paste Reference

For easy copying:

### Variable Names (Keys):
```
SECRET_KEY
DEBUG
MONGODB_URI
PYTHON_VERSION
```

### Variable Values:
```
SECRET_KEY = [generate at https://djecrety.ir/]
DEBUG = False
MONGODB_URI = mongodb://localhost:27017/
PYTHON_VERSION = 3.11.0
```

---

## Screenshot Guide

Your Render environment variables section should look like this:

```
Environment Variables (4)

SECRET_KEY          •••••••••••••••••••••         [Edit] [Delete]
DEBUG               False                          [Edit] [Delete]
MONGODB_URI         mongodb://localhost:27017/     [Edit] [Delete]
PYTHON_VERSION      3.11.0                         [Edit] [Delete]

[+ Add Environment Variable]
```

---

## Step-by-Step Adding Each Variable

### Adding Variable 1 (SECRET_KEY):
1. Click **"Add Environment Variable"**
2. In "Key" field, type: `SECRET_KEY`
3. In "Value" field, paste your generated key from djecrety.ir
4. ✅ Variable added!

### Adding Variable 2 (DEBUG):
1. Click **"Add Environment Variable"** again
2. In "Key" field, type: `DEBUG`
3. In "Value" field, type: `False`
4. ✅ Variable added!

### Adding Variable 3 (MONGODB_URI):
1. Click **"Add Environment Variable"** again
2. In "Key" field, type: `MONGODB_URI`
3. In "Value" field, type: `mongodb://localhost:27017/`
4. ✅ Variable added!

### Adding Variable 4 (PYTHON_VERSION):
1. Click **"Add Environment Variable"** again
2. In "Key" field, type: `PYTHON_VERSION`
3. In "Value" field, type: `3.11.0`
4. ✅ Variable added!

---

## Common Mistakes to Avoid

❌ **Wrong**: `secret_key` (lowercase)  
✅ **Correct**: `SECRET_KEY` (uppercase)

❌ **Wrong**: `debug` or `Debug`  
✅ **Correct**: `DEBUG` (all uppercase)

❌ **Wrong**: `MongoDB_URI` or `mongodb_uri`  
✅ **Correct**: `MONGODB_URI` (all uppercase)

❌ **Wrong**: `debug = false` (value must be `False` with capital F)  
✅ **Correct**: `False`

❌ **Wrong**: `3.11` or `3.11.0.0`  
✅ **Correct**: `3.11.0`

---

## After Adding All 4 Variables

✅ You should see all 4 variables listed  
✅ Total count should show: "Environment Variables (4)"  
✅ Ready to click "Create Web Service"

---

## Need to Edit Later?

To update MONGODB_URI after setting up MongoDB Atlas:
1. Go to your service in Render dashboard
2. Click "Environment" tab
3. Find `MONGODB_URI`
4. Click "Edit"
5. Paste your MongoDB Atlas connection string
6. Service will automatically redeploy

---

## Troubleshooting

### "Service won't start"
- Check that `SECRET_KEY` is set (not empty)
- Verify `DEBUG` = `False` (capital F)
- Check spelling of all variable names

### "Can't connect to database"
- `MONGODB_URI` will be updated in next step
- For now, placeholder value is fine

---

**Ready to add your environment variables?** Follow the exact names and values above! 🚀
