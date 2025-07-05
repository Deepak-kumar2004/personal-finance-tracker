"""
Currency formatting utilities.
This module provides functions for formatting currency amounts.
"""
from typing import Dict


def format_currency(amount: float, currency_code: str = 'USD', currencies: Dict = None) -> str:
    """
    Format amount with currency symbol.
    
    Args:
        amount: Amount to format
        currency_code: Currency code (e.g., 'USD', 'EUR')
        currencies: Dictionary of supported currencies
        
    Returns:
        Formatted currency string
    """
    if currencies and currency_code in currencies:
        symbol = currencies[currency_code]['symbol']
        
        # No decimal places for these currencies
        if currency_code in ['JPY', 'KRW']:
            return f"{symbol}{int(amount):,}"
        else:
            return f"{symbol}{amount:,.2f}"
    
    # Default formatting
    return f"{amount:.2f}"


def get_currency_symbol(currency_code: str, currencies: Dict) -> str:
    """
    Get currency symbol for a currency code.
    
    Args:
        currency_code: Currency code
        currencies: Dictionary of supported currencies
        
    Returns:
        Currency symbol or default '$'
    """
    if currencies and currency_code in currencies:
        return currencies[currency_code].get('symbol', '$')
    return '$'


def validate_currency_code(currency_code: str, currencies: Dict) -> bool:
    """
    Validate if currency code is supported.
    
    Args:
        currency_code: Currency code to validate
        currencies: Dictionary of supported currencies
        
    Returns:
        True if valid, False otherwise
    """
    return currency_code in currencies if currencies else False
