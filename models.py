"""
Data models and database operations for Money Manager application
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from config import Config
from exceptions import DataError, NotFoundError, ValidationError
from logger import LoggerSetup


class BaseModel:
    """
    Base class for all data models with enhanced error handling and logging
    """
    
    def __init__(self, config: Config):
        """
        Initialize base model
        
        Args:
            config: Application configuration object
        """
        self.config = config
        self.logger = LoggerSetup.setup_logger("models")
        self._ensure_data_dir()
    
    def _ensure_data_dir(self):
        """Ensure data directory exists"""
        try:
            if not os.path.exists(self.config.DATA_DIR):
                os.makedirs(self.config.DATA_DIR)
                self.logger.info(f"Created data directory: {self.config.DATA_DIR}")
        except Exception as e:
            self.logger.error(f"Failed to create data directory: {str(e)}")
            raise DataError("Failed to create data directory")
    
    def _get_user_data_path(self, user_id: str, filename: str) -> str:
        """
        Get path for user-specific data file
        
        Args:
            user_id: User ID
            filename: Name of the data file
            
        Returns:
            Full path to the user data file
        """
        try:
            user_dir = os.path.join(self.config.DATA_DIR, user_id)
            if not os.path.exists(user_dir):
                os.makedirs(user_dir)
                self.logger.info(f"Created user directory: {user_dir}")
            return os.path.join(user_dir, filename)
        except Exception as e:
            self.logger.error(f"Failed to get user data path for {user_id}/{filename}: {str(e)}")
            raise DataError("Failed to access user data directory")
    
    def _load_json(self, file_path: str, default: Any = None) -> Any:
        """
        Load JSON data from file with comprehensive error handling
        
        Args:
            file_path: Path to the JSON file
            default: Default value to return if file doesn't exist
            
        Returns:
            Loaded data or default value
            
        Raises:
            DataError: If file exists but cannot be loaded
        """
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.logger.debug(f"Successfully loaded {file_path}")
                    return data
            except json.JSONDecodeError as e:
                self.logger.error(f"Invalid JSON in {file_path}: {str(e)}")
                raise DataError(f"Invalid JSON in file: {file_path}")
            except IOError as e:
                self.logger.error(f"IO error loading {file_path}: {str(e)}")
                raise DataError(f"Cannot read file: {file_path}")
        else:
            self.logger.debug(f"File not found, returning default: {file_path}")
            return default if default is not None else {}
    
    def _save_json(self, file_path: str, data: Any) -> None:
        """
        Save JSON data to file with error handling
        
        Args:
            file_path: Path to save the JSON file
            data: Data to save
            
        Raises:
            DataError: If data cannot be saved
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.logger.debug(f"Successfully saved {file_path}")
        except IOError as e:
            self.logger.error(f"IO error saving {file_path}: {str(e)}")
            raise DataError(f"Cannot save file: {file_path}")
        except Exception as e:
            self.logger.error(f"Unexpected error saving {file_path}: {str(e)}")
            raise DataError(f"Failed to save file: {file_path}")


class UserModel(BaseModel):
    """User management model"""
    
    def load_users(self) -> Dict[str, Any]:
        """Load all users from JSON file"""
        return self._load_json(self.config.USERS_FILE, {})
    
    def save_users(self, users: Dict[str, Any]) -> None:
        """Save users to JSON file"""
        self._save_json(self.config.USERS_FILE, users)
    
    def user_exists(self, username: str, email: str) -> bool:
        """Check if user exists by username or email"""
        users = self.load_users()
        return username in users or any(
            user.get('email') == email for user in users.values()
        )
    
    def create_user(self, username: str, email: str, password_hash: str, user_id: str) -> Dict[str, Any]:
        """Create a new user"""
        users = self.load_users()
        user_data = {
            'id': user_id,
            'email': email,
            'password': password_hash,
            'created_at': datetime.now().isoformat()
        }
        users[username] = user_data
        self.save_users(users)
        return user_data
    
    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        users = self.load_users()
        return users.get(username)


class TransactionModel(BaseModel):
    """Transaction management model"""
    
    def load_user_transactions(self, user_id: str) -> List[Dict[str, Any]]:
        """Load transactions for a specific user"""
        file_path = self._get_user_data_path(user_id, 'transactions.json')
        return self._load_json(file_path, [])
    
    def save_user_transactions(self, user_id: str, transactions: List[Dict[str, Any]]) -> None:
        """Save transactions for a specific user"""
        file_path = self._get_user_data_path(user_id, 'transactions.json')
        self._save_json(file_path, transactions)
    
    def add_transaction(self, user_id: str, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new transaction"""
        # Validate transaction data
        if transaction_data.get('amount', 0) <= 0:
            raise ValidationError("Amount must be positive")
        
        transactions = self.load_user_transactions(user_id)
        
        transaction = {
            'id': len(transactions) + 1,
            'description': transaction_data['description'].strip(),
            'amount': float(transaction_data['amount']),
            'type': transaction_data['type'],
            'category': transaction_data.get('category', 'Other'),
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        transactions.append(transaction)
        self.save_user_transactions(user_id, transactions)
        return transaction
    
    def delete_transaction(self, user_id: str, transaction_id: int) -> None:
        """Delete a transaction"""
        transactions = self.load_user_transactions(user_id)
        filtered_transactions = [t for t in transactions if t['id'] != transaction_id]
        self.save_user_transactions(user_id, filtered_transactions)
    
    def calculate_balance(self, transactions: List[Dict[str, Any]]) -> float:
        """Calculate total balance from transactions"""
        balance = 0.0
        for transaction in transactions:
            if transaction['type'] == 'income':
                balance += transaction['amount']
            else:
                balance -= transaction['amount']
        return balance
    
    def get_totals(self, transactions: List[Dict[str, Any]]) -> Dict[str, float]:
        """Get income and expense totals"""
        total_income = sum(t['amount'] for t in transactions if t['type'] == 'income')
        total_expenses = sum(t['amount'] for t in transactions if t['type'] == 'expense')
        return {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'balance': self.calculate_balance(transactions)
        }


class CategoryModel(BaseModel):
    """Category management model"""
    
    def get_default_categories(self) -> Dict[str, List[str]]:
        """Get default categories for new users"""
        return {
            'expense': ['Food', 'Transportation', 'Entertainment', 'Utilities', 
                       'Shopping', 'Healthcare', 'Education', 'Other'],
            'income': ['Salary', 'Freelance', 'Investment', 'Business', 'Other']
        }
    
    def load_user_categories(self, user_id: str) -> Dict[str, List[str]]:
        """Load categories for a specific user"""
        file_path = self._get_user_data_path(user_id, 'categories.json')
        categories = self._load_json(file_path)
        
        if categories is None:
            # Create default categories for new user
            categories = self.get_default_categories()
            self.save_user_categories(user_id, categories)
        
        return categories
    
    def save_user_categories(self, user_id: str, categories: Dict[str, List[str]]) -> None:
        """Save categories for a specific user"""
        file_path = self._get_user_data_path(user_id, 'categories.json')
        self._save_json(file_path, categories)
    
    def add_category(self, user_id: str, category_name: str, category_type: str) -> bool:
        """Add a new category"""
        categories = self.load_user_categories(user_id)
        
        if category_name in categories[category_type]:
            return False  # Category already exists
        
        categories[category_type].append(category_name)
        self.save_user_categories(user_id, categories)
        return True
    
    def delete_category(self, user_id: str, category_name: str, category_type: str) -> bool:
        """Delete a category and update related transactions"""
        if category_name == 'Other':
            return False  # Cannot delete 'Other' category
        
        categories = self.load_user_categories(user_id)
        
        if category_name in categories[category_type]:
            categories[category_type].remove(category_name)
            self.save_user_categories(user_id, categories)
            
            # Update transactions that use this category
            transaction_model = TransactionModel(self.config)
            transactions = transaction_model.load_user_transactions(user_id)
            for transaction in transactions:
                if transaction.get('category') == category_name:
                    transaction['category'] = 'Other'
            transaction_model.save_user_transactions(user_id, transactions)
            
            return True
        return False


class SettingsModel(BaseModel):
    """Settings management model"""
    
    def get_default_settings(self) -> Dict[str, Any]:
        """Get default settings for new users"""
        return {
            'currency': 'USD',
            'date_format': '%Y-%m-%d %H:%M:%S'
        }
    
    def load_user_settings(self, user_id: str) -> Dict[str, Any]:
        """Load settings for a specific user"""
        file_path = self._get_user_data_path(user_id, 'settings.json')
        settings = self._load_json(file_path)
        
        if settings is None:
            # Create default settings for new user
            settings = self.get_default_settings()
            self.save_user_settings(user_id, settings)
        
        return settings
    
    def save_user_settings(self, user_id: str, settings: Dict[str, Any]) -> None:
        """Save settings for a specific user"""
        file_path = self._get_user_data_path(user_id, 'settings.json')
        self._save_json(file_path, settings)
    
    def update_settings(self, user_id: str, new_settings: Dict[str, Any]) -> None:
        """Update user settings"""
        current_settings = self.load_user_settings(user_id)
        current_settings.update(new_settings)
        self.save_user_settings(user_id, current_settings)


class BudgetModel(BaseModel):
    """Budget management model"""
    
    def load_user_budgets(self, user_id: str) -> Dict[str, float]:
        """Load budgets for a specific user"""
        file_path = self._get_user_data_path(user_id, 'budgets.json')
        return self._load_json(file_path, {})
    
    def save_user_budgets(self, user_id: str, budgets: Dict[str, float]) -> None:
        """Save budgets for a specific user"""
        file_path = self._get_user_data_path(user_id, 'budgets.json')
        self._save_json(file_path, budgets)
    
    def set_budget(self, user_id: str, month: str, amount: float) -> None:
        """Set monthly budget"""
        budgets = self.load_user_budgets(user_id)
        budgets[month] = amount
        self.save_user_budgets(user_id, budgets)
    
    def delete_budget(self, user_id: str, month: str) -> None:
        """Delete a monthly budget"""
        budgets = self.load_user_budgets(user_id)
        if month in budgets:
            del budgets[month]
            self.save_user_budgets(user_id, budgets)
