// ========================================
// FORM VALIDATION
// ========================================

// Email validation
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Password strength checker
function checkPasswordStrength(password) {
    let strength = 0;
    
    if (password.length >= 8) strength++;
    if (password.match(/[a-z]/)) strength++;
    if (password.match(/[A-Z]/)) strength++;
    if (password.match(/[0-9]/)) strength++;
    if (password.match(/[^a-zA-Z0-9]/)) strength++;
    
    return strength;
}

// Show password strength
function showPasswordStrength(input) {
    const strengthMeter = document.getElementById('password-strength');
    if (!strengthMeter) return;
    
    const strength = checkPasswordStrength(input.value);
    const colors = ['#ef4444', '#f59e0b', '#fbbf24', '#3b82f6', '#10b981'];
    const labels = ['Weak', 'Fair', 'Good', 'Strong', 'Excellent'];
    
    if (input.value.length > 0) {
        strengthMeter.style.display = 'block';
        strengthMeter.style.width = `${(strength / 5) * 100}%`;
        strengthMeter.style.backgroundColor = colors[strength - 1];
        strengthMeter.textContent = labels[strength - 1];
    } else {
        strengthMeter.style.display = 'none';
    }
}

// Username availability check
async function checkUsernameAvailability(username) {
    try {
        const response = await fetch(`/api/check-username?username=${username}`);
        const data = await response.json();
        return data.available;
    } catch (error) {
        console.error('Error checking username:', error);
        return true; // Assume available on error
    }
}

// Real-time form validation
document.addEventListener('DOMContentLoaded', function() {
    // Registration form validation
    const registerForm = document.querySelector('form[action*="/register"]');
    if (registerForm) {
        // Email validation
        const emailInput = registerForm.querySelector('input[name="email"]');
        if (emailInput) {
            emailInput.addEventListener('blur', function() {
                if (this.value && !validateEmail(this.value)) {
                    showError(this, 'Please enter a valid email address');
                } else {
                    clearError(this);
                }
            });
        }
        
        // Password validation
        const passwordInput = registerForm.querySelector('input[name="password"]');
        if (passwordInput) {
            passwordInput.addEventListener('input', function() {
                showPasswordStrength(this);
            });
            
            passwordInput.addEventListener('blur', function() {
                if (this.value.length < 8) {
                    showError(this, 'Password must be at least 8 characters');
                } else {
                    clearError(this);
                }
            });
        }
        
        // Confirm password validation
        const confirmPasswordInput = registerForm.querySelector('input[name="confirm_password"]');
        if (confirmPasswordInput && passwordInput) {
            confirmPasswordInput.addEventListener('blur', function() {
                if (this.value !== passwordInput.value) {
                    showError(this, 'Passwords do not match');
                } else {
                    clearError(this);
                }
            });
        }
        
        // Username validation
        const usernameInput = registerForm.querySelector('input[name="username"]');
        if (usernameInput) {
            usernameInput.addEventListener('blur', async function() {
                if (this.value.length < 3) {
                    showError(this, 'Username must be at least 3 characters');
                    return;
                }
                
                // Check availability
                const available = await checkUsernameAvailability(this.value);
                if (!available) {
                    showError(this, 'Username already taken');
                } else {
                    clearError(this);
                }
            });
        }
    }
    
    // Login form validation
    const loginForm = document.querySelector('form[action*="/login"]');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            const username = this.querySelector('input[name="username"]').value;
            const password = this.querySelector('input[name="password"]').value;
            
            if (!username || !password) {
                e.preventDefault();
                alert('Please fill in all fields');
            }
        });
    }
});

// Show error message
function showError(input, message) {
    // Remove existing error
    clearError(input);
    
    // Add error border
    input.style.borderColor = '#ef4444';
    
    // Create error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'form-error';
    errorDiv.style.color = '#ef4444';
    errorDiv.style.fontSize = '14px';
    errorDiv.style.marginTop = '5px';
    errorDiv.textContent = message;
    
    // Add to parent
    input.parentElement.appendChild(errorDiv);
}

// Clear error message
function clearError(input) {
    input.style.borderColor = '#e2e8f0';
    
    // Remove error message
    const errorDiv = input.parentElement.querySelector('.form-error');
    if (errorDiv) {
        errorDiv.remove();
    }
}

// Form submission with loading state
function showLoadingState(button) {
    button.disabled = true;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
}

function hideLoadingState(button, originalText) {
    button.disabled = false;
    button.innerHTML = originalText;
}

// Auto-focus first input on page load
document.addEventListener('DOMContentLoaded', function() {
    const firstInput = document.querySelector('input[autofocus], input[type="text"]:first-of-type');
    if (firstInput) {
        firstInput.focus();
    }
});