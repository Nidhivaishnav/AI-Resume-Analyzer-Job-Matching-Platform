#!/bin/bash

# Setup script for AI Resume Analyzer

echo "🚀 Setting up AI Resume Analyzer & Job Matching Platform..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Download spaCy model
echo "🔤 Downloading spaCy English model..."
python -m spacy download en_core_web_sm

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p uploads

# Copy environment file
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your OpenAI API key"
fi

echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Start API server: uvicorn app.main:app --reload"
echo "  3. Start dashboard (in new terminal): streamlit run app/dashboard.py"
echo ""
echo "Or use Docker:"
echo "  docker-compose up --build"
