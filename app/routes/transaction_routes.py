"""
API routes for transaction management.
This module handles all transaction-related API endpoints.
"""
from flask import Blueprint, request
from app.services.auth_service import AuthService
from app.services.transaction_service import TransactionService
from app.services.user_service import UserService
from app.utils.auth_decorators import create_login_required_decorator
from app.utils.response_utils import success_response, error_response, data_response
from app.utils.currency_utils import get_currency_symbol
from config.settings import Config


class TransactionRoutes:
    """Transaction API routes handler class."""
    
    def __init__(self, auth_service: AuthService, transaction_service: TransactionService, 
                 user_service: UserService):
        """
        Initialize TransactionRoutes with services.
        
        Args:
            auth_service: AuthService instance
            transaction_service: TransactionService instance
            user_service: UserService instance
        """
        self.auth_service = auth_service
        self.transaction_service = transaction_service
        self.user_service = user_service
        self.blueprint = Blueprint('transactions', __name__, url_prefix='/api')
        self.login_required = create_login_required_decorator(auth_service)
        self._register_routes()
    
    def _register_routes(self):
        """Register all transaction routes."""
        self.blueprint.add_url_rule('/transactions', 'get_transactions', 
                                   self.get_transactions, methods=['GET'])
        self.blueprint.add_url_rule('/transactions', 'add_transaction', 
                                   self.add_transaction, methods=['POST'])
        self.blueprint.add_url_rule('/transactions/<int:transaction_id>', 'delete_transaction', 
                                   self.delete_transaction, methods=['DELETE'])
        self.blueprint.add_url_rule('/stats', 'get_stats', 
                                   self.get_stats, methods=['GET'])
    
    @property
    def get_transactions(self):
        """Get all transactions for the current user."""
        @self.login_required
        def _get_transactions():
            user_id = self.auth_service.get_current_user_id()
            
            # Get user settings for currency
            settings = self.user_service.get_user_settings(user_id)
            currency = settings.get('currency', 'USD')
            currency_symbol = get_currency_symbol(currency, Config.CURRENCIES)
            
            # Get transactions with summary
            data = self.transaction_service.get_transactions_with_summary(
                user_id, currency, currency_symbol
            )
            
            return data_response(data)
        return _get_transactions
    
    @property
    def add_transaction(self):
        """Add a new transaction for the current user."""
        @self.login_required
        def _add_transaction():
            user_id = self.auth_service.get_current_user_id()
            data = request.get_json()
            
            # Validate input
            if not data or 'description' not in data or 'amount' not in data or 'type' not in data:
                return error_response('Missing required fields')
            
            try:
                amount = float(data['amount'])
                if amount <= 0:
                    return error_response('Amount must be positive')
            except ValueError:
                return error_response('Invalid amount')
            
            if data['type'] not in ['income', 'expense']:
                return error_response('Type must be income or expense')
            
            # Add transaction
            success, message, transaction = self.transaction_service.add_transaction(
                user_id=user_id,
                description=data['description'],
                amount=amount,
                transaction_type=data['type'],
                category=data.get('category', 'Other')
            )
            
            if success:
                return success_response(message, {'transaction': transaction.to_dict()}, 201)
            else:
                return error_response(message)
        return _add_transaction
    
    @property
    def delete_transaction(self):
        """Delete a transaction for the current user."""
        @self.login_required
        def _delete_transaction(transaction_id):
            user_id = self.auth_service.get_current_user_id()
            
            success, message = self.transaction_service.delete_transaction(user_id, transaction_id)
            
            if success:
                return success_response(message)
            else:
                return error_response(message)
        return _delete_transaction
    
    @property
    def get_stats(self):
        """Get financial statistics for the current user."""
        @self.login_required
        def _get_stats():
            user_id = self.auth_service.get_current_user_id()
            stats = self.transaction_service.get_financial_stats(user_id)
            return data_response(stats)
        return _get_stats
