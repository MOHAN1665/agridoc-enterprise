#!/usr/bin/env python3
"""
Test script for AgriDoc Enterprise System
"""

import sys
import os

def test_imports():
    """Test if all imports work"""
    print("🧪 Testing imports...")
    try:
        from src.config import Config
        print("✅ Config import successful")
        
        from src.database import OutbreakRegistry
        print("✅ Database import successful")
        
        from src.agent import PlantDoctorAgent
        print("✅ Agent import successful")
        
        import google.generativeai as genai
        print("✅ Gemini AI import successful")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_config():
    """Test configuration"""
    print("\n🧪 Testing configuration...")
    try:
        from src.config import Config
        Config.validate()
        print("✅ Configuration valid")
        print(f"   Project: {Config.PROJECT_ID}")
        print(f"   Model: {Config.MODEL_NAME}")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_database():
    """Test database connection"""
    print("\n🧪 Testing database...")
    try:
        from src.database import OutbreakRegistry
        db = OutbreakRegistry()
        stats = db.get_recent_stats()
        print("✅ Database connection successful")
        print(f"   Recent stats: {len(stats)} entries")
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 AgriDoc Enterprise System Test")
    print("=" * 40)
    
    # Add current directory to path
    sys.path.append(os.path.dirname(__file__))
    
    results = [
        test_imports(),
        test_config(), 
        test_database()
    ]
    
    if all(results):
        print("\n🎉 ALL TESTS PASSED! System is ready for deployment.")
    else:
        print("\n❌ SOME TESTS FAILED! Please check the errors above.")
        sys.exit(1)