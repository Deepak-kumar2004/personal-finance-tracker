"""
Main application routes for dashboard and other web pages.
This module handles main web page endpoints.
"""
from flask import Blueprint, render_template
from app.services.auth_service import AuthService
from app.utils.auth_decorators import create_login_required_decorator


class MainRoutes:
    """Main routes handler class."""
    
    def __init__(self, auth_service: AuthService):
        """
        Initialize MainRoutes with auth service.
        
        Args:
            auth_service: AuthService instance
        """
        self.auth_service = auth_service
        self.blueprint = Blueprint('main', __name__)
        self.login_required = create_login_required_decorator(auth_service)
        self._register_routes()
    
    def _register_routes(self):
        """Register all main routes."""
        self.blueprint.add_url_rule('/dashboard', 'dashboard', self.dashboard, methods=['GET'])
    
    @property
    def dashboard(self):
        """Dashboard endpoint with authentication required."""
        @self.login_required
        def _dashboard():
            username = self.auth_service.get_current_username()
            return render_template('dashboard.html', username=username)
        return _dashboard
