# Personal Finance Tracker - Modular Architecture

## 🏗️ Project Structure

The application has been refactored into a modular architecture following the Single Responsibility Principle (SRP):

```
personal-finance-tracker/
├── run.py                          # Main entry point
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment configuration template
│
├── config/                         # Configuration Management
│   ├── __init__.py
│   └── settings.py                 # Application configuration classes
│
├── app/                           # Main application package
│   ├── __init__.py
│   ├── app_factory.py             # Flask application factory
│   │
│   ├── models/                    # Data Models (SRP: Data representation)
│   │   ├── __init__.py
│   │   ├── user.py                # User model and validation
│   │   ├── transaction.py         # Transaction model and calculations
│   │   ├── category.py            # Category management
│   │   └── settings.py            # User settings and budgets
│   │
│   ├── services/                  # Business Logic Layer (SRP: Business operations)
│   │   ├── __init__.py
│   │   ├── data_service.py        # Data persistence operations
│   │   ├── auth_service.py        # Authentication business logic
│   │   ├── transaction_service.py # Transaction business logic
│   │   └── user_service.py        # User management business logic
│   │
│   ├── routes/                    # Route Handlers (SRP: HTTP request handling)
│   │   ├── __init__.py
│   │   ├── auth_routes.py         # Authentication endpoints
│   │   ├── main_routes.py         # Web page endpoints
│   │   ├── transaction_routes.py  # Transaction API endpoints
│   │   └── user_routes.py         # User management API endpoints
│   │
│   └── utils/                     # Utility Functions (SRP: Helper functions)
│       ├── __init__.py
│       ├── auth_decorators.py     # Authentication decorators
│       ├── currency_utils.py      # Currency formatting utilities
│       └── response_utils.py      # API response helpers
│
├── templates/                     # HTML templates (unchanged)
├── static/                        # Static assets (unchanged)
├── user_data/                     # User data files (unchanged)
└── logs/                          # Application logs (unchanged)
```

## 📋 Classes and Responsibilities

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

### Configuration Layer
- **`Config`**: Base configuration class
- **`DevelopmentConfig`**: Development environment settings
- **`ProductionConfig`**: Production environment settings
- **`TestingConfig`**: Testing environment settings

## 🔄 How to Run

### 1. Using the new modular structure:
```bash
python run.py
```

### 2. Using the old monolithic file (backup):
```bash
python app.py
```

## 🧪 Key Improvements

### 1. **Single Responsibility Principle (SRP)**
- Each class has one clear responsibility
- Easy to test and maintain individual components

### 2. **Separation of Concerns**
- Models: Data representation and validation
- Services: Business logic
- Routes: HTTP handling
- Utils: Helper functions

### 3. **Dependency Injection**
- Services are injected into route handlers
- Easy to mock for testing
- Flexible configuration

### 4. **Error Handling**
- Centralized error handling in services
- Standardized API responses
- Better file operation error handling

### 5. **Configuration Management**
- Environment-based configuration
- Production-ready settings
- Secure secret key management

### 6. **Maintainability**
- Easy to add new features
- Clear module boundaries
- Reusable components

## 🔐 Security Improvements

1. **Environment Variables**: Secret key and sensitive config via environment
2. **Validation**: Comprehensive input validation in models
3. **Error Handling**: Secure error messages without exposing internals
4. **Session Management**: Proper session handling in auth service

## 🧪 Testing Ready

The modular structure makes it easy to:
- Unit test individual components
- Mock dependencies
- Test business logic separately from HTTP handling
- Integration testing with test configuration

## 📈 Future Extensibility

Easy to add:
- Database support (replace DataService)
- Email notifications (new service)
- API versioning (new route modules)
- Caching (new service layer)
- Logging (new utility module)
