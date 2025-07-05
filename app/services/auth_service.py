"""
Authentication service for handling user authentication and session management.
This class is responsible for user registration, login, and authentication validation.
"""
from typing import Optional, Tuple
from flask import session
from app.models.user import User
from app.services.data_service import DataService


class AuthService:
    """Authentication service class for handling user authentication."""
    
    def __init__(self, data_service: DataService):
        """
        Initialize AuthService with data service.
        
        Args:
            data_service: DataService instance for data operations
        """
        self.data_service = data_service
    
    def register_user(self, username: str, email: str, password: str) -> Tuple[bool, str, Optional[User]]:
        """
        Register a new user.
        
        Args:
            username: Username for the new user
            email: Email address for the new user
            password: Password for the new user
            
        Returns:
            Tuple of (success, message, user_object)
        """
        # Input validation
        username = username.strip()
        email = email.strip()
        
        if not username or not email or not password:
            return False, "All fields are required", None
        
        # Create user object for validation
        user = User(username, email, password)
        
        if not user.validate_username():
            return False, "Username must be at least 3 characters", None
        
        if not user.validate_email():
            return False, "Please enter a valid email address", None
        
        if not user.validate_password(password):
            return False, "Password must be at least 6 characters", None
        
        # Check if user already exists
        if self.data_service.user_exists(username):
            return False, "Username already exists", None
        
        if self.data_service.email_exists(email):
            return False, "Email already exists", None
        
        # Save user
        users = self.data_service.load_users()
        users[username] = user
        
        if self.data_service.save_users(users):
            return True, "Registration successful", user
        else:
            return False, "Failed to save user data", None
    
    def login_user(self, username: str, password: str) -> Tuple[bool, str, Optional[User]]:
        """
        Authenticate user login.
        
        Args:
            username: Username for login
            password: Password for login
            
        Returns:
            Tuple of (success, message, user_object)
        """
        username = username.strip()
        
        if not username or not password:
            return False, "Username and password are required", None
        
        # Load users and check credentials
        users = self.data_service.load_users()
        
        if username not in users:
            return False, "Invalid username or password", None
        
        user = users[username]
        
        if not user.check_password(password):
            return False, "Invalid username or password", None
        
        return True, "Login successful", user
    
    def create_session(self, user: User) -> None:
        """
        Create user session.
        
        Args:
            user: User object to create session for
        """
        session['user_id'] = user.user_id
        session['username'] = user.username
    
    def destroy_session(self) -> None:
        """Destroy user session."""
        session.clear()
    
    def get_current_user_id(self) -> Optional[str]:
        """Get current user ID from session."""
        return session.get('user_id')
    
    def get_current_username(self) -> Optional[str]:
        """Get current username from session."""
        return session.get('username')
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated."""
        return 'user_id' in session
    
    def require_authentication(self) -> Tuple[bool, str]:
        """
        Check if user is authenticated and return appropriate response.
        
        Returns:
            Tuple of (is_authenticated, error_message)
        """
        if not self.is_authenticated():
            return False, "Authentication required"
        return True, ""
    
    def get_current_user(self) -> Optional[User]:
        """
        Get current user object from session.
        
        Returns:
            User object if authenticated, None otherwise
        """
        username = self.get_current_username()
        if not username:
            return None
        
        users = self.data_service.load_users()
        return users.get(username)
