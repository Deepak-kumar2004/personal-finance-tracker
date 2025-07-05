"""
Authentication utilities for Flask routes.
This module provides decorators for authentication and session management.
"""
from functools import wraps
from flask import jsonify
from app.services.auth_service import AuthService


def create_login_required_decorator(auth_service: AuthService):
    """
    Create a login_required decorator with access to AuthService.
    
    Args:
        auth_service: AuthService instance
        
    Returns:
        login_required decorator function
    """
    def login_required(f):
        """
        Decorator to require authentication for routes.
        
        Args:
            f: Function to decorate
            
        Returns:
            Decorated function
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            is_authenticated, error_message = auth_service.require_authentication()
            if not is_authenticated:
                return jsonify({'error': error_message}), 401
            return f(*args, **kwargs)
        return decorated_function
    
    return login_required
