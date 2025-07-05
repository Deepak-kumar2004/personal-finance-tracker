"""
API routes for user management (categories, settings, budgets).
This module handles all user-related API endpoints.
"""
from flask import Blueprint, request
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.utils.auth_decorators import create_login_required_decorator
from app.utils.response_utils import success_response, error_response, data_response
from config.settings import Config


class UserRoutes:
    """User API routes handler class."""
    
    def __init__(self, auth_service: AuthService, user_service: UserService):
        """
        Initialize UserRoutes with services.
        
        Args:
            auth_service: AuthService instance
            user_service: UserService instance
        """
        self.auth_service = auth_service
        self.user_service = user_service
        self.blueprint = Blueprint('user_api', __name__, url_prefix='/api')
        self.login_required = create_login_required_decorator(auth_service)
        self._register_routes()
    
    def _register_routes(self):
        """Register all user routes."""
        # Category routes
        self.blueprint.add_url_rule('/categories', 'get_categories', 
                                   self.get_categories, methods=['GET'])
        self.blueprint.add_url_rule('/categories', 'add_category', 
                                   self.add_category, methods=['POST'])
        self.blueprint.add_url_rule('/categories/<category_type>/<category_name>', 'delete_category', 
                                   self.delete_category, methods=['DELETE'])
        
        # Settings routes
        self.blueprint.add_url_rule('/settings', 'get_settings', 
                                   self.get_settings, methods=['GET'])
        self.blueprint.add_url_rule('/settings', 'update_settings', 
                                   self.update_settings, methods=['POST'])
        
        # Budget routes
        self.blueprint.add_url_rule('/budgets', 'get_budgets', 
                                   self.get_budgets, methods=['GET'])
        self.blueprint.add_url_rule('/budgets', 'set_budget', 
                                   self.set_budget, methods=['POST'])
        self.blueprint.add_url_rule('/budgets/<month>', 'delete_budget', 
                                   self.delete_budget, methods=['DELETE'])
        
        # Currency route (public)
        self.blueprint.add_url_rule('/currencies', 'get_currencies', 
                                   self.get_currencies, methods=['GET'])
    
    # Category routes
    @property
    def get_categories(self):
        """Get all categories for the current user."""
        @self.login_required
        def _get_categories():
            user_id = self.auth_service.get_current_user_id()
            categories = self.user_service.get_user_categories(user_id)
            return data_response(categories)
        return _get_categories
    
    @property
    def add_category(self):
        """Add a new category for the current user."""
        @self.login_required
        def _add_category():
            user_id = self.auth_service.get_current_user_id()
            data = request.get_json()
            
            # Validate input
            if not data or 'name' not in data or 'type' not in data:
                return error_response('Missing category name or type')
            
            category_name = data['name'].strip()
            category_type = data['type']
            
            if not category_name:
                return error_response('Category name cannot be empty')
            
            if category_type not in ['income', 'expense']:
                return error_response('Type must be income or expense')
            
            # Add category
            success, message = self.user_service.add_category(user_id, category_name, category_type)
            
            if success:
                return success_response(message, {'category': category_name}, 201)
            else:
                return error_response(message)
        return _add_category
    
    @property
    def delete_category(self):
        """Delete a category for the current user."""
        @self.login_required
        def _delete_category(category_type, category_name):
            user_id = self.auth_service.get_current_user_id()
            
            if category_type not in ['income', 'expense']:
                return error_response('Invalid category type')
            
            success, message = self.user_service.delete_category(user_id, category_name, category_type)
            
            if success:
                return success_response(message)
            else:
                return error_response(message)
        return _delete_category
    
    # Settings routes
    @property
    def get_settings(self):
        """Get user settings for the current user."""
        @self.login_required
        def _get_settings():
            user_id = self.auth_service.get_current_user_id()
            settings = self.user_service.get_user_settings(user_id)
            return data_response(settings)
        return _get_settings
    
    @property
    def update_settings(self):
        """Update user settings for the current user."""
        @self.login_required
        def _update_settings():
            user_id = self.auth_service.get_current_user_id()
            data = request.get_json()
            
            if not data:
                return error_response('No data provided')
            
            # Update settings
            success, message = self.user_service.update_user_settings(
                user_id, data, Config.CURRENCIES
            )
            
            if success:
                settings = self.user_service.get_user_settings(user_id)
                return success_response(message, {'settings': settings})
            else:
                return error_response(message)
        return _update_settings
    
    # Budget routes
    @property
    def get_budgets(self):
        """Get all budgets for the current user."""
        @self.login_required
        def _get_budgets():
            user_id = self.auth_service.get_current_user_id()
            budgets = self.user_service.get_user_budgets(user_id)
            return data_response(budgets)
        return _get_budgets
    
    @property
    def set_budget(self):
        """Set monthly budget for the current user."""
        @self.login_required
        def _set_budget():
            user_id = self.auth_service.get_current_user_id()
            data = request.get_json()
            
            # Validate input
            if not data or 'amount' not in data or 'month' not in data:
                return error_response('Missing budget amount or month')
            
            try:
                amount = float(data['amount'])
                if amount <= 0:
                    return error_response('Budget amount must be positive')
            except ValueError:
                return error_response('Invalid budget amount')
            
            month = data['month'].strip()
            if not month:
                return error_response('Month cannot be empty')
            
            # Set budget
            success, message = self.user_service.set_budget(user_id, month, amount)
            
            if success:
                return success_response(message, {'month': month, 'amount': amount}, 201)
            else:
                return error_response(message)
        return _set_budget
    
    @property
    def delete_budget(self):
        """Delete a monthly budget for the current user."""
        @self.login_required
        def _delete_budget(month):
            user_id = self.auth_service.get_current_user_id()
            
            success, message = self.user_service.delete_budget(user_id, month)
            
            if success:
                return success_response(message)
            else:
                return error_response(message)
        return _delete_budget
    
    # Currency route (public)
    def get_currencies(self):
        """Get all supported currencies."""
        return data_response(Config.CURRENCIES)
