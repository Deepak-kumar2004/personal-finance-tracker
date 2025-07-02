# Money Manager - Personal Finance Tracking Application

A modern, multi-user web application for tracking personal finances with support for multiple currencies, budgets, and comprehensive financial analytics built with Flask, HTML, CSS, and JavaScript.

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
- **Modular Architecture**: Clean, maintainable code structure
- **Comprehensive Logging**: Detailed application and error logging
- **Error Handling**: Robust error handling with user-friendly messages
- **Data Security**: Password hashing and session management
- **RESTful API**: Well-structured API endpoints for all operations

## 🏗️ Architecture

### Backend Structure
```
app.py              # Main application entry point
├── config.py       # Configuration management
├── models.py       # Data models and database operations
├── auth.py         # Authentication services
├── main_routes.py  # Web page routes
├── api_routes.py   # API endpoints
├── utils.py        # Utility functions
├── exceptions.py   # Custom exception classes
└── logger.py       # Logging configuration
```
- 🔍 **Filter Transactions**: Filter by all, income, or expenses
- 📈 **Category Statistics**: View spending breakdown by category
- 💾 **Data Persistence**: All data is stored in a JSON file
- ✨ **Modern UI**: Clean and intuitive interface

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

3. **Open your browser and navigate to:**
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

## Project Structure

```
money-manager/
├── app.py              # Flask backend application
├── requirements.txt    # Python dependencies
├── transactions.json   # Data storage (created automatically)
├── templates/
│   └── index.html     # Main HTML template
└── static/
    ├── style.css      # CSS styles
    └── script.js      # JavaScript functionality
```

## API Endpoints

- `GET /` - Main dashboard page
- `GET /api/transactions` - Get all transactions with summary
- `POST /api/transactions` - Add a new transaction
- `DELETE /api/transactions/{id}` - Delete a transaction
- `GET /api/stats` - Get financial statistics

## Technologies Used

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Storage**: JSON file
- **Icons**: Font Awesome
- **Styling**: Custom CSS with gradients and animations

## License

This project is open source and available under the MIT License.
