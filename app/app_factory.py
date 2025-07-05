"""
Flask application factory for the Personal Finance Tracker.
This module creates and configures the Flask application with all services and routes.
"""
from flask import Flask
from config.settings import get_config
from app.services.data_service import DataService
from app.services.auth_service import AuthService
from app.services.transaction_service import TransactionService
from app.services.user_service import UserService
from app.routes.auth_routes import AuthRoutes
from app.routes.main_routes import MainRoutes
from app.routes.transaction_routes import TransactionRoutes
from app.routes.user_routes import UserRoutes


def create_app(config=None):
    """
    Create and configure Flask application.
    
    Args:
        config: Configuration object (optional)
        
    Returns:
        Configured Flask application
    """
    # Get the project root directory (parent of app directory)
    import os
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Create Flask app with correct template and static directories
    app = Flask(__name__, 
                template_folder=os.path.join(project_root, 'templates'),
                static_folder=os.path.join(project_root, 'static'))
    
    # Load configuration
    if config is None:
        config = get_config()
    
    app.config.from_object(config)
    app.secret_key = config.SECRET_KEY
    
    # Initialize services
    data_service = DataService(config.USERS_FILE, config.DATA_DIR)
    auth_service = AuthService(data_service)
    transaction_service = TransactionService(data_service)
    user_service = UserService(data_service)
    
    # Initialize and register route handlers
    auth_routes = AuthRoutes(auth_service)
    main_routes = MainRoutes(auth_service)
    transaction_routes = TransactionRoutes(auth_service, transaction_service, user_service)
    user_routes = UserRoutes(auth_service, user_service)
    
    # Register blueprints
    app.register_blueprint(auth_routes.blueprint)
    app.register_blueprint(main_routes.blueprint)
    app.register_blueprint(transaction_routes.blueprint)
    app.register_blueprint(user_routes.blueprint)
    
    return app


def create_app_with_context():
    """
    Create app and return app with its services for external access.
    Useful for testing or when services need to be accessed directly.
    
    Returns:
        Tuple of (app, services_dict)
    """
    config = get_config()
    app = create_app(config)
    
    # Create services for external access
    data_service = DataService(config.USERS_FILE, config.DATA_DIR)
    auth_service = AuthService(data_service)
    transaction_service = TransactionService(data_service)
    user_service = UserService(data_service)
    
    services = {
        'data_service': data_service,
        'auth_service': auth_service,
        'transaction_service': transaction_service,
        'user_service': user_service
    }
    
    return app, services
