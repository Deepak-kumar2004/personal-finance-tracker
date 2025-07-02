// Money Manager App JavaScript

class MoneyManager {
    constructor() {
        this.transactions = [];
        this.categories = { income: [], expense: [] };
        this.currencies = {};
        this.currentCurrency = 'USD';
        this.currencySymbol = '$';
        this.currentFilter = 'all';
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initializeTheme();
        this.loadCurrencies();
        this.loadSettings();
        this.loadCategories();
        this.loadTransactions();
        this.loadStats();
        this.loadBudgets();
        this.initializeBudgetForm();
    }

    setupEventListeners() {
        // Transaction form submission
        const form = document.getElementById('transaction-form');
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.addTransaction();
        });

        // Category form submission
        const categoryForm = document.getElementById('category-form');
        categoryForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.addCategory();
        });

        // Currency selection
        const currencySelect = document.getElementById('currency-select');
        currencySelect.addEventListener('change', (e) => {
            this.updateCurrency(e.target.value);
        });

        // Theme toggle
        const themeToggle = document.getElementById('theme-toggle');
        themeToggle.addEventListener('click', () => {
            this.toggleTheme();
        });

        // Budget form submission
        const budgetForm = document.getElementById('budget-form');
        if (budgetForm) {
            budgetForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.setBudget();
            });
        }

        // Filter buttons
        const filterButtons = document.querySelectorAll('.filter-btn');
        filterButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.setFilter(e.target.dataset.filter);
            });
        });

        // Type change event to update categories
        const typeSelect = document.getElementById('type');
        typeSelect.addEventListener('change', () => {
            this.updateCategoryOptions();
        });
    }

    updateCategoryOptions() {
        const type = document.getElementById('type').value;
        const categorySelect = document.getElementById('category');
        
        // Clear existing options
        categorySelect.innerHTML = '';
        
        if (type && this.categories[type]) {
            this.categories[type].forEach(category => {
                const option = document.createElement('option');
                option.value = category;
                option.textContent = category;
                categorySelect.appendChild(option);
            });
        }
    }

    async loadCategories() {
        try {
            this.showLoading(true);
            const response = await fetch('/api/categories');
            if (response.ok) {
                this.categories = await response.json();
                this.renderCategories();
            }
        } catch (error) {
            this.showError('Failed to load categories');
            console.error('Error loading categories:', error);
        } finally {
            this.showLoading(false);
        }
    }

    async addCategory() {
        const name = document.getElementById('new-category-name').value.trim();
        const type = document.getElementById('new-category-type').value;

        if (!name || !type) {
            this.showError('Please enter category name and select type');
            return;
        }

        try {
            this.showLoading(true);
            const response = await fetch('/api/categories', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name, type })
            });

            const data = await response.json();

            if (response.ok) {
                this.showSuccess('Category added successfully!');
                document.getElementById('category-form').reset();
                await this.loadCategories();
                this.updateCategoryOptions();
            } else {
                this.showError(data.error || 'Failed to add category');
            }
        } catch (error) {
            this.showError('Failed to add category');
            console.error('Error adding category:', error);
        } finally {
            this.showLoading(false);
        }
    }

    async deleteCategory(categoryName, categoryType) {
        if (categoryName === 'Other') {
            this.showError('Cannot delete Other category');
            return;
        }

        if (!confirm(`Are you sure you want to delete the "${categoryName}" category? Transactions using this category will be moved to "Other".`)) {
            return;
        }

        try {
            this.showLoading(true);
            const response = await fetch(`/api/categories/${categoryType}/${encodeURIComponent(categoryName)}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                this.showSuccess('Category deleted successfully!');
                await this.loadCategories();
                await this.loadTransactions();
                this.updateCategoryOptions();
            } else {
                const data = await response.json();
                this.showError(data.error || 'Failed to delete category');
            }
        } catch (error) {
            this.showError('Failed to delete category');
            console.error('Error deleting category:', error);
        } finally {
            this.showLoading(false);
        }
    }

    renderCategories() {
        const incomeContainer = document.getElementById('income-categories');
        const expenseContainer = document.getElementById('expense-categories');

        // Render income categories
        incomeContainer.innerHTML = '';
        this.categories.income.forEach(category => {
            const categoryElement = this.createCategoryElement(category, 'income');
            incomeContainer.appendChild(categoryElement);
        });

        // Render expense categories
        expenseContainer.innerHTML = '';
        this.categories.expense.forEach(category => {
            const categoryElement = this.createCategoryElement(category, 'expense');
            expenseContainer.appendChild(categoryElement);
        });
    }

    createCategoryElement(categoryName, categoryType) {
        const categoryDiv = document.createElement('div');
        categoryDiv.className = `category-item ${categoryType}`;
        
        const categoryText = document.createElement('span');
        categoryText.textContent = categoryName;
        
        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'category-delete';
        deleteBtn.innerHTML = '×';
        deleteBtn.title = 'Delete category';
        deleteBtn.disabled = categoryName === 'Other';
        deleteBtn.addEventListener('click', () => {
            this.deleteCategory(categoryName, categoryType);
        });

        categoryDiv.appendChild(categoryText);
        categoryDiv.appendChild(deleteBtn);
        
        return categoryDiv;
    }

    async loadTransactions() {
        try {
            console.log('Loading transactions...');
            this.showLoading(true);
            const response = await fetch('/api/transactions');
            console.log('Response status:', response.status);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('Transactions data:', data);
            
            this.transactions = data.transactions;
            this.currentCurrency = data.currency || 'USD';
            this.currencySymbol = data.currency_symbol || '$';
            
            this.updateSummary(data);
            this.renderTransactions();
            
            console.log('Transactions loaded successfully');
        } catch (error) {
            console.error('Error loading transactions:', error);
            this.showError('Failed to load transactions: ' + error.message);
        } finally {
            this.showLoading(false);
        }
    }

    async loadStats() {
        try {
            const response = await fetch('/api/stats');
            const data = await response.json();
            this.renderCategoryStats(data.category_stats);
        } catch (error) {
            console.error('Error loading stats:', error);
        }
    }

    async addTransaction() {
        const description = document.getElementById('description').value.trim();
        const amount = parseFloat(document.getElementById('amount').value);
        const type = document.getElementById('type').value;
        const category = document.getElementById('category').value;

        // Validation
        if (!description || !amount || !type) {
            this.showError('Please fill in all required fields');
            return;
        }

        if (amount <= 0) {
            this.showError('Amount must be greater than 0');
            return;
        }

        try {
            this.showLoading(true);
            
            const response = await fetch('/api/transactions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    description,
                    amount,
                    type,
                    category: category || 'Other'
                })
            });

            if (response.ok) {
                this.showSuccess('Transaction added successfully!');
                this.clearForm();
                await this.loadTransactions();
                await this.loadStats();
            } else {
                const error = await response.json();
                this.showError(error.error || 'Failed to add transaction');
            }
        } catch (error) {
            this.showError('Failed to add transaction');
            console.error('Error adding transaction:', error);
        } finally {
            this.showLoading(false);
        }
    }

    async deleteTransaction(id) {
        if (!confirm('Are you sure you want to delete this transaction?')) {
            return;
        }

        try {
            this.showLoading(true);
            
            const response = await fetch(`/api/transactions/${id}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                this.showSuccess('Transaction deleted successfully!');
                await this.loadTransactions();
                await this.loadStats();
            } else {
                this.showError('Failed to delete transaction');
            }
        } catch (error) {
            this.showError('Failed to delete transaction');
            console.error('Error deleting transaction:', error);
        } finally {
            this.showLoading(false);
        }
    }

    updateSummary(data) {
        document.getElementById('balance').textContent = this.formatCurrency(data.balance);
        document.getElementById('total-income').textContent = this.formatCurrency(data.total_income);
        document.getElementById('total-expenses').textContent = this.formatCurrency(data.total_expenses);

        // Update balance card color based on positive/negative
        const balanceCard = document.querySelector('.balance-card');
        if (data.balance >= 0) {
            balanceCard.style.borderLeft = '5px solid #4CAF50';
        } else {
            balanceCard.style.borderLeft = '5px solid #f44336';
        }
    }

    renderTransactions() {
        const container = document.getElementById('transactions-list');
        
        if (this.transactions.length === 0) {
            container.innerHTML = `
                <div style="text-align: center; padding: 40px; color: #666;">
                    <i class="fas fa-inbox" style="font-size: 3rem; margin-bottom: 15px; opacity: 0.5;"></i>
                    <p>No transactions yet. Add your first transaction above!</p>
                </div>
            `;
            return;
        }

        // Filter transactions
        let filteredTransactions = this.transactions;
        if (this.currentFilter !== 'all') {
            filteredTransactions = this.transactions.filter(t => t.type === this.currentFilter);
        }

        // Sort by date (newest first)
        filteredTransactions.sort((a, b) => new Date(b.date) - new Date(a.date));

        container.innerHTML = filteredTransactions.map(transaction => `
            <div class="transaction-item">
                <div class="transaction-info">
                    <div class="transaction-description">${this.escapeHtml(transaction.description)}</div>
                    <div class="transaction-meta">
                        <span><i class="fas fa-tag"></i> ${transaction.category}</span>
                        <span><i class="fas fa-calendar"></i> ${this.formatDate(transaction.date)}</span>
                    </div>
                </div>
                <div class="transaction-amount ${transaction.type}">
                    ${transaction.type === 'income' ? '+' : '-'}${this.formatCurrency(transaction.amount)}
                </div>
                <button class="delete-btn" onclick="app.deleteTransaction(${transaction.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `).join('');
    }

    renderCategoryStats(categoryStats) {
        const container = document.getElementById('category-stats');
        
        if (Object.keys(categoryStats).length === 0) {
            container.innerHTML = `
                <div style="text-align: center; padding: 20px; color: #666;">
                    <p>No expense categories yet</p>
                </div>
            `;
            return;
        }

        // Sort categories by amount (highest first)
        const sortedCategories = Object.entries(categoryStats)
            .sort(([,a], [,b]) => b - a);

        container.innerHTML = sortedCategories.map(([category, amount]) => `
            <div class="category-item">
                <span class="category-name">${category}</span>
                <span class="category-amount">${this.formatCurrency(amount)}</span>
            </div>
        `).join('');
    }

    setFilter(filter) {
        this.currentFilter = filter;
        
        // Update active button
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-filter="${filter}"]`).classList.add('active');
        
        this.renderTransactions();
    }

    clearForm() {
        document.getElementById('transaction-form').reset();
        document.getElementById('category').innerHTML = '<option value="Other">Other</option>';
    }

    async loadCurrencies() {
        try {
            const response = await fetch('/api/currencies');
            if (response.ok) {
                this.currencies = await response.json();
                this.populateCurrencySelect();
            }
        } catch (error) {
            console.error('Error loading currencies:', error);
        }
    }

    async loadSettings() {
        try {
            const response = await fetch('/api/settings');
            if (response.ok) {
                const settings = await response.json();
                this.currentCurrency = settings.currency || 'USD';
                this.currencySymbol = this.currencies[this.currentCurrency]?.symbol || '$';
                
                // Update currency select
                const currencySelect = document.getElementById('currency-select');
                if (currencySelect) {
                    currencySelect.value = this.currentCurrency;
                }
            }
        } catch (error) {
            console.error('Error loading settings:', error);
        }
    }

    populateCurrencySelect() {
        const currencySelect = document.getElementById('currency-select');
        currencySelect.innerHTML = '';
        
        Object.keys(this.currencies).forEach(code => {
            const currency = this.currencies[code];
            const option = document.createElement('option');
            option.value = code;
            // Format: 🇺🇸 USD ($) - US Dollar
            option.textContent = `${currency.flag || '💰'} ${code} (${currency.symbol}) - ${currency.name}`;
            currencySelect.appendChild(option);
        });
    }

    async updateCurrency(currencyCode) {
        if (!this.currencies[currencyCode]) return;

        try {
            this.showLoading(true);
            const response = await fetch('/api/settings', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ currency: currencyCode })
            });

            if (response.ok) {
                this.currentCurrency = currencyCode;
                this.currencySymbol = this.currencies[currencyCode].symbol;
                
                // Refresh the display
                await this.loadTransactions();
                this.showSuccess(`Currency changed to ${this.currencies[currencyCode].name}`);
            } else {
                const data = await response.json();
                this.showError(data.error || 'Failed to update currency');
            }
        } catch (error) {
            this.showError('Failed to update currency');
            console.error('Error updating currency:', error);
        } finally {
            this.showLoading(false);
        }
    }

    formatCurrency(amount) {
        if (this.currentCurrency === 'JPY' || this.currentCurrency === 'KRW') {
            return `${this.currencySymbol}${Math.round(amount).toLocaleString()}`;
        }
        return `${this.currencySymbol}${amount.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    }

    // Budget Management Methods
    async loadBudgets() {
        try {
            const response = await fetch('/api/budgets');
            if (response.ok) {
                this.budgets = await response.json();
                this.renderBudgetStatus();
            }
        } catch (error) {
            console.error('Error loading budgets:', error);
        }
    }

    async setBudget() {
        const amount = parseFloat(document.getElementById('budget-amount').value);
        const month = document.getElementById('budget-month').value;

        if (!amount || amount <= 0 || !month) {
            this.showError('Please fill in all budget fields with valid values');
            return;
        }

        try {
            this.showLoading(true);
            const response = await fetch('/api/budgets', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    amount: amount,
                    month: month
                })
            });

            const data = await response.json();

            if (response.ok) {
                this.showSuccess('Budget set successfully!');
                document.getElementById('budget-form').reset();
                this.initializeBudgetForm(); // Reset month to current
                await this.loadBudgets();
            } else {
                this.showError(data.error || 'Failed to set budget');
            }
        } catch (error) {
            this.showError('Failed to set budget');
            console.error('Error setting budget:', error);
        } finally {
            this.showLoading(false);
        }
    }

    async deleteBudget(month) {
        if (!confirm(`Are you sure you want to delete the budget for ${month}?`)) {
            return;
        }

        try {
            this.showLoading(true);
            const response = await fetch(`/api/budgets/${month}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                this.showSuccess('Budget deleted successfully!');
                await this.loadBudgets();
            } else {
                const data = await response.json();
                this.showError(data.error || 'Failed to delete budget');
            }
        } catch (error) {
            this.showError('Failed to delete budget');
            console.error('Error deleting budget:', error);
        } finally {
            this.showLoading(false);
        }
    }

    renderBudgetStatus() {
        const container = document.getElementById('budget-status');
        if (!container || !this.budgets) return;

        const currentMonth = new Date().toISOString().slice(0, 7); // YYYY-MM format
        const currentBudget = this.budgets[currentMonth];

        if (!currentBudget) {
            container.innerHTML = `
                <div style="text-align: center; padding: 20px; color: #666;">
                    <p>No budget set for this month</p>
                </div>
            `;
            return;
        }

        // Calculate total spending for current month
        let totalSpent = 0;
        this.transactions.forEach(transaction => {
            if (transaction.type === 'expense') {
                const transactionMonth = transaction.date.slice(0, 7);
                if (transactionMonth === currentMonth) {
                    totalSpent += transaction.amount;
                }
            }
        });

        const remaining = currentBudget - totalSpent;
        const percentage = (totalSpent / currentBudget) * 100;
        
        let statusClass = 'budget-good';
        if (percentage > 90) statusClass = 'budget-danger';
        else if (percentage > 75) statusClass = 'budget-warning';

        container.innerHTML = `
            <div class="budget-item ${statusClass}">
                <div class="budget-header">
                    <span class="budget-category">Monthly Budget (${currentMonth})</span>
                    <button class="budget-delete" onclick="app.deleteBudget('${currentMonth}')">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
                <div class="budget-progress">
                    <div class="budget-bar">
                        <div class="budget-fill" style="width: ${Math.min(percentage, 100)}%"></div>
                    </div>
                    <div class="budget-text">
                        ${this.formatCurrency(totalSpent)} / ${this.formatCurrency(currentBudget)}
                    </div>
                </div>
                <div class="budget-remaining">
                    ${remaining >= 0 ? 'Remaining: ' + this.formatCurrency(remaining) : 'Over budget: ' + this.formatCurrency(-remaining)}
                </div>
                <div class="budget-percentage">
                    ${percentage.toFixed(1)}% of budget used
                </div>
            </div>
        `;
    }

    initializeBudgetForm() {
        // Set default month to current month
        const monthInput = document.getElementById('budget-month');
        if (monthInput) {
            const currentMonth = new Date().toISOString().slice(0, 7);
            monthInput.value = currentMonth;
        }
    }

    // Theme Management Methods
    initializeTheme() {
        // Load saved theme from localStorage or default to light
        const savedTheme = localStorage.getItem('moneyManagerTheme') || 'light';
        this.setTheme(savedTheme);
    }

    toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        this.setTheme(newTheme);
    }

    setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('moneyManagerTheme', theme);
        
        // Update theme toggle icon
        const themeToggle = document.getElementById('theme-toggle');
        const icon = themeToggle.querySelector('i');
        
        if (theme === 'dark') {
            icon.className = 'fas fa-sun';
            themeToggle.title = 'Switch to light mode';
        } else {
            icon.className = 'fas fa-moon';
            themeToggle.title = 'Switch to dark mode';
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    }

    showLoading(show) {
        const loading = document.getElementById('loading');
        if (show) {
            loading.classList.remove('hidden');
        } else {
            loading.classList.add('hidden');
        }
    }

    showSuccess(message) {
        this.showMessage(message, 'success');
    }

    showError(message) {
        this.showMessage(message, 'error');
    }

    showMessage(message, type) {
        const messageEl = document.getElementById(`${type}-message`);
        const textEl = document.getElementById(`${type}-text`);
        
        textEl.textContent = message;
        messageEl.classList.remove('hidden');
        
        // Auto hide after 3 seconds
        setTimeout(() => {
            messageEl.classList.add('hidden');
        }, 3000);
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new MoneyManager();
});

// Add some keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to submit form
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const form = document.getElementById('transaction-form');
        if (document.activeElement.closest('#transaction-form')) {
            form.dispatchEvent(new Event('submit'));
        }
    }
});
