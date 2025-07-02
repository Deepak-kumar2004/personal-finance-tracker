from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime
import json
import os
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'  # Change this in production!

# Data files
USERS_FILE = 'users.json'
DATA_DIR = 'user_data'

# Ensure user_data directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Supported currencies with their symbols and flag emojis
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

# User management functions
def load_users():
    """Load users from JSON file"""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save users to JSON file"""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def get_user_data_path(user_id, filename):
    """Get the path for user-specific data file"""
    user_dir = os.path.join(DATA_DIR, user_id)
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    return os.path.join(user_dir, filename)

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

# User-specific data functions
def load_user_transactions(user_id):
    """Load transactions for a specific user"""
    file_path = get_user_data_path(user_id, 'transactions.json')
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return []

def save_user_transactions(user_id, transactions):
    """Save transactions for a specific user"""
    file_path = get_user_data_path(user_id, 'transactions.json')
    with open(file_path, 'w') as f:
        json.dump(transactions, f, indent=2)

def load_user_categories(user_id):
    """Load categories for a specific user"""
    default_categories = {
        'expense': ['Food', 'Transportation', 'Entertainment', 'Utilities', 
                   'Shopping', 'Healthcare', 'Education', 'Other'],
        'income': ['Salary', 'Freelance', 'Investment', 'Business', 'Other']
    }
    
    file_path = get_user_data_path(user_id, 'categories.json')
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    
    # Create default categories file for new user
    save_user_categories(user_id, default_categories)
    return default_categories

def save_user_categories(user_id, categories):
    """Save categories for a specific user"""
    file_path = get_user_data_path(user_id, 'categories.json')
    with open(file_path, 'w') as f:
        json.dump(categories, f, indent=2)

def load_user_settings(user_id):
    """Load settings for a specific user"""
    default_settings = {
        'currency': 'USD',
        'date_format': '%Y-%m-%d %H:%M:%S'
    }
    
    file_path = get_user_data_path(user_id, 'settings.json')
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    
    # Create default settings file for new user
    save_user_settings(user_id, default_settings)
    return default_settings

def save_user_settings(user_id, settings):
    """Save settings for a specific user"""
    file_path = get_user_data_path(user_id, 'settings.json')
    with open(file_path, 'w') as f:
        json.dump(settings, f, indent=2)

def load_user_budgets(user_id):
    """Load budgets for a specific user"""
    file_path = get_user_data_path(user_id, 'budgets.json')
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return {}

def save_user_budgets(user_id, budgets):
    """Save budgets for a specific user"""
    file_path = get_user_data_path(user_id, 'budgets.json')
    with open(file_path, 'w') as f:
        json.dump(budgets, f, indent=2)

def calculate_balance(transactions):
    """Calculate total balance from transactions"""
    balance = 0
    for transaction in transactions:
        if transaction['type'] == 'income':
            balance += transaction['amount']
        else:
            balance -= transaction['amount']
    return balance

def format_currency(amount, currency_code='USD'):
    """Format amount with currency symbol"""
    if currency_code in CURRENCIES:
        symbol = CURRENCIES[currency_code]['symbol']
        if currency_code in ['JPY', 'KRW']:  # No decimal places for these currencies
            return f"{symbol}{int(amount):,}"
        else:
            return f"{symbol}{amount:,.2f}"
    return f"{amount:.2f}"

# Authentication routes
@app.route('/')
def home():
    """Home page - show login/register or redirect to dashboard"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'GET':
        return render_template('register.html')
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    # Validation
    if not username or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400
    
    if len(username) < 3:
        return jsonify({'error': 'Username must be at least 3 characters'}), 400
    
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    # Check if user already exists
    users = load_users()
    if username in users or any(user.get('email') == email for user in users.values()):
        return jsonify({'error': 'Username or email already exists'}), 400
    
    # Create new user
    user_id = str(uuid.uuid4())
    users[username] = {
        'id': user_id,
        'email': email,
        'password': generate_password_hash(password),
        'created_at': datetime.now().isoformat()
    }
    
    save_users(users)
    
    # Log in the user
    session['user_id'] = user_id
    session['username'] = username
    
    return jsonify({'message': 'Registration successful', 'redirect': '/dashboard'}), 201

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'GET':
        return render_template('login.html')
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    # Check credentials
    users = load_users()
    if username not in users:
        return jsonify({'error': 'Invalid username or password'}), 401
    
    user = users[username]
    if not check_password_hash(user['password'], password):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    # Log in the user
    session['user_id'] = user['id']
    session['username'] = username
    
    return jsonify({'message': 'Login successful', 'redirect': '/dashboard'}), 200

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    return render_template('dashboard.html', username=session.get('username'))

# API routes (all require authentication)
@app.route('/api/transactions', methods=['GET'])
@login_required
def get_transactions():
    """Get all transactions for the current user"""
    user_id = session['user_id']
    transactions = load_user_transactions(user_id)
    settings = load_user_settings(user_id)
    currency = settings.get('currency', 'USD')
    balance = calculate_balance(transactions)
    
    # Calculate totals
    total_income = sum(t['amount'] for t in transactions if t['type'] == 'income')
    total_expenses = sum(t['amount'] for t in transactions if t['type'] == 'expense')
    
    return jsonify({
        'transactions': transactions,
        'balance': balance,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'currency': currency,
        'currency_symbol': CURRENCIES.get(currency, {}).get('symbol', '$')
    })

@app.route('/api/transactions', methods=['POST'])
@login_required
def add_transaction():
    """Add a new transaction for the current user"""
    user_id = session['user_id']
    data = request.get_json()
    
    # Validate input
    if not data or 'description' not in data or 'amount' not in data or 'type' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        amount = float(data['amount'])
        if amount <= 0:
            return jsonify({'error': 'Amount must be positive'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid amount'}), 400
    
    if data['type'] not in ['income', 'expense']:
        return jsonify({'error': 'Type must be income or expense'}), 400
    
    # Create new transaction
    transactions = load_user_transactions(user_id)
    transaction = {
        'id': len(transactions) + 1,
        'description': data['description'].strip(),
        'amount': amount,
        'type': data['type'],
        'category': data.get('category', 'Other'),
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Save transaction
    transactions.append(transaction)
    save_user_transactions(user_id, transactions)
    
    return jsonify({'message': 'Transaction added successfully', 'transaction': transaction}), 201

@app.route('/api/transactions/<int:transaction_id>', methods=['DELETE'])
@login_required
def delete_transaction(transaction_id):
    """Delete a transaction for the current user"""
    user_id = session['user_id']
    transactions = load_user_transactions(user_id)
    
    # Find and remove transaction
    transactions = [t for t in transactions if t['id'] != transaction_id]
    save_user_transactions(user_id, transactions)
    
    return jsonify({'message': 'Transaction deleted successfully'})

@app.route('/api/stats')
@login_required
def get_stats():
    """Get financial statistics for the current user"""
    user_id = session['user_id']
    transactions = load_user_transactions(user_id)
    
    # Calculate monthly stats
    monthly_stats = {}
    category_stats = {}
    
    for transaction in transactions:
        # Monthly stats
        date = datetime.strptime(transaction['date'], '%Y-%m-%d %H:%M:%S')
        month_key = date.strftime('%Y-%m')
        
        if month_key not in monthly_stats:
            monthly_stats[month_key] = {'income': 0, 'expenses': 0}
        
        if transaction['type'] == 'income':
            monthly_stats[month_key]['income'] += transaction['amount']
        else:
            monthly_stats[month_key]['expenses'] += transaction['amount']
        
        # Category stats (for expenses only)
        if transaction['type'] == 'expense':
            category = transaction.get('category', 'Other')
            category_stats[category] = category_stats.get(category, 0) + transaction['amount']
    
    return jsonify({
        'monthly_stats': monthly_stats,
        'category_stats': category_stats
    })

@app.route('/api/categories', methods=['GET'])
@login_required
def get_categories():
    """Get all categories for the current user"""
    user_id = session['user_id']
    categories = load_user_categories(user_id)
    return jsonify(categories)

@app.route('/api/categories', methods=['POST'])
@login_required
def add_category():
    """Add a new category for the current user"""
    user_id = session['user_id']
    data = request.get_json()
    
    # Validate input
    if not data or 'name' not in data or 'type' not in data:
        return jsonify({'error': 'Missing category name or type'}), 400
    
    category_name = data['name'].strip()
    category_type = data['type']
    
    if not category_name:
        return jsonify({'error': 'Category name cannot be empty'}), 400
    
    if category_type not in ['income', 'expense']:
        return jsonify({'error': 'Type must be income or expense'}), 400
    
    # Load existing categories
    categories = load_user_categories(user_id)
    
    # Check if category already exists
    if category_name in categories[category_type]:
        return jsonify({'error': 'Category already exists'}), 400
    
    # Add new category
    categories[category_type].append(category_name)
    save_user_categories(user_id, categories)
    
    return jsonify({'message': 'Category added successfully', 'category': category_name}), 201

@app.route('/api/categories/<category_type>/<category_name>', methods=['DELETE'])
@login_required
def delete_category(category_type, category_name):
    """Delete a category for the current user"""
    user_id = session['user_id']
    
    if category_type not in ['income', 'expense']:
        return jsonify({'error': 'Invalid category type'}), 400
    
    categories = load_user_categories(user_id)
    
    # Don't allow deletion of 'Other' category
    if category_name == 'Other':
        return jsonify({'error': 'Cannot delete Other category'}), 400
    
    # Remove category if it exists
    if category_name in categories[category_type]:
        categories[category_type].remove(category_name)
        save_user_categories(user_id, categories)
        
        # Update transactions that use this category to 'Other'
        transactions = load_user_transactions(user_id)
        for transaction in transactions:
            if transaction.get('category') == category_name:
                transaction['category'] = 'Other'
        save_user_transactions(user_id, transactions)
    
    return jsonify({'message': 'Category deleted successfully'})

@app.route('/api/currencies', methods=['GET'])
def get_currencies():
    """Get all supported currencies"""
    return jsonify(CURRENCIES)

@app.route('/api/settings', methods=['GET'])
@login_required
def get_settings():
    """Get user settings for the current user"""
    user_id = session['user_id']
    settings = load_user_settings(user_id)
    return jsonify(settings)

@app.route('/api/settings', methods=['POST'])
@login_required
def update_settings():
    """Update user settings for the current user"""
    user_id = session['user_id']
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    settings = load_user_settings(user_id)
    
    # Update currency if provided
    if 'currency' in data:
        currency = data['currency']
        if currency not in CURRENCIES:
            return jsonify({'error': 'Invalid currency code'}), 400
        settings['currency'] = currency
    
    # Update other settings as needed
    for key in ['date_format']:
        if key in data:
            settings[key] = data[key]
    
    save_user_settings(user_id, settings)
    
    return jsonify({'message': 'Settings updated successfully', 'settings': settings})

@app.route('/api/budgets', methods=['GET'])
@login_required
def get_budgets():
    """Get all budgets for the current user"""
    user_id = session['user_id']
    budgets = load_user_budgets(user_id)
    return jsonify(budgets)

@app.route('/api/budgets', methods=['POST'])
@login_required
def set_budget():
    """Set monthly budget for the current user"""
    user_id = session['user_id']
    data = request.get_json()
    
    # Validate input
    if not data or 'amount' not in data or 'month' not in data:
        return jsonify({'error': 'Missing budget amount or month'}), 400
    
    try:
        amount = float(data['amount'])
        if amount <= 0:
            return jsonify({'error': 'Budget amount must be positive'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid budget amount'}), 400
    
    month = data['month'].strip()
    if not month:
        return jsonify({'error': 'Month cannot be empty'}), 400
    
    # Load existing budgets
    budgets = load_user_budgets(user_id)
    
    # Set budget for the month
    budgets[month] = amount
    save_user_budgets(user_id, budgets)
    
    return jsonify({'message': 'Budget set successfully', 'month': month, 'amount': amount}), 201

@app.route('/api/budgets/<month>', methods=['DELETE'])
@login_required
def delete_budget(month):
    """Delete a monthly budget for the current user"""
    user_id = session['user_id']
    budgets = load_user_budgets(user_id)
    
    # Remove budget if it exists
    if month in budgets:
        del budgets[month]
        save_user_budgets(user_id, budgets)
    
    return jsonify({'message': 'Budget deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
