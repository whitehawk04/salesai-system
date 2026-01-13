#!/usr/bin/env python
"""
Quick setup script for Sales AI Performance System
Handles initial setup and launches the server
"""
import os
import sys
import subprocess


def print_banner():
    print("=" * 70)
    print("🎯 AI-Powered Sales Agent Performance System")
    print("=" * 70)
    print()


def check_python_version():
    """Check if Python version is adequate"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")


def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--quiet"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        print("   Try manually: pip install -r requirements.txt")
        sys.exit(1)


def check_mongodb():
    """Check MongoDB connection"""
    print("\n🔌 Checking MongoDB connection...")
    mongodb_uri = os.getenv('MONGODB_URI')
    
    if not mongodb_uri:
        print("⚠️  MongoDB URI not configured")
        print("   The system will attempt to connect to localhost:27017")
        print("   For MongoDB Atlas, set MONGODB_URI in your environment or .env file")
        return False
    
    try:
        from pymongo import MongoClient
        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
        client.server_info()
        print("✅ MongoDB connection successful")
        return True
    except Exception as e:
        print(f"⚠️  MongoDB connection issue: {e}")
        print("   The system will still work with local MongoDB if available")
        return False


def setup_demo_data():
    """Set up demo data and train model"""
    print("\n🚀 Setting up demo system...")
    try:
        # Import here to avoid issues if Django isn't set up yet
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salesAI.settings')
        import django
        django.setup()
        
        from core.utils.sample_data import create_sample_data
        from core.ai.trainer import AITrainer
        
        print("\n📊 Creating sample data...")
        create_sample_data()
        
        print("\n🤖 Training AI model...")
        model, accuracy = AITrainer.train_model()
        print(f"✅ Model trained with {accuracy * 100:.2f}% accuracy")
        
        return True
    except Exception as e:
        print(f"⚠️  Setup warning: {e}")
        print("   You can set up data manually from the web interface")
        return False


def run_server():
    """Run Django development server"""
    print("\n" + "=" * 70)
    print("🌐 Starting Django development server...")
    print("=" * 70)
    print("\n📊 Access the dashboard at: http://localhost:8000")
    print("🤖 Train the model at: http://localhost:8000/train/")
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        subprocess.call([sys.executable, "manage.py", "runserver"])
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")


def main():
    print_banner()
    
    # Check Python version
    check_python_version()
    
    # Ask user what they want to do
    print("\nWhat would you like to do?")
    print("1. Full setup (install dependencies, create demo data, train model, run server)")
    print("2. Quick start (skip setup, just run server)")
    print("3. Setup only (install dependencies and create demo data)")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        install_dependencies()
        check_mongodb()
        setup_demo_data()
        run_server()
    elif choice == "2":
        print("\n🚀 Quick start mode...")
        run_server()
    elif choice == "3":
        install_dependencies()
        check_mongodb()
        setup_demo_data()
        print("\n✅ Setup complete!")
        print("   Run 'python manage.py runserver' to start the server")
    else:
        print("❌ Invalid choice. Exiting.")


if __name__ == "__main__":
    main()
