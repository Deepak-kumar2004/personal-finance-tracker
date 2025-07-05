"""
Settings model for handling user preferences and configurations.
This class is responsible for user settings management.
"""
from typing import Dict, Any


class UserSettings:
    """User settings model class for managing user preferences."""
    
    def __init__(self, currency: str = 'USD', date_format: str = '%Y-%m-%d %H:%M:%S', **kwargs):
        """
        Initialize UserSettings instance.
        
        Args:
            currency: Default currency code
            date_format: Date format string
            **kwargs: Additional settings
        """
        self.currency = currency
        self.date_format = date_format
        self.additional_settings = kwargs
    
    def get_default_settings(self) -> Dict[str, Any]:
        """Get default settings for new users."""
        return {
            'currency': 'USD',
            'date_format': '%Y-%m-%d %H:%M:%S'
        }
    
    def update_currency(self, currency_code: str, valid_currencies: Dict) -> tuple[bool, str]:
        """
        Update currency setting.
        
        Args:
            currency_code: New currency code
            valid_currencies: Dictionary of valid currencies
            
        Returns:
            Tuple of (success, message)
        """
        if currency_code not in valid_currencies:
            return False, "Invalid currency code"
        
        self.currency = currency_code
        return True, "Currency updated successfully"
    
    def update_date_format(self, date_format: str) -> tuple[bool, str]:
        """
        Update date format setting.
        
        Args:
            date_format: New date format string
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Test the format by formatting current date
            from datetime import datetime
            datetime.now().strftime(date_format)
            self.date_format = date_format
            return True, "Date format updated successfully"
        except ValueError:
            return False, "Invalid date format"
    
    def update_setting(self, key: str, value: Any) -> tuple[bool, str]:
        """
        Update any setting.
        
        Args:
            key: Setting key
            value: Setting value
            
        Returns:
            Tuple of (success, message)
        """
        if key == 'currency':
            # Note: This requires valid_currencies to be passed
            # In practice, this would be handled by the service layer
            self.currency = value
        elif key == 'date_format':
            return self.update_date_format(value)
        else:
            self.additional_settings[key] = value
        
        return True, f"Setting '{key}' updated successfully"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert settings to dictionary for JSON serialization."""
        settings = {
            'currency': self.currency,
            'date_format': self.date_format
        }
        settings.update(self.additional_settings)
        return settings
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserSettings':
        """Create UserSettings instance from dictionary data."""
        currency = data.pop('currency', 'USD')
        date_format = data.pop('date_format', '%Y-%m-%d %H:%M:%S')
        return cls(currency=currency, date_format=date_format, **data)
    
    def __repr__(self) -> str:
        return f"<UserSettings: {self.currency}, {self.date_format}>"


class BudgetManager:
    """Budget manager class for handling monthly budgets."""
    
    def __init__(self, budgets: Dict[str, float] = None):
        """
        Initialize BudgetManager.
        
        Args:
            budgets: Dictionary of month -> budget amount
        """
        self.budgets = budgets or {}
    
    def set_budget(self, month: str, amount: float) -> tuple[bool, str]:
        """
        Set budget for a specific month.
        
        Args:
            month: Month key (e.g., '2025-07')
            amount: Budget amount
            
        Returns:
            Tuple of (success, message)
        """
        if amount <= 0:
            return False, "Budget amount must be positive"
        
        if not month.strip():
            return False, "Month cannot be empty"
        
        self.budgets[month] = float(amount)
        return True, "Budget set successfully"
    
    def get_budget(self, month: str) -> float:
        """Get budget for a specific month."""
        return self.budgets.get(month, 0.0)
    
    def remove_budget(self, month: str) -> tuple[bool, str]:
        """
        Remove budget for a specific month.
        
        Args:
            month: Month key to remove
            
        Returns:
            Tuple of (success, message)
        """
        if month in self.budgets:
            del self.budgets[month]
            return True, "Budget deleted successfully"
        
        return False, "Budget not found"
    
    def get_all_budgets(self) -> Dict[str, float]:
        """Get all budgets."""
        return self.budgets.copy()
    
    def to_dict(self) -> Dict[str, float]:
        """Convert budgets to dictionary for JSON serialization."""
        return self.budgets
    
    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> 'BudgetManager':
        """Create BudgetManager instance from dictionary data."""
        return cls(data)
    
    def __repr__(self) -> str:
        return f"<BudgetManager: {len(self.budgets)} budgets>"
