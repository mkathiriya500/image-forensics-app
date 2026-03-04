#!/usr/bin/env python3
"""
Installation script for Image & Video Forensics Tool
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check Python version"""
    required_version = (3, 7)
    current_version = sys.version_info[:2]
    
    if current_version < required_version:
        print(f"❌ Python {required_version[0]}.{required_version[1]}+ required")
        print(f"   Current version: {current_version[0]}.{current_version[1]}")
        return False
    
    print(f"✅ Python version: {current_version[0]}.{current_version[1]}")
    return True

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing requirements...")
    
    requirements = [
        "streamlit>=1.28.0",
        "Pillow>=9.5.0",
        "opencv-python>=4.8.0",
        "exifread>=3.0.0",
        "selenium>=4.15.0",
        "beautifulsoup4>=4.12.0",
        "folium>=0.14.0",
        "geopy>=2.4.0",
        "requests>=2.28.0",
        "numpy>=1.24.0",
        "python-dotenv>=1.0.0",
        "streamlit-folium>=0.15.0"
    ]
    
    for req in requirements:
        print(f"   Installing {req}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", req.split('>=')[0]])
        except:
            print(f"   ⚠️  Failed to install {req}")
    
    print("✅ Requirements installed")

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    dirs = ['temp', 'output', 'logs', 'cache']
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)
        print(f"   Created {dir_name}/")
    
    print("✅ Directories created")

def create_env_file():
    """Create .env file template"""
    print("\n🔑 Creating .env file template...")
    
    env_template = """# API Keys
PIMEYES_API_KEY=your_key_here
CARNET_API_KEY=your_key_here
TWITTER_API_KEY=your_key_here
FACEBOOK_API_KEY=your_key_here

# Application Settings
DEBUG=False
MAX_FILE_SIZE=200
TEMP_DIR=./temp
OUTPUT_DIR=./output
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(env_template)
        print("   Created .env file")
    else:
        print("   .env file already exists")
    
    print("✅ Environment file ready")

def main():
    """Main installation function"""
    print("=" * 50)
    print("🔍 Image & Video Forensics Tool - Installation")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install requirements
    install_requirements()
    
    # Create directories
    create_directories()
    
    # Create env file
    create_env_file()
    
    print("\n" + "=" * 50)
    print("✅ Installation complete!")
    print("=" * 50)
    print("\n🚀 To run the application:")
    print("   1. Add your API keys to .env file")
    print("   2. Run: streamlit run app.py")
    print("\n📖 For more information, check the README.md file")

if __name__ == "__main__":
    main()