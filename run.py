#!/usr/bin/env python3
"""
Main entry point for the Personal Finance Tracker application.
This is the new modular version with proper separation of concerns.
"""
import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.app_factory import create_app
from config.settings import get_config


def main():
    """Main function to run the application."""
    # Get configuration
    config = get_config()
    
    print(f"Starting Personal Finance Tracker...")
    print(f"Debug mode: {config.DEBUG}")
    print(f"Host: {config.HOST}")
    print(f"Port: {config.PORT}")
    
    # Create Flask application
    app = create_app(config)
    
    # Run the application
    app.run(
        debug=config.DEBUG,
        host=config.HOST,
        port=config.PORT
    )


if __name__ == '__main__':
    main()
