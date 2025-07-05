"""
Transaction service for handling transaction-related business logic.
This class is responsible for transaction operations and calculations.
"""
from typing import List, Dict, Tuple, Optional
from app.models.transaction import Transaction, TransactionSummary
from app.services.data_service import DataService


class TransactionService:
    """Transaction service class for handling transaction operations."""
    
    def __init__(self, data_service: DataService):
        """
        Initialize TransactionService with data service.
        
        Args:
            data_service: DataService instance for data operations
        """
        self.data_service = data_service
    
    def get_user_transactions(self, user_id: str) -> List[Transaction]:
        """
        Get all transactions for a user.
        
        Args:
            user_id: User ID to get transactions for
            
        Returns:
            List of Transaction objects
        """
        return self.data_service.load_user_transactions(user_id)
    
    def add_transaction(self, user_id: str, description: str, amount: float, 
                       transaction_type: str, category: str = 'Other') -> Tuple[bool, str, Optional[Transaction]]:
        """
        Add a new transaction for a user.
        
        Args:
            user_id: User ID to add transaction for
            description: Transaction description
            amount: Transaction amount
            transaction_type: 'income' or 'expense'
            category: Transaction category
            
        Returns:
            Tuple of (success, message, transaction_object)
        """
        # Get next transaction ID
        transaction_id = self.data_service.get_next_transaction_id(user_id)
        
        # Create transaction
        transaction = Transaction(
            description=description,
            amount=amount,
            transaction_type=transaction_type,
            category=category,
            transaction_id=transaction_id
        )
        
        # Validate transaction
        is_valid, error_message = transaction.validate()
        if not is_valid:
            return False, error_message, None
        
        # Load existing transactions
        transactions = self.data_service.load_user_transactions(user_id)
        
        # Add new transaction
        transactions.append(transaction)
        
        # Save transactions
        if self.data_service.save_user_transactions(user_id, transactions):
            return True, "Transaction added successfully", transaction
        else:
            return False, "Failed to save transaction", None
    
    def delete_transaction(self, user_id: str, transaction_id: int) -> Tuple[bool, str]:
        """
        Delete a transaction for a user.
        
        Args:
            user_id: User ID to delete transaction for
            transaction_id: ID of transaction to delete
            
        Returns:
            Tuple of (success, message)
        """
        # Load transactions
        transactions = self.data_service.load_user_transactions(user_id)
        
        # Filter out the transaction to delete
        original_count = len(transactions)
        transactions = [t for t in transactions if t.transaction_id != transaction_id]
        
        if len(transactions) == original_count:
            return False, "Transaction not found"
        
        # Save updated transactions
        if self.data_service.save_user_transactions(user_id, transactions):
            return True, "Transaction deleted successfully"
        else:
            return False, "Failed to delete transaction"
    
    def get_transaction_summary(self, user_id: str) -> Dict:
        """
        Get transaction summary for a user.
        
        Args:
            user_id: User ID to get summary for
            
        Returns:
            Dictionary containing transaction summary
        """
        transactions = self.data_service.load_user_transactions(user_id)
        summary = TransactionSummary(transactions)
        return summary.get_summary()
    
    def get_transactions_with_summary(self, user_id: str, currency: str, currency_symbol: str) -> Dict:
        """
        Get transactions with summary information.
        
        Args:
            user_id: User ID to get data for
            currency: Currency code
            currency_symbol: Currency symbol
            
        Returns:
            Dictionary containing transactions and summary
        """
        transactions = self.data_service.load_user_transactions(user_id)
        summary = TransactionSummary(transactions)
        
        return {
            'transactions': [t.to_dict() for t in transactions],
            'balance': summary.calculate_balance(),
            'total_income': summary.calculate_total_income(),
            'total_expenses': summary.calculate_total_expenses(),
            'currency': currency,
            'currency_symbol': currency_symbol
        }
    
    def get_financial_stats(self, user_id: str) -> Dict:
        """
        Get financial statistics for a user.
        
        Args:
            user_id: User ID to get statistics for
            
        Returns:
            Dictionary containing financial statistics
        """
        transactions = self.data_service.load_user_transactions(user_id)
        summary = TransactionSummary(transactions)
        
        return {
            'monthly_stats': summary.get_monthly_stats(),
            'category_stats': summary.get_category_stats()
        }
    
    def update_transactions_category(self, user_id: str, old_category: str, new_category: str) -> bool:
        """
        Update category for all transactions using a specific category.
        
        Args:
            user_id: User ID to update transactions for
            old_category: Category to replace
            new_category: New category name
            
        Returns:
            True if successful, False otherwise
        """
        transactions = self.data_service.load_user_transactions(user_id)
        
        # Update transactions with the old category
        updated = False
        for transaction in transactions:
            if transaction.category == old_category:
                transaction.category = new_category
                updated = True
        
        if updated:
            return self.data_service.save_user_transactions(user_id, transactions)
        
        return True  # No updates needed
