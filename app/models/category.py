"""
Category model for handling transaction categories.
This class is responsible for category data management and validation.
"""
from typing import Dict, List


class CategoryManager:
    """Category manager class for handling income and expense categories."""
    
    def __init__(self, categories: Dict = None):
        """
        Initialize CategoryManager with default or provided categories.
        
        Args:
            categories: Dictionary with 'income' and 'expense' category lists
        """
        if categories is None:
            self.categories = self._get_default_categories()
        else:
            self.categories = categories
    
    def _get_default_categories(self) -> Dict[str, List[str]]:
        """Get default categories for new users."""
        return {
            'expense': [
                'Food', 'Transportation', 'Entertainment', 'Utilities',
                'Shopping', 'Healthcare', 'Education', 'Other'
            ],
            'income': [
                'Salary', 'Freelance', 'Investment', 'Business', 'Other'
            ]
        }
    
    def get_categories(self) -> Dict[str, List[str]]:
        """Get all categories."""
        return self.categories
    
    def get_income_categories(self) -> List[str]:
        """Get income categories."""
        return self.categories.get('income', [])
    
    def get_expense_categories(self) -> List[str]:
        """Get expense categories."""
        return self.categories.get('expense', [])
    
    def add_category(self, category_type: str, category_name: str) -> tuple[bool, str]:
        """
        Add a new category.
        
        Args:
            category_type: 'income' or 'expense'
            category_name: Name of the category to add
            
        Returns:
            Tuple of (success, message)
        """
        category_name = category_name.strip()
        
        # Validation
        if not category_name:
            return False, "Category name cannot be empty"
        
        if category_type not in ['income', 'expense']:
            return False, "Type must be 'income' or 'expense'"
        
        if category_name in self.categories[category_type]:
            return False, "Category already exists"
        
        # Add category
        self.categories[category_type].append(category_name)
        return True, "Category added successfully"
    
    def remove_category(self, category_type: str, category_name: str) -> tuple[bool, str]:
        """
        Remove a category.
        
        Args:
            category_type: 'income' or 'expense'
            category_name: Name of the category to remove
            
        Returns:
            Tuple of (success, message)
        """
        # Validation
        if category_type not in ['income', 'expense']:
            return False, "Invalid category type"
        
        if category_name == 'Other':
            return False, "Cannot delete 'Other' category"
        
        if category_name not in self.categories[category_type]:
            return False, "Category does not exist"
        
        # Remove category
        self.categories[category_type].remove(category_name)
        return True, "Category deleted successfully"
    
    def category_exists(self, category_type: str, category_name: str) -> bool:
        """Check if a category exists."""
        return category_name in self.categories.get(category_type, [])
    
    def validate_category(self, category_type: str, category_name: str) -> bool:
        """Validate if a category is valid for the given type."""
        return self.category_exists(category_type, category_name)
    
    def to_dict(self) -> Dict:
        """Convert categories to dictionary for JSON serialization."""
        return self.categories
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'CategoryManager':
        """Create CategoryManager instance from dictionary data."""
        return cls(data)
    
    def __repr__(self) -> str:
        income_count = len(self.categories.get('income', []))
        expense_count = len(self.categories.get('expense', []))
        return f"<CategoryManager: {income_count} income, {expense_count} expense categories>"
