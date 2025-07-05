#!/bin/bash

# Personal Finance Tracker Setup Script
# This script sets up the development environment

set -e  # Exit on any error

echo "🚀 Setting up Personal Finance Tracker..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check Python version
print_status "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
min_version="3.8"

if [ "$(printf '%s\n' "$min_version" "$python_version" | sort -V | head -n1)" = "$min_version" ]; then
    print_success "Python $python_version found (>= $min_version required)"
else
    print_error "Python $min_version or higher is required. Found: $python_version"
    exit 1
fi

# Check if virtual environment already exists
if [ -d ".venv" ]; then
    print_warning "Virtual environment already exists"
    read -p "Do you want to recreate it? (y/N): " recreate
    if [[ $recreate =~ ^[Yy]$ ]]; then
        print_status "Removing existing virtual environment..."
        rm -rf .venv
    else
        print_status "Using existing virtual environment"
    fi
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv .venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
print_status "Installing dependencies..."
pip install -r requirements.txt

# Ask about development dependencies
echo
read -p "Install development dependencies (linting, formatting, etc.)? (y/N): " install_dev
if [[ $install_dev =~ ^[Yy]$ ]]; then
    print_status "Installing development dependencies..."
    pip install -r requirements-dev.txt
    pip install -e .[dev]
    
    # Install pre-commit hooks
    print_status "Installing pre-commit hooks..."
    pre-commit install || print_warning "Pre-commit installation failed - install manually with 'make pre-commit-install'"
    
    print_success "Development environment set up"
else
    print_status "Skipping development dependencies"
fi

# Create environment file if it doesn't exist
if [ ! -f ".env" ]; then
    print_status "Creating .env file from template..."
    cp .env.example .env
    print_success ".env file created"
    print_warning "Please edit .env file with your configuration"
else
    print_status ".env file already exists"
fi

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p user_data logs
print_success "Directories created"

# Run a quick test
print_status "Testing installation..."
if python -c "import flask; print('Flask import successful')"; then
    print_success "Installation test passed"
else
    print_error "Installation test failed"
    exit 1
fi

echo
print_success "🎉 Setup completed successfully!"
echo
echo "To start the application:"
echo "  1. Activate the virtual environment: source .venv/bin/activate"
echo "  2. Run the application: python run.py"
echo "  3. Open your browser to: http://localhost:5000"
echo
echo "For development:"
echo "  - Install dev dependencies: pip install -r requirements-dev.txt"
echo "  - Install pre-commit hooks: make pre-commit-install"
echo "  - Run all checks: make all-checks"
echo "  - Format code: make format"
echo "  - Run tests: pytest (when implemented)"
echo
echo "📚 Documentation:"
echo "  - README.md - General information and API"
echo "  - ARCHITECTURE.md - Detailed architecture"
echo "  - CONTRIBUTING.md - Contribution guidelines"
