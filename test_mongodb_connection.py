#!/usr/bin/env python
"""
Test MongoDB connection
"""
import os
from dotenv import load_dotenv

print("=" * 70)
print("🔌 Testing MongoDB Connection")
print("=" * 70)
print()

# Load environment variables
load_dotenv()

# Check if .env file exists
if not os.path.exists('.env'):
    print("❌ Error: .env file not found!")
    print()
    print("Please create a .env file in the project root with:")
    print()
    print("MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/sales_ai")
    print()
    exit(1)

# Get MongoDB URI
mongodb_uri = os.getenv('MONGODB_URI')

if not mongodb_uri:
    print("❌ Error: MONGODB_URI not found in .env file!")
    print()
    print("Please add this line to your .env file:")
    print("MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/sales_ai")
    print()
    exit(1)

print(f"✅ .env file found")
print(f"✅ MONGODB_URI loaded")
print()

# Test connection
try:
    from pymongo import MongoClient
    
    print("Connecting to MongoDB...")
    client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
    
    # Test the connection
    client.server_info()
    
    print("✅ Successfully connected to MongoDB!")
    print()
    
    # List databases
    databases = client.list_database_names()
    print(f"📊 Available databases: {databases}")
    print()
    
    # Check if sales_ai database exists
    if 'sales_ai' in databases:
        db = client['sales_ai']
        collections = db.list_collection_names()
        print(f"✅ Database 'sales_ai' found!")
        print(f"📁 Collections: {collections}")
    else:
        print("ℹ️  Database 'sales_ai' will be created when you run setup")
    
    print()
    print("=" * 70)
    print("✅ MongoDB Connection Test Successful!")
    print("=" * 70)
    print()
    print("Next step:")
    print("  python tmp_rovodev_quick_setup.py")
    print()
    
except Exception as e:
    print("❌ Connection failed!")
    print()
    print(f"Error: {e}")
    print()
    print("Common issues:")
    print("  1. Wrong username or password in connection string")
    print("  2. IP address not whitelisted in MongoDB Atlas")
    print("  3. Network connectivity issues")
    print()
    print("Please check:")
    print("  - Your .env file has the correct connection string")
    print("  - Your password doesn't have special characters")
    print("  - Network Access in MongoDB Atlas allows your IP (0.0.0.0/0)")
    print()
    exit(1)
