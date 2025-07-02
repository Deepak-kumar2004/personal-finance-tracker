"""
API routes for Money Manager application
"""
from flask import Blueprint, request, jsonify, session
from datetime import datetime
from auth import login_required
from models import TransactionModel, CategoryModel, SettingsModel, BudgetModel
from utils import format_currency, calculate_stats
from config import Config
from exceptions import ValidationError, DataError
from logger import LoggerSetup


# Create API blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')


class ApiController:
    """API Controller class to handle all API endpoints"""
    
    def __init__(self, config: Config):
        self.config = config
        self.transaction_model = TransactionModel(config)
        self.category_model = CategoryModel(config)
        self.settings_model = SettingsModel(config)
        self.budget_model = BudgetModel(config)
        self.logger = LoggerSetup.setup_logger("api")
    
    def setup_routes(self, blueprint: Blueprint):
        """Setup all API routes"""
        # Transaction routes
        blueprint.add_url_rule('/transactions', 'get_transactions', 
                             self.get_transactions, methods=['GET'])
        blueprint.add_url_rule('/transactions', 'add_transaction', 
                             self.add_transaction, methods=['POST'])
        blueprint.add_url_rule('/transactions/<int:transaction_id>', 'delete_transaction', 
                             self.delete_transaction, methods=['DELETE'])
        
        # Category routes
        blueprint.add_url_rule('/categories', 'get_categories', 
                             self.get_categories, methods=['GET'])
        blueprint.add_url_rule('/categories', 'add_category', 
                             self.add_category, methods=['POST'])
        blueprint.add_url_rule('/categories/<category_type>/<category_name>', 'delete_category', 
                             self.delete_category, methods=['DELETE'])
        
        # Settings routes
        blueprint.add_url_rule('/settings', 'get_settings', 
                             self.get_settings, methods=['GET'])
        blueprint.add_url_rule('/settings', 'update_settings', 
                             self.update_settings, methods=['POST'])
        
        # Budget routes
        blueprint.add_url_rule('/budgets', 'get_budgets', 
                             self.get_budgets, methods=['GET'])
        blueprint.add_url_rule('/budgets', 'set_budget', 
                             self.set_budget, methods=['POST'])
        blueprint.add_url_rule('/budgets/<month>', 'delete_budget', 
                             self.delete_budget, methods=['DELETE'])
        
        # Other routes
        blueprint.add_url_rule('/stats', 'get_stats', 
                             self.get_stats, methods=['GET'])
        blueprint.add_url_rule('/currencies', 'get_currencies', 
                             self.get_currencies, methods=['GET'])
    
    @login_required
    def get_transactions(self):
        """Get all transactions for the current user"""
        user_id = session['user_id']
        transactions = self.transaction_model.load_user_transactions(user_id)
        settings = self.settings_model.load_user_settings(user_id)
        currency = settings.get('currency', 'USD')
        
        # Calculate totals
        totals = self.transaction_model.get_totals(transactions)
        
        return jsonify({
            'transactions': transactions,
            'balance': totals['balance'],
            'total_income': totals['total_income'],
            'total_expenses': totals['total_expenses'],
            'currency': currency,
            'currency_symbol': self.config.CURRENCIES.get(currency, {}).get('symbol', '$')
        })
    
    @login_required
    def add_transaction(self):
        """Add a new transaction for the current user"""
        user_id = session['user_id']
        data = request.get_json()
        
        # Validate input
        if not data or not all(key in data for key in ['description', 'amount', 'type']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        if data['type'] not in ['income', 'expense']:
            return jsonify({'error': 'Type must be income or expense'}), 400
        
        try:
            # Add transaction using model
            transaction = self.transaction_model.add_transaction(user_id, data)
            self.logger.info(f"User {user_id} added transaction: {transaction['description']}")
            return jsonify({
                'message': 'Transaction added successfully', 
                'transaction': transaction
            }), 201
        except ValidationError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            self.logger.error(f"Error adding transaction for user {user_id}: {str(e)}")
            return jsonify({'error': 'Failed to add transaction'}), 500
    
    @login_required
    def delete_transaction(self, transaction_id: int):
        """Delete a transaction for the current user"""
        user_id = session['user_id']
        
        try:
            self.transaction_model.delete_transaction(user_id, transaction_id)
            self.logger.info(f"User {user_id} deleted transaction {transaction_id}")
            return jsonify({'message': 'Transaction deleted successfully'})
        except Exception as e:
            self.logger.error(f"Error deleting transaction {transaction_id} for user {user_id}: {str(e)}")
            return jsonify({'error': 'Failed to delete transaction'}), 500
    
    @login_required
    def get_stats(self):
        """Get financial statistics for the current user"""
        user_id = session['user_id']
        transactions = self.transaction_model.load_user_transactions(user_id)
        
        monthly_stats, category_stats = calculate_stats(transactions)
        
        return jsonify({
            'monthly_stats': monthly_stats,
            'category_stats': category_stats
        })
    
    @login_required
    def get_categories(self):
        """Get all categories for the current user"""
        user_id = session['user_id']
        categories = self.category_model.load_user_categories(user_id)
        return jsonify(categories)
    
    @login_required
    def add_category(self):
        """Add a new category for the current user"""
        user_id = session['user_id']
        data = request.get_json()
        
        # Validate input
        if not data or 'name' not in data or 'type' not in data:
            return jsonify({'error': 'Missing category name or type'}), 400
        
        category_name = data['name'].strip()
        category_type = data['type']
        
        if not category_name:
            return jsonify({'error': 'Category name cannot be empty'}), 400
        
        if category_type not in ['income', 'expense']:
            return jsonify({'error': 'Type must be income or expense'}), 400
        
        # Add category
        if self.category_model.add_category(user_id, category_name, category_type):
            return jsonify({
                'message': 'Category added successfully', 
                'category': category_name
            }), 201
        
        return jsonify({'error': 'Category already exists'}), 400
    
    @login_required
    def delete_category(self, category_type: str, category_name: str):
        """Delete a category for the current user"""
        user_id = session['user_id']
        
        if category_type not in ['income', 'expense']:
            return jsonify({'error': 'Invalid category type'}), 400
        
        if category_name == 'Other':
            return jsonify({'error': 'Cannot delete Other category'}), 400
        
        if self.category_model.delete_category(user_id, category_name, category_type):
            return jsonify({'message': 'Category deleted successfully'})
        
        return jsonify({'error': 'Category not found'}), 404
    
    def get_currencies(self):
        """Get all supported currencies"""
        return jsonify(self.config.CURRENCIES)
    
    @login_required
    def get_settings(self):
        """Get user settings for the current user"""
        user_id = session['user_id']
        settings = self.settings_model.load_user_settings(user_id)
        return jsonify(settings)
    
    @login_required
    def update_settings(self):
        """Update user settings for the current user"""
        user_id = session['user_id']
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate currency if provided
        if 'currency' in data:
            currency = data['currency']
            if currency not in self.config.CURRENCIES:
                return jsonify({'error': 'Invalid currency code'}), 400
        
        # Update settings
        if self.settings_model.update_settings(user_id, data):
            settings = self.settings_model.load_user_settings(user_id)
            return jsonify({
                'message': 'Settings updated successfully', 
                'settings': settings
            })
        
        return jsonify({'error': 'Failed to update settings'}), 500
    
    @login_required
    def get_budgets(self):
        """Get all budgets for the current user"""
        user_id = session['user_id']
        budgets = self.budget_model.load_user_budgets(user_id)
        return jsonify(budgets)
    
    @login_required
    def set_budget(self):
        """Set monthly budget for the current user"""
        user_id = session['user_id']
        data = request.get_json()
        
        # Validate input
        if not data or 'amount' not in data or 'month' not in data:
            return jsonify({'error': 'Missing budget amount or month'}), 400
        
        try:
            amount = float(data['amount'])
            if amount <= 0:
                return jsonify({'error': 'Budget amount must be positive'}), 400
        except ValueError:
            return jsonify({'error': 'Invalid budget amount'}), 400
        
        month = data['month'].strip()
        if not month:
            return jsonify({'error': 'Month cannot be empty'}), 400
        
        # Set budget
        if self.budget_model.set_budget(user_id, month, amount):
            return jsonify({
                'message': 'Budget set successfully', 
                'month': month, 
                'amount': amount
            }), 201
        
        return jsonify({'error': 'Failed to set budget'}), 500
    
    @login_required
    def delete_budget(self, month: str):
        """Delete a monthly budget for the current user"""
        user_id = session['user_id']
        
        if self.budget_model.delete_budget(user_id, month):
            return jsonify({'message': 'Budget deleted successfully'})
        
        return jsonify({'error': 'Failed to delete budget'}), 500
