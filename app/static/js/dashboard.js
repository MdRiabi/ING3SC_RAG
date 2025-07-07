
    function startNewChat() {
        // Ici vous pouvez implémenter la logique pour démarrer une nouvelle conversation
        alert('Fonctionnalité de chat à implémenter');
    }

    function viewHistory() {
        alert('Historique des conversations à implémenter');
    }

    function showHelp() {
        alert('Page d\'aide à implémenter');
    }

    function viewStats() {
        alert('Statistiques d\'utilisation à implémenter');
    }

    function shareApp() {
        if (navigator.share) {
            navigator.share({
                title: 'Chatbot Intelligent',
                text: 'Découvrez ce chatbot intelligent !',
                url: window.location.origin
            });
        } else {
            // Fallback pour les navigateurs qui ne supportent pas l'API Web Share
            const url = window.location.origin;
            navigator.clipboard.writeText(url).then(() => {
                alert('Lien copié dans le presse-papiers !');
            });
        }
    }

    // Animation au scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observer les cartes du tableau de bord
    document.querySelectorAll('.dashboard-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'all 0.6s ease';
        observer.observe(card);
    });
