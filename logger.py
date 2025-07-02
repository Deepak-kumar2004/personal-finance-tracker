"""
Logging configuration for Money Manager application
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime


class LoggerSetup:
    """Setup and configure logging for the application"""
    
    @staticmethod
    def setup_logger(app_name: str = "money_manager", log_level: str = "INFO") -> logging.Logger:
        """
        Setup application logger with file and console handlers
        
        Args:
            app_name: Name of the application for logging
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            
        Returns:
            Configured logger instance
        """
        # Create logs directory if it doesn't exist
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Create logger
        logger = logging.getLogger(app_name)
        logger.setLevel(getattr(logging, log_level.upper()))
        
        # Avoid adding handlers multiple times
        if logger.handlers:
            return logger
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s'
        )
        
        simple_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # File handler for all logs
        file_handler = RotatingFileHandler(
            filename=os.path.join(log_dir, f"{app_name}.log"),
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        
        # File handler for errors only
        error_file_handler = RotatingFileHandler(
            filename=os.path.join(log_dir, f"{app_name}_errors.log"),
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        error_file_handler.setLevel(logging.ERROR)
        error_file_handler.setFormatter(detailed_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)
        
        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(error_file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    @staticmethod
    def log_request(logger: logging.Logger, request, response_status: int = None):
        """
        Log HTTP request details
        
        Args:
            logger: Logger instance
            request: Flask request object
            response_status: HTTP response status code
        """
        log_message = f"{request.method} {request.path}"
        if request.query_string:
            log_message += f"?{request.query_string.decode()}"
        
        if response_status:
            log_message += f" - Status: {response_status}"
        
        logger.info(log_message)
    
    @staticmethod
    def log_user_action(logger: logging.Logger, user_id: str, action: str, details: str = None):
        """
        Log user actions for audit trail
        
        Args:
            logger: Logger instance
            user_id: User ID performing the action
            action: Action being performed
            details: Additional details about the action
        """
        log_message = f"User {user_id} - {action}"
        if details:
            log_message += f" - {details}"
        
        logger.info(log_message)
    
    @staticmethod
    def log_error(logger: logging.Logger, error: Exception, context: str = None):
        """
        Log error with context information
        
        Args:
            logger: Logger instance
            error: Exception that occurred
            context: Additional context about where the error occurred
        """
        error_message = f"Error: {str(error)}"
        if context:
            error_message = f"{context} - {error_message}"
        
        logger.error(error_message, exc_info=True)


# Global logger instance
logger = LoggerSetup.setup_logger()
