// main.js — students will add JavaScript here as features are built

// Registration form validation
document.addEventListener("DOMContentLoaded", function() {
    const registerForm = document.querySelector('form[method="POST"][action="/register"]');

    if (registerForm) {
        const passwordInput = registerForm.querySelector('input[name="password"]');
        const confirmPasswordInput = registerForm.querySelector('input[name="confirm_password"]');
        const submitButton = registerForm.querySelector('button[type="submit"]');

        // Real-time password match validation
        function checkPasswordMatch() {
            if (confirmPasswordInput.value && passwordInput.value !== confirmPasswordInput.value) {
                confirmPasswordInput.setCustomValidity("Passwords do not match");
            } else {
                confirmPasswordInput.setCustomValidity("");
            }
        }

        passwordInput.addEventListener("input", checkPasswordMatch);
        confirmPasswordInput.addEventListener("input", checkPasswordMatch);

        // Prevent form submission if passwords don't match
        registerForm.addEventListener("submit", function(e) {
            if (passwordInput.value !== confirmPasswordInput.value) {
                e.preventDefault();
                confirmPasswordInput.setCustomValidity("Passwords do not match");
                confirmPasswordInput.reportValidity();
            }
        });
    }

    // Date filter validation for profile page
    const dateFilterForm = document.querySelector('.date-filter-form');

    if (dateFilterForm) {
        const dateFromInput = dateFilterForm.querySelector('input[name="date_from"]');
        const dateToInput = dateFilterForm.querySelector('input[name="date_to"]');

        // Validate date range on change
        function validateDateRange() {
            if (dateFromInput.value && dateToInput.value) {
                if (dateFromInput.value > dateToInput.value) {
                    dateToInput.setCustomValidity("End date must be after start date");
                } else {
                    dateToInput.setCustomValidity("");
                }
            } else {
                dateToInput.setCustomValidity("");
            }
        }

        dateFromInput.addEventListener("change", validateDateRange);
        dateToInput.addEventListener("change", validateDateRange);

        // Prevent form submission if date range is invalid
        dateFilterForm.addEventListener("submit", function(e) {
            if (dateFromInput.value && dateToInput.value && dateFromInput.value > dateToInput.value) {
                e.preventDefault();
                dateToInput.setCustomValidity("End date must be after start date");
                dateToInput.reportValidity();
            }
        });
    }
});
