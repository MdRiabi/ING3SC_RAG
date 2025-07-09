from functools import wraps
from flask import flash, redirect, url_for, request
from flask_login import current_user, login_required
from app.services.auth_service import AuthService

def login_required_custom(f):
    """Décorateur personnalisé pour vérifier l'authentification"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Vous devez être connecté pour accéder à cette page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Décorateur pour vérifier les droits d'administrateur"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Vous devez être connecté pour accéder à cette page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        
        # Vérifier si l'utilisateur est admin (à implémenter selon vos besoins)
        if not hasattr(current_user, 'is_admin') or not current_user.is_admin:
            flash('Accès refusé. Droits d\'administrateur requis.', 'error')
            return redirect(url_for('main.index'))
        
        return f(*args, **kwargs)
    return decorated_function

def verified_user_required(f):
    """Décorateur pour vérifier que l'utilisateur est vérifié"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Vous devez être connecté pour accéder à cette page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        
        if not current_user.is_verified:
            flash('Votre compte doit être vérifié pour accéder à cette fonctionnalité.', 'warning')
            return redirect(url_for('auth.verify_account'))
        
        return f(*args, **kwargs)
    return decorated_function

def active_user_required(f):
    """Décorateur pour vérifier que l'utilisateur est actif"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Vous devez être connecté pour accéder à cette page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        
        if not current_user.is_active:
            flash('Votre compte a été désactivé. Contactez l\'administrateur.', 'error')
            return redirect(url_for('auth.login'))
        
        return f(*args, **kwargs)
    return decorated_function

def rate_limit(max_requests=5, window=60):
    """Décorateur pour limiter le taux de requêtes"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Implémentation simple du rate limiting
            # En production, utilisez Redis ou une solution plus robuste
            client_ip = request.remote_addr
            # Ici vous pourriez vérifier le nombre de requêtes dans une fenêtre de temps
            # Pour l'instant, on laisse passer toutes les requêtes
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def validate_session(f):
    """Décorateur pour valider la session utilisateur"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            # Vérifier si la session est toujours valide
            session_id = request.cookies.get('session_id')
            if session_id:
                session = AuthService.get_session_by_id(session_id)
                if not session:
                    # Session invalide, déconnecter l'utilisateur
                    from flask_login import logout_user
                    logout_user()
                    flash('Votre session a expiré. Veuillez vous reconnecter.', 'warning')
                    return redirect(url_for('auth.login'))
        
        return f(*args, **kwargs)
    return decorated_function 