#!/usr/bin/env python
"""
Debug MongoDB connection issues
"""
import os
from dotenv import load_dotenv

print("=" * 70)
print("🔍 MongoDB Connection Debug")
print("=" * 70)
print()

# Load environment variables
load_dotenv()

# Check if .env file exists
print("1. Checking .env file...")
if os.path.exists('.env'):
    print("   ✅ .env file exists")
    with open('.env', 'r') as f:
        content = f.read()
        print(f"   File size: {len(content)} bytes")
        if 'MONGODB_URI' in content:
            print("   ✅ MONGODB_URI found in file")
        else:
            print("   ❌ MONGODB_URI not found in file")
else:
    print("   ❌ .env file not found!")
    exit(1)

print()

# Get MongoDB URI
print("2. Reading MONGODB_URI...")
mongodb_uri = os.getenv('MONGODB_URI')

if not mongodb_uri:
    print("   ❌ MONGODB_URI is empty or not loaded")
    exit(1)

print("   ✅ MONGODB_URI loaded")
print()

# Display connection string (hiding password)
print("3. Connection string format:")
if mongodb_uri.startswith('mongodb+srv://'):
    parts = mongodb_uri.split('@')
    if len(parts) >= 2:
        user_part = parts[0].split('://')[1]
        if ':' in user_part:
            username = user_part.split(':')[0]
            print(f"   Protocol: mongodb+srv://")
            print(f"   Username: {username}")
            print(f"   Password: {'*' * 10} (hidden)")
            print(f"   Host: {parts[1].split('/')[0]}")
            print(f"   Database: {parts[1].split('/')[1].split('?')[0] if '/' in parts[1] else 'NOT SPECIFIED'}")
        else:
            print("   ❌ Invalid format: No password separator (:)")
    else:
        print("   ❌ Invalid format: No @ separator")
else:
    print("   ❌ Should start with: mongodb+srv://")
    print(f"   Actually starts with: {mongodb_uri[:20]}...")

print()

# Check for common issues
print("4. Checking for common issues...")
issues_found = []

# Check for spaces
if ' ' in mongodb_uri:
    issues_found.append("⚠️  Connection string contains spaces")

# Check for newlines
if '\n' in mongodb_uri or '\r' in mongodb_uri:
    issues_found.append("⚠️  Connection string contains newline characters")

# Check for database name
if '/sales_ai?' not in mongodb_uri and '/sales_ai&' not in mongodb_uri:
    if '?' in mongodb_uri:
        issues_found.append("⚠️  Missing /sales_ai before the ?")

# Check for encoded password
if '%' in mongodb_uri and '@' in mongodb_uri:
    password_part = mongodb_uri.split('://')[1].split('@')[0].split(':')[1]
    if '%' in password_part:
        issues_found.append("✅ Password appears to be URL-encoded (good)")

if not issues_found:
    print("   ✅ No obvious formatting issues found")
else:
    for issue in issues_found:
        print(f"   {issue}")

print()

# Try to connect
print("5. Attempting connection...")
try:
    from pymongo import MongoClient
    
    client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
    client.server_info()
    
    print("   ✅ CONNECTION SUCCESSFUL!")
    print()
    print("   Databases:", client.list_database_names())
    
except Exception as e:
    print(f"   ❌ CONNECTION FAILED!")
    print()
    print(f"   Error type: {type(e).__name__}")
    print(f"   Error message: {str(e)}")
    print()
    print("   Common causes:")
    print("   • Wrong password in connection string")
    print("   • Special characters in password not URL-encoded")
    print("   • IP address not whitelisted (use 0.0.0.0/0)")
    print("   • Network/firewall blocking connection")
    print("   • Cluster is paused or deleted")
    print()
    
    # Provide specific guidance based on error
    error_msg = str(e).lower()
    if 'authentication failed' in error_msg or 'auth' in error_msg:
        print("   💡 This is an AUTHENTICATION error")
        print("      → Check your username and password are correct")
        print("      → Try resetting the password in MongoDB Atlas")
    elif 'timeout' in error_msg or 'selection' in error_msg:
        print("   💡 This is a CONNECTION TIMEOUT error")
        print("      → Check Network Access in MongoDB Atlas")
        print("      → Make sure 0.0.0.0/0 is in the IP whitelist")
    elif 'ssl' in error_msg or 'certificate' in error_msg:
        print("   💡 This is an SSL/TLS error")
        print("      → Add &tlsAllowInvalidCertificates=true to connection string")

print()
print("=" * 70)
