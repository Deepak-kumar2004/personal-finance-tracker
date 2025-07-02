#!/bin/bash

# Money Manager Setup Script

echo "🚀 Setting up Money Manager Application..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv .venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs
mkdir -p user_data

# Copy environment file
if [ ! -f .env ]; then
    echo "⚙️  Creating environment configuration..."
    cp .env.example .env
    echo "📝 Please edit .env file to configure your application"
fi

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "To start the application:"
echo "1. Activate the virtual environment: source .venv/bin/activate"
echo "2. Run the application: python app.py"
echo "3. Open your browser to: http://localhost:5000"
echo ""
echo "📖 For more information, see README.md"
