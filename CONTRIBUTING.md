# Contributing to Money Manager

Thank you for your interest in contributing to Money Manager! 

## 🚀 Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/money-manager.git`
3. Create a virtual environment: `python -m venv .venv`
4. Activate it: `source .venv/bin/activate` (Linux/Mac) or `.venv\Scripts\activate` (Windows)
5. Install dependencies: `pip install -r requirements.txt`
6. Run the application: `python app.py`

## 🔧 Development Setup

### Prerequisites
- Python 3.8 or higher
- Flask 2.0+
- Git

### Installation
```bash
# Run the setup script
./setup.sh

# Or manual setup
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 📝 Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Write unit tests for new features
- Keep functions small and focused

## 🧪 Testing

Run tests before submitting:
```bash
python test_app.py
```

## 📋 Pull Request Process

1. Create a feature branch: `git checkout -b feature/amazing-feature`
2. Make your changes
3. Add tests for new functionality
4. Ensure all tests pass
5. Update documentation if needed
6. Commit your changes: `git commit -m 'Add amazing feature'`
7. Push to your fork: `git push origin feature/amazing-feature`
8. Create a Pull Request

## 🐛 Bug Reports

When filing a bug report, please include:
- Python version
- Flask version
- Operating system
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages (if any)

## 💡 Feature Requests

We welcome feature requests! Please provide:
- Clear description of the feature
- Why it would be useful
- How it should work
- Any examples or mockups

## 📖 Documentation

- Update README.md for new features
- Add inline comments for complex code
- Update API documentation if needed

## 🏗️ Architecture

The application follows a modular structure:
- `app.py` - Main application entry point
- `config.py` - Configuration management
- `models.py` - Data models
- `auth.py` - Authentication services
- `*_routes.py` - Route handlers
- `exceptions.py` - Custom exceptions
- `logger.py` - Logging configuration

## ❓ Questions?

Feel free to open an issue for questions or join discussions!

Thank you for contributing! 🎉
