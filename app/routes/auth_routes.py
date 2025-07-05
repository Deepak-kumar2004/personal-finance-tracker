"""
Authentication routes for user registration, login, and logout.
This module handles all authentication-related endpoints.
"""
from flask import Blueprint, render_template, request, redirect, url_for
from app.services.auth_service import AuthService
from app.utils.response_utils import success_response, error_response


class AuthRoutes:
    """Authentication routes handler class."""
    
    def __init__(self, auth_service: AuthService):
        """
        Initialize AuthRoutes with auth service.
        
        Args:
            auth_service: AuthService instance
        """
        self.auth_service = auth_service
        self.blueprint = Blueprint('auth', __name__)
        self._register_routes()
    
    def _register_routes(self):
        """Register all authentication routes."""
        self.blueprint.add_url_rule('/', 'home', self.home, methods=['GET'])
        self.blueprint.add_url_rule('/register', 'register', self.register, methods=['GET', 'POST'])
        self.blueprint.add_url_rule('/login', 'login', self.login, methods=['GET', 'POST'])
        self.blueprint.add_url_rule('/logout', 'logout', self.logout, methods=['GET'])
        self.blueprint.add_url_rule('/clear-session', 'clear_session', self.clear_session, methods=['GET'])
    
    def home(self):
        """Home page - show login/register or redirect to dashboard."""
        try:
            if self.auth_service.is_authenticated():
                return redirect(url_for('main.dashboard'))
        except Exception as e:
            # If there's any issue with authentication, clear session and show home
            self.auth_service.destroy_session()
        return render_template('home.html')
    
    def register(self):
        """User registration endpoint."""
        if request.method == 'GET':
            return render_template('register.html')
        
        # Handle POST request
        data = request.get_json()
        if not data:
            return error_response('No data provided')
        
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        # Register user
        success, message, user = self.auth_service.register_user(username, email, password)
        
        if success:
            # Create session for the new user
            self.auth_service.create_session(user)
            return success_response(message, {'redirect': '/dashboard'}, 201)
        else:
            return error_response(message)
    
    def login(self):
        """User login endpoint."""
        if request.method == 'GET':
            return render_template('login.html')
        
        # Handle POST request
        data = request.get_json()
        if not data:
            return error_response('No data provided')
        
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        # Authenticate user
        success, message, user = self.auth_service.login_user(username, password)
        
        if success:
            # Create session for the user
            self.auth_service.create_session(user)
            return success_response(message, {'redirect': '/dashboard'})
        else:
            return error_response(message, 401)
    
    def logout(self):
        """User logout endpoint."""
        self.auth_service.destroy_session()
        return redirect(url_for('auth.home'))
    
    def clear_session(self):
        """Clear session for debugging purposes."""
        self.auth_service.destroy_session()
        return redirect(url_for('auth.home'))
