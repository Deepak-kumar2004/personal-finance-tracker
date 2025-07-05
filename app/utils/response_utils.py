"""
Response formatting utilities.
This module provides functions for standardizing API responses.
"""
from typing import Any, Dict, Optional
from flask import jsonify


def success_response(message: str, data: Any = None, status_code: int = 200) -> tuple:
    """
    Create a standardized success response.
    
    Args:
        message: Success message
        data: Optional data to include
        status_code: HTTP status code
        
    Returns:
        Flask response tuple
    """
    response = {'message': message}
    if data is not None:
        response.update(data)
    
    return jsonify(response), status_code


def error_response(message: str, status_code: int = 400, error_code: str = None) -> tuple:
    """
    Create a standardized error response.
    
    Args:
        message: Error message
        status_code: HTTP status code
        error_code: Optional error code
        
    Returns:
        Flask response tuple
    """
    response = {'error': message}
    if error_code:
        response['error_code'] = error_code
    
    return jsonify(response), status_code


def data_response(data: Dict, status_code: int = 200) -> tuple:
    """
    Create a response with data only.
    
    Args:
        data: Data to return
        status_code: HTTP status code
        
    Returns:
        Flask response tuple
    """
    return jsonify(data), status_code


def validation_error_response(errors: Dict) -> tuple:
    """
    Create a validation error response.
    
    Args:
        errors: Dictionary of validation errors
        
    Returns:
        Flask response tuple
    """
    return jsonify({
        'error': 'Validation failed',
        'validation_errors': errors
    }), 400
