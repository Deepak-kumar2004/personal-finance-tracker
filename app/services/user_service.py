"""
User service for handling user-related business logic.
This class is responsible for user settings, categories, and budgets operations.
"""
from typing import Dict, Tuple, Any
from app.models.category import CategoryManager
from app.models.settings import UserSettings, BudgetManager
from app.services.data_service import DataService
from app.services.transaction_service import TransactionService


class UserService:
    """User service class for handling user-related operations."""
    
    def __init__(self, data_service: DataService):
        """
        Initialize UserService with data service.
        
        Args:
            data_service: DataService instance for data operations
        """
        self.data_service = data_service
        self.transaction_service = TransactionService(data_service)
    
    # Category operations
    def get_user_categories(self, user_id: str) -> Dict:
        """
        Get categories for a user.
        
        Args:
            user_id: User ID to get categories for
            
        Returns:
            Dictionary containing categories
        """
        category_manager = self.data_service.load_user_categories(user_id)
        return category_manager.to_dict()
    
    def add_category(self, user_id: str, category_name: str, category_type: str) -> Tuple[bool, str]:
        """
        Add a new category for a user.
        
        Args:
            user_id: User ID to add category for
            category_name: Name of the category
            category_type: 'income' or 'expense'
            
        Returns:
            Tuple of (success, message)
        """
        category_manager = self.data_service.load_user_categories(user_id)
        
        success, message = category_manager.add_category(category_type, category_name)
        
        if success:
            if self.data_service.save_user_categories(user_id, category_manager):
                return True, message
            else:
                return False, "Failed to save category"
        
        return False, message
    
    def delete_category(self, user_id: str, category_name: str, category_type: str) -> Tuple[bool, str]:
        """
        Delete a category for a user.
        
        Args:
            user_id: User ID to delete category for
            category_name: Name of the category to delete
            category_type: 'income' or 'expense'
            
        Returns:
            Tuple of (success, message)
        """
        category_manager = self.data_service.load_user_categories(user_id)
        
        success, message = category_manager.remove_category(category_type, category_name)
        
        if success:
            # Save updated categories
            if self.data_service.save_user_categories(user_id, category_manager):
                # Update transactions that use this category to 'Other'
                self.transaction_service.update_transactions_category(user_id, category_name, 'Other')
                return True, message
            else:
                return False, "Failed to save category changes"
        
        return False, message
    
    # Settings operations
    def get_user_settings(self, user_id: str) -> Dict:
        """
        Get settings for a user.
        
        Args:
            user_id: User ID to get settings for
            
        Returns:
            Dictionary containing user settings
        """
        user_settings = self.data_service.load_user_settings(user_id)
        return user_settings.to_dict()
    
    def update_user_settings(self, user_id: str, settings_data: Dict[str, Any], 
                           valid_currencies: Dict) -> Tuple[bool, str]:
        """
        Update settings for a user.
        
        Args:
            user_id: User ID to update settings for
            settings_data: Dictionary containing settings to update
            valid_currencies: Dictionary of valid currencies
            
        Returns:
            Tuple of (success, message)
        """
        user_settings = self.data_service.load_user_settings(user_id)
        
        # Update currency if provided
        if 'currency' in settings_data:
            success, message = user_settings.update_currency(settings_data['currency'], valid_currencies)
            if not success:
                return False, message
        
        # Update other settings
        for key, value in settings_data.items():
            if key != 'currency':  # Already handled above
                success, message = user_settings.update_setting(key, value)
                if not success:
                    return False, message
        
        # Save updated settings
        if self.data_service.save_user_settings(user_id, user_settings):
            return True, "Settings updated successfully"
        else:
            return False, "Failed to save settings"
    
    # Budget operations
    def get_user_budgets(self, user_id: str) -> Dict:
        """
        Get budgets for a user.
        
        Args:
            user_id: User ID to get budgets for
            
        Returns:
            Dictionary containing user budgets
        """
        budget_manager = self.data_service.load_user_budgets(user_id)
        return budget_manager.to_dict()
    
    def set_budget(self, user_id: str, month: str, amount: float) -> Tuple[bool, str]:
        """
        Set budget for a user.
        
        Args:
            user_id: User ID to set budget for
            month: Month key (e.g., '2025-07')
            amount: Budget amount
            
        Returns:
            Tuple of (success, message)
        """
        budget_manager = self.data_service.load_user_budgets(user_id)
        
        success, message = budget_manager.set_budget(month, amount)
        
        if success:
            if self.data_service.save_user_budgets(user_id, budget_manager):
                return True, message
            else:
                return False, "Failed to save budget"
        
        return False, message
    
    def delete_budget(self, user_id: str, month: str) -> Tuple[bool, str]:
        """
        Delete budget for a user.
        
        Args:
            user_id: User ID to delete budget for
            month: Month key to delete budget for
            
        Returns:
            Tuple of (success, message)
        """
        budget_manager = self.data_service.load_user_budgets(user_id)
        
        success, message = budget_manager.remove_budget(month)
        
        if success:
            if self.data_service.save_user_budgets(user_id, budget_manager):
                return True, message
            else:
                return False, "Failed to save budget changes"
        
        return False, message
