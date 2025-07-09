
    function togglePassword(inputId, iconId) {
        const passwordInput = document.getElementById(inputId);
        const passwordIcon = document.getElementById(iconId);
        
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            passwordIcon.className = 'fas fa-eye-slash';
        } else {
            passwordInput.type = 'password';
            passwordIcon.className = 'fas fa-eye';
        }
    }

    function checkPasswordStrength(password) {
        let strength = 0;
        let text = '';
        let className = '';

        if (password.length >= 8) strength++;
        if (/[a-z]/.test(password)) strength++;
        if (/[A-Z]/.test(password)) strength++;
        if (/[0-9]/.test(password)) strength++;
        if (/[^A-Za-z0-9]/.test(password)) strength++;

        switch (strength) {
            case 0:
            case 1:
                text = 'Très faible';
                className = 'strength-weak';
                break;
            case 2:
                text = 'Faible';
                className = 'strength-weak';
                break;
            case 3:
                text = 'Moyen';
                className = 'strength-fair';
                break;
            case 4:
                text = 'Fort';
                className = 'strength-good';
                break;
            case 5:
                text = 'Très fort';
                className = 'strength-strong';
                break;
        }

        return { strength, text, className };
    }

    function validateForm() {
        let isValid = true;
        
        // Validation du prénom
        const firstName = document.getElementById('firstName').value;
        if (firstName.length < 2) {
            showError('firstNameError', 'Le prénom doit contenir au moins 2 caractères');
            isValid = false;
        } else {
            hideError('firstNameError');
        }

        // Validation du nom
        const lastName = document.getElementById('lastName').value;
        if (lastName.length < 2) {
            showError('lastNameError', 'Le nom doit contenir au moins 2 caractères');
            isValid = false;
        } else {
            hideError('lastNameError');
        }

        // Validation de l'email
        const email = document.getElementById('email').value;
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            showError('emailError', 'Veuillez saisir une adresse email valide');
            isValid = false;
        } else {
            hideError('emailError');
        }

        // Validation du mot de passe
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        
        if (password !== confirmPassword) {
            showError('confirmPasswordError', 'Les mots de passe ne correspondent pas');
            isValid = false;
        } else {
            hideError('confirmPasswordError');
        }

        return isValid;
    }

    function showError(elementId, message) {
        const element = document.getElementById(elementId);
        element.textContent = message;
        element.classList.add('show');
    }

    function hideError(elementId) {
        const element = document.getElementById(elementId);
        element.classList.remove('show');
    }

    function showTerms() {
        alert('Conditions d\'utilisation à implémenter');
    }

    function showPrivacy() {
        alert('Politique de confidentialité à implémenter');
    }

    function socialSignup(provider) {
        alert(`Inscription avec ${provider} à implémenter`);
    }

    // Event listeners
    document.getElementById('password').addEventListener('input', function() {
        const password = this.value;
        const result = checkPasswordStrength(password);
        
        const strengthFill = document.getElementById('strengthFill');
        const strengthText = document.getElementById('strengthText');
        
        strengthFill.className = `strength-fill ${result.className}`;
        strengthText.textContent = result.text;
    });

    document.getElementById('confirmPassword').addEventListener('input', function() {
        const password = document.getElementById('password').value;
        const confirmPassword = this.value;
        
        if (confirmPassword && password !== confirmPassword) {
            showError('confirmPasswordError', 'Les mots de passe ne correspondent pas');
        } else {
            hideError('confirmPasswordError');
        }
    });

    document.getElementById('signupForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (!validateForm()) {
            return;
        }
        
        const button = document.querySelector('.signup-button');
        const originalText = button.innerHTML;
        
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Création du compte...';
        button.disabled = true;
        
        // Simulation de l'inscription
        setTimeout(() => {
            button.innerHTML = originalText;
            button.disabled = false;
            
            // Ici vous pouvez ajouter la logique d'inscription réelle
            alert('Compte créé avec succès ! Vous pouvez maintenant vous connecter.');
            window.location.href = '/login';
        }, 2000);
    });

    // Animation des champs de saisie
    document.querySelectorAll('.form-control').forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.style.transform = 'scale(1.02)';
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.style.transform = 'scale(1)';
        });
    });
