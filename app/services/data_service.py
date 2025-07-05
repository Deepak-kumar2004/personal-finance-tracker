"""
Data access layer for handling file-based data operations.
This class is responsible for reading and writing data to JSON files.
"""
import json
import os
from typing import Dict, List, Any, Optional
from app.models.user import User
from app.models.transaction import Transaction
from app.models.category import CategoryManager
from app.models.settings import UserSettings, BudgetManager


class DataService:
    """Data service class for handling file-based data operations."""
    
    def __init__(self, users_file: str, data_dir: str):
        """
        Initialize DataService with file paths.
        
        Args:
            users_file: Path to users JSON file
            data_dir: Directory for user-specific data files
        """
        self.users_file = users_file
        self.data_dir = data_dir
        self._ensure_directories()
    
    def _ensure_directories(self) -> None:
        """Ensure required directories exist."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def _get_user_data_path(self, user_id: str, filename: str) -> str:
        """Get the path for user-specific data file."""
        user_dir = os.path.join(self.data_dir, user_id)
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        return os.path.join(user_dir, filename)
    
    def _read_json_file(self, file_path: str, default: Any = None) -> Any:
        """
        Read JSON file with error handling.
        
        Args:
            file_path: Path to JSON file
            default: Default value if file doesn't exist
            
        Returns:
            Parsed JSON data or default value
        """
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error reading {file_path}: {e}")
        
        return default if default is not None else {}
    
    def _write_json_file(self, file_path: str, data: Any) -> bool:
        """
        Write data to JSON file with error handling.
        
        Args:
            file_path: Path to JSON file
            data: Data to write
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except (IOError, TypeError) as e:
            print(f"Error writing {file_path}: {e}")
            return False
    
    # User data operations
    def load_users(self) -> Dict[str, User]:
        """Load all users from file."""
        users_data = self._read_json_file(self.users_file, {})
        users = {}
        
        for username, user_data in users_data.items():
            users[username] = User.from_dict(username, user_data)
        
        return users
    
    def save_users(self, users: Dict[str, User]) -> bool:
        """Save all users to file."""
        users_data = {}
        for username, user in users.items():
            users_data[username] = user.to_dict()
        
        return self._write_json_file(self.users_file, users_data)
    
    def user_exists(self, username: str) -> bool:
        """Check if user exists."""
        users = self.load_users()
        return username in users
    
    def email_exists(self, email: str) -> bool:
        """Check if email already exists."""
        users = self.load_users()
        return any(user.email == email for user in users.values())
    
    # Transaction data operations
    def load_user_transactions(self, user_id: str) -> List[Transaction]:
        """Load transactions for a specific user."""
        file_path = self._get_user_data_path(user_id, 'transactions.json')
        transactions_data = self._read_json_file(file_path, [])
        
        transactions = []
        for transaction_data in transactions_data:
            transactions.append(Transaction.from_dict(transaction_data))
        
        return transactions
    
    def save_user_transactions(self, user_id: str, transactions: List[Transaction]) -> bool:
        """Save transactions for a specific user."""
        file_path = self._get_user_data_path(user_id, 'transactions.json')
        transactions_data = [transaction.to_dict() for transaction in transactions]
        
        return self._write_json_file(file_path, transactions_data)
    
    def get_next_transaction_id(self, user_id: str) -> int:
        """Get the next available transaction ID for a user."""
        transactions = self.load_user_transactions(user_id)
        if not transactions:
            return 1
        
        max_id = max(t.transaction_id for t in transactions if t.transaction_id)
        return max_id + 1
    
    # Category data operations
    def load_user_categories(self, user_id: str) -> CategoryManager:
        """Load categories for a specific user."""
        file_path = self._get_user_data_path(user_id, 'categories.json')
        categories_data = self._read_json_file(file_path)
        
        if categories_data:
            return CategoryManager.from_dict(categories_data)
        else:
            # Create default categories for new user
            category_manager = CategoryManager()
            self.save_user_categories(user_id, category_manager)
            return category_manager
    
    def save_user_categories(self, user_id: str, category_manager: CategoryManager) -> bool:
        """Save categories for a specific user."""
        file_path = self._get_user_data_path(user_id, 'categories.json')
        return self._write_json_file(file_path, category_manager.to_dict())
    
    # Settings data operations
    def load_user_settings(self, user_id: str) -> UserSettings:
        """Load settings for a specific user."""
        file_path = self._get_user_data_path(user_id, 'settings.json')
        settings_data = self._read_json_file(file_path)
        
        if settings_data:
            return UserSettings.from_dict(settings_data)
        else:
            # Create default settings for new user
            user_settings = UserSettings()
            self.save_user_settings(user_id, user_settings)
            return user_settings
    
    def save_user_settings(self, user_id: str, user_settings: UserSettings) -> bool:
        """Save settings for a specific user."""
        file_path = self._get_user_data_path(user_id, 'settings.json')
        return self._write_json_file(file_path, user_settings.to_dict())
    
    # Budget data operations
    def load_user_budgets(self, user_id: str) -> BudgetManager:
        """Load budgets for a specific user."""
        file_path = self._get_user_data_path(user_id, 'budgets.json')
        budgets_data = self._read_json_file(file_path, {})
        
        return BudgetManager.from_dict(budgets_data)
    
    def save_user_budgets(self, user_id: str, budget_manager: BudgetManager) -> bool:
        """Save budgets for a specific user."""
        file_path = self._get_user_data_path(user_id, 'budgets.json')
        return self._write_json_file(file_path, budget_manager.to_dict())
