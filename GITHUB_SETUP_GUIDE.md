# 📦 Step 2: Push Your Code to GitHub

## What is GitHub?
GitHub is like Google Drive for code. It stores your project and lets Render.com automatically deploy it.

---

## Part A: Create GitHub Account (if you don't have one)

1. Go to: https://github.com
2. Click **"Sign up"** (top right)
3. Enter your email address
4. Create a password
5. Choose a username (e.g., yourname-dev)
6. Verify you're human
7. Check your email and verify

**Done!** You now have a GitHub account.

---

## Part B: Create Repository on GitHub

1. **Log in** to GitHub
2. Click the **"+"** icon (top right corner)
3. Select **"New repository"**

**Fill in these details:**

- **Repository name**: `salesai-system`
- **Description** (optional): `AI-powered Sales Performance System`
- **Visibility**: 
  - Choose **Public** (required for free Render.com)
- **Do NOT check any boxes below:**
  - ❌ Don't add README
  - ❌ Don't add .gitignore
  - ❌ Don't choose a license

4. Click **"Create repository"**

**You'll see a page with setup instructions - keep this page open!**

---

## Part C: Install Git (if needed)

### Check if Git is installed:
Open your terminal/command prompt and type:
```bash
git --version
```

**If you see a version number** (like `git version 2.40.0`):
✅ Git is installed - skip to Part D

**If you see "command not found" or error:**
❌ Need to install Git:

### Windows:
1. Download: https://git-scm.com/download/win
2. Run installer
3. Use default settings (just click Next)
4. Restart your terminal/command prompt

### Mac:
```bash
# Install using Homebrew (if you have it)
brew install git

# OR install Xcode Command Line Tools
xcode-select --install
```

### Linux:
```bash
# Ubuntu/Debian
sudo apt-get install git

# Fedora
sudo dnf install git
```

**Verify installation:**
```bash
git --version
```

---

## Part D: Configure Git (First Time Only)

If this is your first time using Git, set your identity:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

**Example:**
```bash
git config --global user.name "Juan Dela Cruz"
git config --global user.email "juan@example.com"
```

Use the SAME email you used for GitHub!

---

## Part E: Push Your Code to GitHub

### Step 1: Open Terminal in Your Project Folder

**Windows:**
1. Open File Explorer
2. Navigate to your `salesAI` project folder
3. Click in the address bar, type `cmd`, press Enter
4. OR right-click → "Open in Terminal" (Windows 11)

**Mac/Linux:**
1. Open Terminal
2. Navigate to your project:
   ```bash
   cd /path/to/your/salesai-project
   ```

**Verify you're in the right folder:**
```bash
# Windows
dir

# Mac/Linux
ls
```

You should see: `manage.py`, `requirements.txt`, `core/`, `salesAI/`, etc.

---

### Step 2: Initialize Git Repository

```bash
git init
```

**Expected output:**
```
Initialized empty Git repository in ...
```

---

### Step 3: Add All Files

```bash
git add .
```

**The dot (`.`) means "add all files"**

**Check what was added:**
```bash
git status
```

You should see a list of files in green.

---

### Step 4: Commit Your Code

```bash
git commit -m "Initial commit - SalesAI ready for deployment"
```

**Expected output:**
```
[main ...] Initial commit - SalesAI ready for deployment
XX files changed, XXXX insertions(+)
```

---

### Step 5: Connect to GitHub

Go back to your GitHub repository page (the one you kept open).

You'll see a section that says **"…or push an existing repository from the command line"**

Copy the commands shown, which look like:

```bash
git remote add origin https://github.com/YOUR_USERNAME/salesai-system.git
git branch -M main
git push -u origin main
```

**Paste and run those commands in your terminal.**

**Example (replace with YOUR username):**
```bash
# Add remote repository
git remote add origin https://github.com/juandelacruz/salesai-system.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

---

### Step 6: Authenticate with GitHub

When you run `git push`, GitHub will ask for authentication.

**You have 2 options:**

#### Option A: Personal Access Token (Recommended)

1. **GitHub will open a browser window**
2. Log in if needed
3. Click **"Authorize GitCredentialManager"**
4. Done! Your code will upload

#### Option B: Manual Token (if browser doesn't open)

1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token (classic)"**
3. Name: `SalesAI Deployment`
4. Expiration: **No expiration**
5. Check: ✅ `repo` (full control of private repositories)
6. Click **"Generate token"**
7. **COPY THE TOKEN** (you won't see it again!)
8. When terminal asks for password, **paste the token** (not your GitHub password!)

---

### Step 7: Verify Upload

**Wait for upload to complete. You should see:**
```
Enumerating objects: XXX, done.
Counting objects: 100% (XXX/XXX), done.
Writing objects: 100% (XXX/XXX), done.
Total XXX (delta XX), reused XX (delta XX)
To https://github.com/YOUR_USERNAME/salesai-system.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

**✅ SUCCESS!**

---

## Part F: Verify on GitHub

1. Go to: `https://github.com/YOUR_USERNAME/salesai-system`
2. Refresh the page
3. You should see all your files:
   - ✅ `manage.py`
   - ✅ `requirements.txt`
   - ✅ `core/` folder
   - ✅ `salesAI/` folder
   - ✅ All your project files

**🎉 YOUR CODE IS NOW ON GITHUB!**

---

## 🐛 Troubleshooting

### Problem: "Permission denied (publickey)"
**Solution**: Use HTTPS instead of SSH
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/salesai-system.git
```

### Problem: "fatal: not a git repository"
**Solution**: Make sure you're in the project folder and ran `git init`

### Problem: "Everything up-to-date" but nothing uploaded
**Solution**: 
```bash
git add .
git commit -m "Add all files"
git push origin main
```

### Problem: "Authentication failed"
**Solution**: Use Personal Access Token instead of password (see Step 6, Option B)

### Problem: Files not showing on GitHub
**Solution**: 
1. Check `.gitignore` - it might be excluding files
2. Verify files were committed: `git status`
3. Push again: `git push origin main`

---

## ✅ Checklist

- ⬜ GitHub account created
- ⬜ Repository created on GitHub (salesai-system)
- ⬜ Git installed on computer
- ⬜ Git configured (name & email)
- ⬜ Navigated to project folder in terminal
- ⬜ Ran `git init`
- ⬜ Ran `git add .`
- ⬜ Ran `git commit -m "message"`
- ⬜ Added remote origin
- ⬜ Pushed to GitHub
- ⬜ Verified files on GitHub website

---

## 🎯 What's Next?

Now that your code is on GitHub, you can:

**✅ Proceed to Step 3**: Deploy to Render.com
- Open `RENDER_DEPLOYMENT_QUICK_START.md`
- Jump to **STEP 3: Deploy to Render.com**

---

## 💡 Pro Tips

1. **Keep your repository public** (required for free Render.com)
2. **Never commit `.env` file** (it's in .gitignore already)
3. **Future updates are easy**: Just run:
   ```bash
   git add .
   git commit -m "Your changes"
   git push origin main
   ```
4. **Render auto-deploys** when you push to GitHub!

---

## 🎉 Congratulations!

Your code is now safely stored on GitHub and ready for deployment to Render.com!

**Continue to Step 3** in the main deployment guide.
