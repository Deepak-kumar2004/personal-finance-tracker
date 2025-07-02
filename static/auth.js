// Authentication JavaScript

class AuthManager {
    constructor() {
        this.init();
    }

    init() {
        this.setupTheme();
        this.setupEventListeners();
    }

    setupTheme() {
        const themeToggle = document.getElementById('theme-toggle');
        const savedTheme = localStorage.getItem('moneyManagerTheme') || 'light';
        
        // Set initial theme
        document.documentElement.setAttribute('data-theme', savedTheme);
        this.updateThemeIcon(savedTheme);
        
        if (themeToggle) {
            themeToggle.addEventListener('click', () => {
                const currentTheme = document.documentElement.getAttribute('data-theme');
                const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
                
                document.documentElement.setAttribute('data-theme', newTheme);
                localStorage.setItem('moneyManagerTheme', newTheme);
                this.updateThemeIcon(newTheme);
            });
        }
    }

    updateThemeIcon(theme) {
        const themeToggle = document.getElementById('theme-toggle');
        if (!themeToggle) return;
        
        const icon = themeToggle.querySelector('i');
        if (theme === 'dark') {
            icon.className = 'fas fa-sun';
            themeToggle.title = 'Switch to light mode';
        } else {
            icon.className = 'fas fa-moon';
            themeToggle.title = 'Switch to dark mode';
        }
    }

    setupEventListeners() {
        // Login form
        const loginForm = document.getElementById('login-form');
        if (loginForm) {
            loginForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleLogin();
            });
        }

        // Register form
        const registerForm = document.getElementById('register-form');
        if (registerForm) {
            registerForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleRegister();
            });

            // Password confirmation validation
            const password = document.getElementById('password');
            const confirmPassword = document.getElementById('confirm-password');
            
            if (password && confirmPassword) {
                confirmPassword.addEventListener('input', () => {
                    if (confirmPassword.value && password.value !== confirmPassword.value) {
                        confirmPassword.setCustomValidity('Passwords do not match');
                    } else {
                        confirmPassword.setCustomValidity('');
                    }
                });
            }
        }
    }

    async handleLogin() {
        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value;

        if (!username || !password) {
            this.showError('Please fill in all fields');
            return;
        }

        try {
            this.showLoading(true);
            
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();

            if (response.ok) {
                this.showSuccess('Login successful! Redirecting...');
                setTimeout(() => {
                    window.location.href = data.redirect || '/dashboard';
                }, 1000);
            } else {
                this.showError(data.error || 'Login failed');
            }
        } catch (error) {
            this.showError('Network error. Please try again.');
            console.error('Login error:', error);
        } finally {
            this.showLoading(false);
        }
    }

    async handleRegister() {
        const username = document.getElementById('username').value.trim();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm-password').value;

        // Validation
        if (!username || !email || !password || !confirmPassword) {
            this.showError('Please fill in all fields');
            return;
        }

        if (username.length < 3) {
            this.showError('Username must be at least 3 characters');
            return;
        }

        if (password.length < 6) {
            this.showError('Password must be at least 6 characters');
            return;
        }

        if (password !== confirmPassword) {
            this.showError('Passwords do not match');
            return;
        }

        // Email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            this.showError('Please enter a valid email address');
            return;
        }

        try {
            this.showLoading(true);
            
            const response = await fetch('/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, email, password })
            });

            const data = await response.json();

            if (response.ok) {
                this.showSuccess('Account created successfully! Redirecting...');
                setTimeout(() => {
                    window.location.href = data.redirect || '/dashboard';
                }, 1000);
            } else {
                this.showError(data.error || 'Registration failed');
            }
        } catch (error) {
            this.showError('Network error. Please try again.');
            console.error('Registration error:', error);
        } finally {
            this.showLoading(false);
        }
    }

    showLoading(show) {
        const loading = document.getElementById('loading');
        if (loading) {
            if (show) {
                loading.classList.remove('hidden');
            } else {
                loading.classList.add('hidden');
            }
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
        
        if (messageEl && textEl) {
            textEl.textContent = message;
            messageEl.classList.remove('hidden');
            
            // Auto hide after 5 seconds
            setTimeout(() => {
                messageEl.classList.add('hidden');
            }, 5000);
        }
    }
}

// Initialize auth manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new AuthManager();
});
