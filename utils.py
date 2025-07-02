"""
Utility functions for Money Manager application
"""
from datetime import datetime
from typing import Dict, List, Any, Tuple
from config import Config


def format_currency(amount: float, currency_code: str = 'USD') -> str:
    """Format amount with currency symbol"""
    config = Config()
    
    if currency_code in config.CURRENCIES:
        symbol = config.CURRENCIES[currency_code]['symbol']
        if currency_code in ['JPY', 'KRW']:  # No decimal places for these currencies
            return f"{symbol}{int(amount):,}"
        else:
            return f"{symbol}{amount:,.2f}"
    return f"{amount:.2f}"


def calculate_stats(transactions: List[Dict[str, Any]]) -> Tuple[Dict[str, Any], Dict[str, float]]:
    """Calculate monthly and category statistics from transactions"""
    monthly_stats = {}
    category_stats = {}
    
    for transaction in transactions:
        # Monthly stats
        try:
            date = datetime.strptime(transaction['date'], '%Y-%m-%d %H:%M:%S')
            month_key = date.strftime('%Y-%m')
            
            if month_key not in monthly_stats:
                monthly_stats[month_key] = {'income': 0, 'expenses': 0}
            
            if transaction['type'] == 'income':
                monthly_stats[month_key]['income'] += transaction['amount']
            else:
                monthly_stats[month_key]['expenses'] += transaction['amount']
            
            # Category stats (for expenses only)
            if transaction['type'] == 'expense':
                category = transaction.get('category', 'Other')
                category_stats[category] = category_stats.get(category, 0) + transaction['amount']
        
        except ValueError as e:
            print(f"Error parsing date {transaction.get('date')}: {e}")
            continue
    
    return monthly_stats, category_stats


def validate_transaction_data(data: Dict[str, Any]) -> Tuple[bool, str]:
    """Validate transaction data"""
    if not data:
        return False, 'No data provided'
    
    required_fields = ['description', 'amount', 'type']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return False, f'Missing required fields: {", ".join(missing_fields)}'
    
    # Validate amount
    try:
        amount = float(data['amount'])
        if amount <= 0:
            return False, 'Amount must be positive'
    except (ValueError, TypeError):
        return False, 'Invalid amount format'
    
    # Validate type
    if data['type'] not in ['income', 'expense']:
        return False, 'Type must be income or expense'
    
    # Validate description
    if not data['description'].strip():
        return False, 'Description cannot be empty'
    
    return True, 'Valid'


def validate_category_data(data: Dict[str, Any]) -> Tuple[bool, str]:
    """Validate category data"""
    if not data:
        return False, 'No data provided'
    
    if 'name' not in data or 'type' not in data:
        return False, 'Missing category name or type'
    
    category_name = data['name'].strip()
    category_type = data['type']
    
    if not category_name:
        return False, 'Category name cannot be empty'
    
    if category_type not in ['income', 'expense']:
        return False, 'Type must be income or expense'
    
    return True, 'Valid'


def validate_budget_data(data: Dict[str, Any]) -> Tuple[bool, str]:
    """Validate budget data"""
    if not data:
        return False, 'No data provided'
    
    if 'amount' not in data or 'month' not in data:
        return False, 'Missing budget amount or month'
    
    # Validate amount
    try:
        amount = float(data['amount'])
        if amount <= 0:
            return False, 'Budget amount must be positive'
    except (ValueError, TypeError):
        return False, 'Invalid budget amount format'
    
    # Validate month
    month = data['month'].strip()
    if not month:
        return False, 'Month cannot be empty'
    
    # Basic month format validation (YYYY-MM)
    try:
        datetime.strptime(month, '%Y-%m')
    except ValueError:
        return False, 'Invalid month format. Use YYYY-MM format'
    
    return True, 'Valid'


def sanitize_input(value: str) -> str:
    """Sanitize string input"""
    if not isinstance(value, str):
        return str(value)
    return value.strip()


def get_current_month() -> str:
    """Get current month in YYYY-MM format"""
    return datetime.now().strftime('%Y-%m')


def get_month_name(month_str: str) -> str:
    """Convert YYYY-MM format to readable month name"""
    try:
        date = datetime.strptime(month_str, '%Y-%m')
        return date.strftime('%B %Y')
    except ValueError:
        return month_str
