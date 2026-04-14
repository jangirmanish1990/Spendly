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
});
