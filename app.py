"""
Money Manager Flask Application - Modular Structure
"""
import os
from flask import Flask, jsonify, request
from config import config
from main_routes import MainController, main_bp
from api_routes import ApiController, api_bp
from exceptions import MoneyManagerException
from logger import LoggerSetup


class MoneyManagerApp:
    """
    Main application class for Money Manager
    
    This class encapsulates the Flask application setup, configuration,
    and initialization of all components including routes, error handlers,
    and logging.
    """
    
    def __init__(self, config_name: str = 'development'):
        """
        Initialize the Money Manager application
        
        Args:
            config_name: Configuration environment name (development/production)
        """
        self.app = Flask(__name__)
        self.config_name = config_name
        self.config = None
        self.logger = LoggerSetup.setup_logger("money_manager")
        self._setup_app()
    
    def _setup_app(self):
        """
        Setup Flask application with configuration, routes, and error handlers
        """
        try:
            # Load configuration
            self.config = config.get(self.config_name, config['default'])
            if not self.config:
                raise Exception(f"Configuration '{self.config_name}' not found")
                
            self.app.config.from_object(self.config)
            
            # Setup secret key
            self.app.secret_key = self.config.SECRET_KEY
            
            # Ensure data directory exists
            if not os.path.exists(self.config.DATA_DIR):
                os.makedirs(self.config.DATA_DIR)
                self.logger.info(f"Created data directory: {self.config.DATA_DIR}")
            
            # Setup routes
            self._setup_routes()
            
            # Setup error handlers
            self._setup_error_handlers()
            
            # Setup request logging
            self._setup_request_logging()
            
            self.logger.info(f"Application setup completed successfully for environment: {self.config_name}")
            
        except Exception as e:
            self.logger.error(f"Failed to setup application: {str(e)}")
            raise
    
    def _setup_routes(self):
        """Setup all application routes"""
        # Initialize controllers
        main_controller = MainController(self.config)
        api_controller = ApiController(self.config)
        
        # Setup routes
        main_controller.setup_routes(main_bp)
        api_controller.setup_routes(api_bp)
        
        # Register blueprints
        self.app.register_blueprint(main_bp)
        self.app.register_blueprint(api_bp)
    
    def _setup_error_handlers(self):
        """Setup comprehensive error handlers"""
        @self.app.errorhandler(MoneyManagerException)
        def handle_money_manager_exception(error):
            """Handle custom Money Manager exceptions"""
            self.logger.error(f"MoneyManager Exception: {error.message}")
            return jsonify({'error': error.message}), error.status_code
        
        @self.app.errorhandler(404)
        def not_found(error):
            """Handle 404 errors"""
            self.logger.warning(f"404 Error: {request.url}")
            return jsonify({'error': 'Resource not found'}), 404
        
        @self.app.errorhandler(500)
        def internal_error(error):
            """Handle 500 errors"""
            self.logger.error(f"500 Error: {str(error)}")
            return jsonify({'error': 'Internal server error'}), 500
        
        @self.app.errorhandler(401)
        def unauthorized(error):
            """Handle 401 errors"""
            self.logger.warning(f"401 Error: Unauthorized access attempt")
            return jsonify({'error': 'Authentication required'}), 401
        
        @self.app.errorhandler(403)
        def forbidden(error):
            """Handle 403 errors"""
            self.logger.warning(f"403 Error: Access denied")
            return jsonify({'error': 'Access denied'}), 403
    
    def _setup_request_logging(self):
        """Setup request logging middleware"""
        @self.app.before_request
        def log_request_info():
            """Log request information"""
            LoggerSetup.log_request(self.logger, request)
        
        @self.app.after_request
        def log_response_info(response):
            """Log response information"""
            LoggerSetup.log_request(self.logger, request, response.status_code)
            return response
    
    def run(self, **kwargs):
        """
        Run the Flask application
        
        Args:
            **kwargs: Additional parameters to pass to Flask's run method
        """
        # Default run parameters
        run_params = {
            'debug': self.config.DEBUG,
            'host': self.config.HOST,
            'port': self.config.PORT
        }
        
        # Override with any provided parameters
        run_params.update(kwargs)
        
        self.logger.info(f"Starting Money Manager application...")
        self.logger.info(f"Configuration: {self.config_name}")
        self.logger.info(f"Debug mode: {run_params['debug']}")
        self.logger.info(f"Running on http://{run_params['host']}:{run_params['port']}")
        
        self.app.run(**run_params)
    
    def get_app(self):
        """
        Get the Flask app instance
        
        Returns:
            Flask application instance
        """
        return self.app


def create_app(config_name: str = 'development') -> Flask:
    """
    Factory function to create Flask app
    
    Args:
        config_name: Configuration environment name
        
    Returns:
        Flask application instance
    """
    money_manager = MoneyManagerApp(config_name)
    return money_manager.get_app()


if __name__ == '__main__':
    # Get configuration from environment
    env = os.environ.get('FLASK_ENV', 'development')
    
    # Create and run the application
    app_instance = MoneyManagerApp(env)
    app_instance.run()
