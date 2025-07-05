#!/usr/bin/env python3
"""
Debug script to check Flask app configuration
"""
import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.app_factory import create_app
from config.settings import get_config

def debug_app():
    config = get_config()
    app = create_app(config)
    
    print("=== Flask App Debug Info ===")
    print(f"App instance path: {app.instance_path}")
    print(f"Template folder: {app.template_folder}")
    print(f"Static folder: {app.static_folder}")
    print(f"Template folder exists: {os.path.exists(app.template_folder)}")
    print(f"Static folder exists: {os.path.exists(app.static_folder)}")
    
    # List templates
    if os.path.exists(app.template_folder):
        templates = os.listdir(app.template_folder)
        print(f"Templates found: {templates}")
        print(f"dashboard.html exists: {'dashboard.html' in templates}")
    
    # Test template loading
    with app.app_context():
        try:
            from flask import render_template_string
            print("App context working...")
            
            # Try to list all available templates
            from jinja2 import select_autoescape
            print(f"Template loader: {app.jinja_env.loader}")
            print(f"Template search path: {app.jinja_env.loader.searchpath if hasattr(app.jinja_env.loader, 'searchpath') else 'No searchpath'}")
            
        except Exception as e:
            print(f"Error in app context: {e}")

if __name__ == '__main__':
    debug_app()
