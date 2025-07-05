"""
Transaction model for handling financial transaction data.
This class is responsible for transaction data management and validation.
"""
from datetime import datetime
from typing import Dict, List, Optional


class Transaction:
    """Transaction model class for managing financial transaction data."""
    
    def __init__(self, description: str, amount: float, transaction_type: str,
                 category: str = 'Other', transaction_id: int = None, 
                 date: str = None):
        """
        Initialize a Transaction instance.
        
        Args:
            description: Description of the transaction
            amount: Amount of the transaction
            transaction_type: Type of transaction ('income' or 'expense')
            category: Category of the transaction
            transaction_id: Unique identifier for the transaction
            date: Date of the transaction (ISO format string)
        """
        self.transaction_id = transaction_id
        self.description = description.strip()
        self.amount = float(amount)
        self.transaction_type = transaction_type
        self.category = category
        self.date = date or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def to_dict(self) -> Dict:
        """Convert transaction object to dictionary for JSON serialization."""
        return {
            'id': self.transaction_id,
            'description': self.description,
            'amount': self.amount,
            'type': self.transaction_type,
            'category': self.category,
            'date': self.date
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Transaction':
        """Create a Transaction instance from dictionary data."""
        return cls(
            description=data['description'],
            amount=data['amount'],
            transaction_type=data['type'],
            category=data.get('category', 'Other'),
            transaction_id=data.get('id'),
            date=data.get('date')
        )
    
    def validate(self) -> tuple[bool, str]:
        """
        Validate transaction data.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.description:
            return False, "Description cannot be empty"
        
        if self.amount <= 0:
            return False, "Amount must be positive"
        
        if self.transaction_type not in ['income', 'expense']:
            return False, "Type must be 'income' or 'expense'"
        
        if not self.category:
            return False, "Category cannot be empty"
        
        return True, ""
    
    def get_month_key(self) -> str:
        """Get the month key for grouping transactions."""
        date_obj = datetime.strptime(self.date, '%Y-%m-%d %H:%M:%S')
        return date_obj.strftime('%Y-%m')
    
    def is_income(self) -> bool:
        """Check if transaction is income."""
        return self.transaction_type == 'income'
    
    def is_expense(self) -> bool:
        """Check if transaction is expense."""
        return self.transaction_type == 'expense'
    
    def __repr__(self) -> str:
        return f"<Transaction {self.transaction_id}: {self.description} - {self.amount}>"


class TransactionSummary:
    """Class for calculating transaction summaries and statistics."""
    
    def __init__(self, transactions: List[Transaction]):
        """Initialize with a list of transactions."""
        self.transactions = transactions
    
    def calculate_balance(self) -> float:
        """Calculate total balance from all transactions."""
        balance = 0.0
        for transaction in self.transactions:
            if transaction.is_income():
                balance += transaction.amount
            else:
                balance -= transaction.amount
        return balance
    
    def calculate_total_income(self) -> float:
        """Calculate total income from all transactions."""
        return sum(t.amount for t in self.transactions if t.is_income())
    
    def calculate_total_expenses(self) -> float:
        """Calculate total expenses from all transactions."""
        return sum(t.amount for t in self.transactions if t.is_expense())
    
    def get_monthly_stats(self) -> Dict:
        """Get monthly income and expense statistics."""
        monthly_stats = {}
        
        for transaction in self.transactions:
            month_key = transaction.get_month_key()
            
            if month_key not in monthly_stats:
                monthly_stats[month_key] = {'income': 0, 'expenses': 0}
            
            if transaction.is_income():
                monthly_stats[month_key]['income'] += transaction.amount
            else:
                monthly_stats[month_key]['expenses'] += transaction.amount
        
        return monthly_stats
    
    def get_category_stats(self) -> Dict:
        """Get expense statistics by category."""
        category_stats = {}
        
        for transaction in self.transactions:
            if transaction.is_expense():
                category = transaction.category
                category_stats[category] = category_stats.get(category, 0) + transaction.amount
        
        return category_stats
    
    def get_summary(self) -> Dict:
        """Get complete transaction summary."""
        return {
            'balance': self.calculate_balance(),
            'total_income': self.calculate_total_income(),
            'total_expenses': self.calculate_total_expenses(),
            'monthly_stats': self.get_monthly_stats(),
            'category_stats': self.get_category_stats()
        }
