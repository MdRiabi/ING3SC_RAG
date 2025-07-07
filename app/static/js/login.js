

    function togglePassword() {
        const passwordInput = document.getElementById('password');
        const passwordIcon = document.getElementById('passwordIcon');
        
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            passwordIcon.className = 'fas fa-eye-slash';
        } else {
            passwordInput.type = 'password';
            passwordIcon.className = 'fas fa-eye';
        }
    }

    function showForgotPassword() {
        alert('Fonctionnalité de récupération de mot de passe à implémenter');
    }

    function socialLogin(provider) {
        alert(`Connexion avec ${provider} à implémenter`);
    }

    // Animation du formulaire
    document.getElementById('loginForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const button = document.querySelector('.login-button');
        const originalText = button.innerHTML;
        
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Connexion...';
        button.disabled = true;
        
        // Simulation de la connexion
        setTimeout(() => {
            button.innerHTML = originalText;
            button.disabled = false;
            
            // Ici vous pouvez ajouter la logique de connexion réelle
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            if (email && password) {
                // Redirection vers le tableau de bord ou la page principale
                window.location.href = '/';
            }
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
