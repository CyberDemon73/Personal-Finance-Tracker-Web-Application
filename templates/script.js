const signupForm = document.getElementById('signup-form');

signupForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    // Form field values
    const formData = getFormData();

    // Validation checks
    if (!areAllFieldsFilled(formData)) {
        displayMessage('Please fill in all required fields.', 'error');
        return;
    }

    if (!isPasswordMatching(formData.password, formData.confirmpassword)) {
        displayMessage('Passwords do not match.', 'error');
        return;
    }

    if (!isValidEmail(formData.email)) {
        displayMessage('Please enter a valid email address.', 'error');
        return;
    }

    if (!isValidPhone(formData.phone)) {
        displayMessage('Please enter a valid phone number.', 'error');
        return;
    }

    if (!isPasswordStrong(formData.password)) {
        displayMessage('Password should be at least 8 characters long and include a mix of letters, numbers, and symbols.', 'error');
        return;
    }

    // Checking email uniqueness asynchronously
    try {
        const isEmailUnique = await checkEmailUniqueness(formData.email);
        if (!isEmailUnique) {
            displayMessage('This email is already in use.', 'error');
            return;
        }

        displayMessage('Form is successfully validated. Submitting...', 'success');
        // Perform form submission or further processing here
        // signupForm.submit();
    } catch (error) {
        displayMessage('An error occurred during validation.', 'error');
    }
});

function getFormData() {
    return {
        firstname: document.getElementById('firstname').value,
        lastname: document.getElementById('lastname').value,
        email: document.getElementById('email').value,
        phone: document.getElementById('phone').value,
        gender: document.getElementById('gender').value,
        password: document.getElementById('password').value,
        confirmpassword: document.getElementById('confirmpassword').value
    };
}

function displayMessage(message, type) {
    const messageElement = document.getElementById('message');
    messageElement.textContent = message;
    messageElement.className = type === 'error' ? 'alert alert-danger' : 'alert alert-success';
    messageElement.style.display = 'block';
}

function areAllFieldsFilled(formData) {
    return Object.values(formData).every(value => value !== '');
}

function isPasswordMatching(password, confirmPassword) {
    return password === confirmPassword;
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function isValidPhone(phone) {
    const phoneRegex = /^\+?[1-9]\d{1,14}$/; // E.164 format
    return phoneRegex.test(phone);
}

function isPasswordStrong(password) {
    const strongPasswordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    return strongPasswordRegex.test(password);
}

async function checkEmailUniqueness(email) {
    // Simulated API request - replace with actual API call
    // Example: return await apiCallToCheckEmail(email);
    return new Promise(resolve => setTimeout(() => resolve(true), 1000)); // Mock async behavior
}
