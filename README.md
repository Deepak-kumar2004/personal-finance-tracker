# Personal Finance Tracker - Modular Architecture

A modern, multi-user web application for tracking personal finances with support for multiple currencies, budgets, and comprehensive financial analytics. Built with Flask using a modular architecture following the Single Responsibility Principle (SRP).

## 🚀 Features

### Core Functionality
- **Multi-user Support**: Individual user accounts with secure authentication
- **Transaction Management**: Add, edit, and delete income/expense transactions
- **Category Management**: Customize transaction categories for better organization
- **Multi-currency Support**: 17+ currencies with flag emojis and symbols
- **Budget Tracking**: Set monthly budgets and track spending against limits
- **Financial Analytics**: Visual charts and statistics for spending patterns

### User Experience
- **Modern UI**: Clean, responsive design with dark/light theme support
- **Real-time Updates**: Instant balance and summary calculations
- **Mobile Friendly**: Responsive design works on all devices
- **Intuitive Navigation**: Easy-to-use interface with clear visual feedback

### Technical Features
- **Modular Architecture**: Clean, maintainable code structure following SRP
- **Separation of Concerns**: Models, Services, Routes, and Utils layers
- **Dependency Injection**: Services injected into route handlers
- **Error Handling**: Robust error handling with user-friendly messages
- **Data Security**: Password hashing and session management
- **RESTful API**: Well-structured API endpoints for all operations
- **Environment Configuration**: Production-ready configuration management

## 🏗️ Architecture

The application follows a clean, modular architecture with clear separation of concerns. For detailed information about the project structure, design principles, and class responsibilities, see [ARCHITECTURE.md](ARCHITECTURE.md).

**Key Benefits:**
- **Single Responsibility Principle (SRP)**: Each class has one clear responsibility
- **Maintainable Code**: Clean separation between models, services, and routes
- **Testable Design**: Dependency injection enables easy unit testing
- **Scalable Structure**: Easy to extend with new features

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Quick Start

**Option 1: Automated Setup (Recommended)**
```bash
git clone <repository-url>
cd personal-finance-tracker
./setup.sh
```

**Option 2: Manual Setup**

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd personal-finance-tracker
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   # Or for development: pip install -e .[dev]
   ```

4. **Set up environment variables (optional):**
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

**Option 3: Using Make (if available)**
```bash
make setup  # Sets up everything
make run    # Starts the application
```

### Running the Application

5. **Run the application:**
   
   **Option A: New Modular Architecture (Recommended)**
   ```bash
   python run.py
   # Or: make run
   # Or: finance-tracker (if installed with pip install -e .)
   ```
   
   **Option B: Using Virtual Environment**
   ```bash
   .venv/bin/python run.py
   ```
   
   **Option C: Legacy Monolithic Version**
   ```bash
   python app.py
   ```

6. **Open your browser and navigate to:**
   ```
   http://localhost:5000
   ```

## Usage

1. **Add a Transaction:**
   - Fill in the description, amount, type (income/expense), and category
   - Click "Add Transaction"

2. **View Transactions:**
   - See all transactions in the "Recent Transactions" section
   - Use filter buttons to show only income or expenses
   - Delete transactions by clicking the trash icon

3. **Monitor Your Finances:**
   - Check your current balance in the dashboard
   - View total income and expenses
   - Analyze spending by category in the statistics section

## 📁 Project Structure Details

### Models Layer
- **`User`**: User data representation and validation
- **`Transaction`**: Transaction data and validation
- **`TransactionSummary`**: Transaction calculations and statistics  
- **`CategoryManager`**: Category management operations
- **`UserSettings`**: User preferences management
- **`BudgetManager`**: Budget operations

### Services Layer
- **`DataService`**: File-based data persistence (JSON operations)
- **`AuthService`**: User authentication and session management
- **`TransactionService`**: Transaction business logic
- **`UserService`**: User settings, categories, and budgets business logic

### Routes Layer
- **`AuthRoutes`**: Authentication endpoints (login, register, logout)
- **`MainRoutes`**: Web page endpoints (dashboard)
- **`TransactionRoutes`**: Transaction API endpoints
- **`UserRoutes`**: User management API endpoints

### Utils Layer
- **`auth_decorators`**: Authentication decorators
- **`currency_utils`**: Currency formatting functions
- **`response_utils`**: Standardized API response helpers

## 🔧 Configuration

The application supports environment-based configuration:

```bash
# .env file
FLASK_ENV=development
SECRET_KEY=your-very-secure-secret-key
DEBUG=True
HOST=0.0.0.0
PORT=5000
USERS_FILE=users.json
DATA_DIR=user_data
```

## 🧪 Development

### Quick Development Setup
```bash
# Automated setup with development dependencies
./setup.sh
pip install -e .[dev]

# Or using Make
make setup
make install-dev
```

### Development Tools
```bash
# Code formatting
make format          # Format code with black
make check-format    # Check formatting

# Code quality
make lint           # Run flake8 linting
make type-check     # Run mypy type checking
make all-checks     # Run all quality checks

# Running the app
make run            # Start the application
make clean          # Clean up temporary files
```

### Adding New Features
1. **Models**: Add new data models in `app/models/`
2. **Services**: Add business logic in `app/services/`
3. **Routes**: Add new endpoints in `app/routes/`
4. **Utils**: Add helper functions in `app/utils/`

### Testing
The modular structure makes it easy to:
- Unit test individual components
- Mock dependencies
- Test business logic separately from HTTP handling

*Note: Comprehensive testing framework is planned for future development.*

## API Endpoints

### Authentication
- `GET /` - Home page (redirects to dashboard if authenticated)
- `GET /register` - Registration page
- `POST /register` - User registration
- `GET /login` - Login page
- `POST /login` - User authentication
- `GET /logout` - User logout

### Dashboard
- `GET /dashboard` - User dashboard (requires authentication)

### Transactions API
- `GET /api/transactions` - Get all transactions with summary
- `POST /api/transactions` - Add a new transaction
- `DELETE /api/transactions/{id}` - Delete a transaction
- `GET /api/stats` - Get financial statistics

### Categories API
- `GET /api/categories` - Get user categories
- `POST /api/categories` - Add new category
- `DELETE /api/categories/{type}/{name}` - Delete category

### Settings API
- `GET /api/settings` - Get user settings
- `POST /api/settings` - Update user settings

### Budgets API
- `GET /api/budgets` - Get user budgets
- `POST /api/budgets` - Set monthly budget
- `DELETE /api/budgets/{month}` - Delete budget

### Utilities
- `GET /api/currencies` - Get supported currencies (public)

## Technologies Used

- **Backend**: Python Flask with modular architecture
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Storage**: JSON file-based persistence
- **Icons**: Font Awesome
- **Styling**: Custom CSS with gradients and animations
- **Architecture**: Factory Pattern, Dependency Injection, SRP
- **Security**: Password hashing, session management, environment variables

## 🚀 Key Improvements in Modular Version

1. **Single Responsibility Principle**: Each class has one clear responsibility
2. **Maintainability**: Easy to add new features and modify existing ones
3. **Testability**: Components can be tested in isolation
4. **Security**: Enhanced security with environment-based configuration
5. **Scalability**: Easy to extend with new services and features
6. **Code Organization**: Clear separation of concerns across layers

## 📚 Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Detailed modular architecture, design principles, and class responsibilities
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines, coding standards, and development workflow

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on:
- Development setup
- Code style and standards  
- Pull request process
- Bug reporting and feature requests

Quick start:
1. Fork the repository
2. Create a feature branch
3. Follow the modular architecture patterns
4. Submit a pull request

## License

This project is open source and available under the MIT License.
