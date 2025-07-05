"""
Configuration settings for the Personal Finance Tracker application.
This module handles all configuration-related functionality.
"""
import os
from typing import Dict, Any


class Config:
    """Base configuration class with default settings."""
    
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-this-in-production'
    
    # Application settings
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # Data storage paths
    USERS_FILE = os.environ.get('USERS_FILE', 'users.json')
    DATA_DIR = os.environ.get('DATA_DIR', 'user_data')
    
    # Supported currencies with their symbols and flag emojis
    CURRENCIES = {
        'USD': {'symbol': '$', 'name': 'US Dollar', 'flag': '🇺🇸'},
        'EUR': {'symbol': '€', 'name': 'Euro', 'flag': '🇪🇺'},
        'GBP': {'symbol': '£', 'name': 'British Pound', 'flag': '🇬🇧'},
        'JPY': {'symbol': '¥', 'name': 'Japanese Yen', 'flag': '🇯🇵'},
        'CAD': {'symbol': 'C$', 'name': 'Canadian Dollar', 'flag': '🇨🇦'},
        'AUD': {'symbol': 'A$', 'name': 'Australian Dollar', 'flag': '🇦🇺'},
        'CHF': {'symbol': 'CHF', 'name': 'Swiss Franc', 'flag': '🇨🇭'},
        'CNY': {'symbol': '¥', 'name': 'Chinese Yuan', 'flag': '🇨🇳'},
        'INR': {'symbol': '₹', 'name': 'Indian Rupee', 'flag': '🇮🇳'},
        'BRL': {'symbol': 'R$', 'name': 'Brazilian Real', 'flag': '🇧🇷'},
        'RUB': {'symbol': '₽', 'name': 'Russian Ruble', 'flag': '🇷🇺'},
        'KRW': {'symbol': '₩', 'name': 'South Korean Won', 'flag': '🇰🇷'},
        'SEK': {'symbol': 'kr', 'name': 'Swedish Krona', 'flag': '🇸🇪'},
        'NOK': {'symbol': 'kr', 'name': 'Norwegian Krone', 'flag': '🇳🇴'},
        'MXN': {'symbol': '$', 'name': 'Mexican Peso', 'flag': '🇲🇽'},
        'SGD': {'symbol': 'S$', 'name': 'Singapore Dollar', 'flag': '🇸🇬'},
        'NZD': {'symbol': 'NZ$', 'name': 'New Zealand Dollar', 'flag': '🇳🇿'}
    }


class DevelopmentConfig(Config):
    """Development configuration with debug enabled."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration with enhanced security."""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    def __init__(self):
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY environment variable must be set in production")


class TestingConfig(Config):
    """Testing configuration for unit tests."""
    TESTING = True
    USERS_FILE = 'test_users.json'
    DATA_DIR = 'test_user_data'


# Configuration factory
def get_config() -> Config:
    """Get configuration based on environment."""
    env = os.environ.get('FLASK_ENV', 'development').lower()
    
    if env == 'production':
        return ProductionConfig()
    elif env == 'testing':
        return TestingConfig()
    else:
        return DevelopmentConfig()
