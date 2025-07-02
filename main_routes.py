"""
Main routes for Money Manager application
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from auth import AuthService
from models import UserModel
from config import Config
from exceptions import ValidationError, AuthenticationError
from logger import LoggerSetup


# Create main blueprint
main_bp = Blueprint('main', __name__)


class MainController:
    """Main Controller class to handle authentication and page routes"""
    
    def __init__(self, config: Config):
        self.config = config
        self.user_model = UserModel(config)
        self.auth_service = AuthService(self.user_model)
    
    def setup_routes(self, blueprint: Blueprint):
        """Setup all main routes"""
        blueprint.add_url_rule('/', 'home', self.home, methods=['GET'])
        blueprint.add_url_rule('/register', 'register', self.register, methods=['GET', 'POST'])
        blueprint.add_url_rule('/login', 'login', self.login, methods=['GET', 'POST'])
        blueprint.add_url_rule('/logout', 'logout', self.logout, methods=['GET'])
        blueprint.add_url_rule('/dashboard', 'dashboard', self.dashboard, methods=['GET'])
    
    def home(self):
        """Home page - show login/register or redirect to dashboard"""
        if 'user_id' in session:
            return redirect(url_for('main.dashboard'))
        return render_template('home.html')
    
    def register(self):
        """User registration"""
        if request.method == 'GET':
            return render_template('register.html')
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        try:
            # Register user
            result = self.auth_service.register_user(username, email, password)
            
            # Log in the user
            self.auth_service.create_session(result)
            return jsonify({
                'message': 'Registration successful', 
                'redirect': '/dashboard'
            }), 201
        except (ValidationError, AuthenticationError) as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': 'Registration failed'}), 500
    
    def login(self):
        """User login"""
        if request.method == 'GET':
            return render_template('login.html')
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        try:
            # Authenticate user
            result = self.auth_service.authenticate_user(username, password)
            
            # Create session
            self.auth_service.create_session(result)
            return jsonify({
                'message': 'Login successful', 
                'redirect': '/dashboard'
            }), 200
        except (ValidationError, AuthenticationError) as e:
            return jsonify({'error': str(e)}), 401
        except Exception as e:
            return jsonify({'error': 'Login failed'}), 500
    
    def logout(self):
        """User logout"""
        self.auth_service.clear_session()
        return redirect(url_for('main.home'))
    
    def dashboard(self):
        """User dashboard"""
        if 'user_id' not in session:
            return redirect(url_for('main.home'))
        
        return render_template('dashboard.html', username=session.get('username'))
