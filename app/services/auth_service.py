from app import db
from app.models import User, UserSession
from flask import request, current_app
from datetime import datetime, timedelta, timezone
import re
import secrets
import string

class AuthService:
    """Service pour gérer l'authentification et les sessions"""
    
    @staticmethod
    def validate_email(email):
        """Valide le format de l'email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_password(password):
        """Valide la force du mot de passe"""
        if len(password) < 8:
            return False, "Le mot de passe doit contenir au moins 8 caractères"
        
        if not re.search(r'[A-Z]', password):
            return False, "Le mot de passe doit contenir au moins une majuscule"
        
        if not re.search(r'[a-z]', password):
            return False, "Le mot de passe doit contenir au moins une minuscule"
        
        if not re.search(r'\d', password):
            return False, "Le mot de passe doit contenir au moins un chiffre"
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Le mot de passe doit contenir au moins un caractère spécial"
        
        return True, "Mot de passe valide"
    
    @staticmethod
    def register_user(first_name, last_name, email, password):
        """Enregistre un nouvel utilisateur"""
        try:
            # Validation des données
            if not first_name or not last_name or not email or not password:
                return False, "Tous les champs sont requis"
            
            if not AuthService.validate_email(email):
                return False, "Format d'email invalide"
            
            is_valid, message = AuthService.validate_password(password)
            if not is_valid:
                return False, message
            
            # Vérifier si l'email existe déjà
            if User.query.filter_by(email=email).first():
                return False, "Cet email est déjà utilisé"
            
            # Créer l'utilisateur
            user = User(
                first_name=first_name.strip(),
                last_name=last_name.strip(),
                email=email.lower().strip(),
                password=password
            )
            
            db.session.add(user)
            db.session.commit()
            
            return True, "Compte créé avec succès"
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Erreur lors de l'inscription: {str(e)}")
            return False, "Erreur lors de la création du compte"
    
    @staticmethod
    def authenticate_user(email, password, remember_me=False):
        """Authentifie un utilisateur"""
        try:
            # Rechercher l'utilisateur
            user = User.query.filter_by(email=email.lower().strip()).first()
            
            if not user:
                return False, "Email ou mot de passe incorrect"
            
            if not user.is_active:
                return False, "Compte désactivé"
            
            if not user.check_password(password):
                return False, "Email ou mot de passe incorrect"
            
            # Mettre à jour la dernière connexion
            user.update_last_login()
            
            # Créer une session
            session = AuthService.create_session(user, remember_me)
            
            return True, user, session
            
        except Exception as e:
            current_app.logger.error(f"Erreur lors de l'authentification: {str(e)}")
            return False, "Erreur lors de l'authentification"
    
    @staticmethod
    def create_session(user, remember_me=False):
        """Crée une nouvelle session pour l'utilisateur"""
        try:
            # Nettoyer les sessions expirées
            UserSession.cleanup_expired_sessions()
            
            # Créer une nouvelle session
            session = UserSession(
                user_id=user.id,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent', '')
            )
            
            # Prolonger la session si "Se souvenir de moi" est activé
            if remember_me:
                session.extend_session(hours=30*24)  # 30 jours
            
            db.session.add(session)
            db.session.commit()
            
            return session
            
        except Exception as e:
            current_app.logger.error(f"Erreur lors de la création de session: {str(e)}")
            return None
    
    @staticmethod
    def get_session_by_id(session_id):
        """Récupère une session par son ID"""
        try:
            session = UserSession.query.filter_by(
                session_id=session_id,
                is_active=True
            ).first()
            
            if session and not session.is_expired():
                session.update_activity()
                return session
            
            return None
            
        except Exception as e:
            current_app.logger.error(f"Erreur lors de la récupération de session: {str(e)}")
            return None
    
    @staticmethod
    def logout_user(session_id):
        """Déconnecte un utilisateur"""
        try:
            session = UserSession.query.filter_by(session_id=session_id).first()
            if session:
                session.deactivate()
                return True
            
            return False
            
        except Exception as e:
            current_app.logger.error(f"Erreur lors de la déconnexion: {str(e)}")
            return False
    
    @staticmethod
    def generate_reset_token():
        """Génère un token de réinitialisation sécurisé"""
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(32))
    
    @staticmethod
    def cleanup_old_sessions():
        """Nettoie les anciennes sessions"""
        try:
            # Supprimer les sessions inactives depuis plus de 7 jours
            cutoff_date = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=7)
            old_sessions = UserSession.query.filter(
                getattr(UserSession, "last_activity") < cutoff_date
            ).all()
            
            for session in old_sessions:
                db.session.delete(session)
            
            db.session.commit()
            return len(old_sessions)
            
        except Exception as e:
            current_app.logger.error(f"Erreur lors du nettoyage des sessions: {str(e)}")
            return 0 