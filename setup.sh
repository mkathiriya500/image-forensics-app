#!/bin/bash

echo "🔍 Setting up Image & Video Forensics Tool"
echo "=========================================="

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "📥 Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p temp output logs cache

# Download required models
echo "🤖 Downloading ML models..."
python -c "
import cv2
cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
print('✓ Face detection model downloaded')
"

# Set permissions
chmod +x run.sh

echo "✅ Setup complete!"
echo ""
echo "🚀 To run the application:"
echo "   source venv/bin/activate"
echo "   streamlit run app.py"
echo ""
echo "📝 Default login:"
echo "   Username: admin"
echo "   Password: admin123"