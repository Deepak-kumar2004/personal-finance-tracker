"""
User model for handling user-related data operations.
This class is responsible for user data management and validation.
"""
from datetime import datetime
from typing import Dict, Optional
from werkzeug.security import generate_password_hash, check_password_hash
import uuid


class User:
    """User model class for managing user data and authentication."""
    
    def __init__(self, username: str, email: str, password: str = None, 
                 user_id: str = None, created_at: str = None):
        """
        Initialize a User instance.
        
        Args:
            username: The username for the user
            email: The email address for the user
            password: The plain text password (will be hashed)
            user_id: The unique identifier (generated if not provided)
            created_at: Creation timestamp (generated if not provided)
        """
        self.username = username
        self.email = email
        self.user_id = user_id or str(uuid.uuid4())
        self.created_at = created_at or datetime.now().isoformat()
        
        if password:
            self.password_hash = generate_password_hash(password)
        else:
            self.password_hash = None
    
    def set_password(self, password: str) -> None:
        """Set the user's password with proper hashing."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        """Check if the provided password matches the stored hash."""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self) -> Dict:
        """Convert user object to dictionary for JSON serialization."""
        return {
            'id': self.user_id,
            'email': self.email,
            'password': self.password_hash,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, username: str, data: Dict) -> 'User':
        """Create a User instance from dictionary data."""
        user = cls(
            username=username,
            email=data['email'],
            user_id=data['id'],
            created_at=data['created_at']
        )
        user.password_hash = data['password']
        return user
    
    def validate_username(self) -> bool:
        """Validate username format and length."""
        return len(self.username.strip()) >= 3
    
    def validate_email(self) -> bool:
        """Basic email validation."""
        import re
        email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        return bool(re.match(email_pattern, self.email))
    
    def validate_password(self, password: str) -> bool:
        """Validate password strength."""
        return len(password) >= 6
    
    def __repr__(self) -> str:
        return f"<User {self.username}>"
