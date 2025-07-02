"""
Configuration settings for Money Manager application
"""
import os

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-this-in-production'
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000
    
    # Data configuration
    USERS_FILE = 'users.json'
    DATA_DIR = 'user_data'
    
    # Supported currencies with symbols and flag emojis
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
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-this-in-production'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
