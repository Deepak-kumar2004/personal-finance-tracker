"""
Authentication utilities and decorators for Money Manager application
"""
from functools import wraps
from flask import session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Callable, Any, Dict, Tuple
from exceptions import ValidationError, AuthenticationError
import uuid


def login_required(f: Callable) -> Callable:
    """Decorator to require user authentication"""
    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function


class AuthService:
    """Authentication service class"""
    
    def __init__(self, user_model):
        self.user_model = user_model
    
    def hash_password(self, password: str) -> str:
        """Hash a password using werkzeug"""
        return generate_password_hash(password)
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify a password against its hash"""
        return check_password_hash(password_hash, password)
    
    def validate_registration_data(self, username: str, email: str, password: str) -> None:
        """Validate registration data"""
        # Basic validation
        if not username or not email or not password:
            raise ValidationError('All fields are required')
        
        if len(username) < 3:
            raise ValidationError('Username must be at least 3 characters')
        
        if len(password) < 6:
            raise ValidationError('Password must be at least 6 characters')
        
        # Check if user already exists
        if self.user_model.user_exists(username, email):
            raise ValidationError('Username or email already exists')
    
    def register_user(self, username: str, email: str, password: str) -> Dict[str, Any]:
        """Register a new user"""
        self.validate_registration_data(username, email, password)
        
        user_id = str(uuid.uuid4())
        password_hash = self.hash_password(password)
        
        user_data = self.user_model.create_user(username, email, password_hash, user_id)
        
        return {
            'success': True,
            'user_id': user_id,
            'username': username
        }
    
    def authenticate_user(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticate user credentials"""
        user = self.user_model.get_user(username)
        
        if not user:
            raise AuthenticationError('Invalid username or password')
        
        if not self.verify_password(password, user['password']):
            raise AuthenticationError('Invalid username or password')
        
        return {
            'success': True,
            'user_id': user['id'],
        }
    
    def create_session(self, user_data: dict) -> None:
        """Create user session"""
        session['user_id'] = user_data['user_id']
        session['username'] = user_data['username']
    
    def clear_session(self) -> None:
        """Clear user session"""
        session.clear()
        """Clear user session"""
        session.clear()
    
    def get_current_user(self) -> dict:
        """Get current user from session"""
        return {
            'user_id': session.get('user_id'),
            'username': session.get('username')
        }
