"""
Custom exceptions for Money Manager application
"""


class MoneyManagerException(Exception):
    """Base exception for Money Manager application"""
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class ValidationError(MoneyManagerException):
    """Raised when input validation fails"""
    def __init__(self, message: str):
        super().__init__(message, 400)


class AuthenticationError(MoneyManagerException):
    """Raised when authentication fails"""
    def __init__(self, message: str = "Authentication required"):
        super().__init__(message, 401)


class AuthorizationError(MoneyManagerException):
    """Raised when user is not authorized for an action"""
    def __init__(self, message: str = "Access denied"):
        super().__init__(message, 403)


class NotFoundError(MoneyManagerException):
    """Raised when requested resource is not found"""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, 404)


class DataError(MoneyManagerException):
    """Raised when data operations fail"""
    def __init__(self, message: str = "Data operation failed"):
        super().__init__(message, 500)


class ConfigurationError(MoneyManagerException):
    """Raised when configuration is invalid"""
    def __init__(self, message: str = "Configuration error"):
        super().__init__(message, 500)
