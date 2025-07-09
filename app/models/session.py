from app import db
from datetime import datetime, timedelta
import uuid

class UserSession(db.Model):
    __tablename__ = 'user_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(36), unique=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ip_address = db.Column(db.String(45))  # IPv6 compatible
    user_agent = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super(UserSession, self).__init__(**kwargs)
        # Session expire après 24 heures par défaut
        if not self.expires_at:
            self.expires_at = datetime.utcnow() + timedelta(hours=24)
    
    def is_expired(self):
        """Vérifie si la session a expiré"""
        return datetime.utcnow() > self.expires_at
    
    def update_activity(self):
        """Met à jour la dernière activité"""
        self.last_activity = datetime.utcnow()
        db.session.commit()
    
    def extend_session(self, hours=24):
        """Prolonge la session"""
        self.expires_at = datetime.utcnow() + timedelta(hours=hours)
        self.update_activity()
    
    def deactivate(self):
        """Désactive la session"""
        self.is_active = False
        db.session.commit()
    
    @classmethod
    def cleanup_expired_sessions(cls):
        """Nettoie les sessions expirées"""
        expired_sessions = cls.query.filter(
            (cls.expires_at < datetime.utcnow()) | (cls.is_active == False)
        ).all()
        
        for session in expired_sessions:
            db.session.delete(session)
        
        db.session.commit()
        return len(expired_sessions)
    
    def __repr__(self):
        return f'<UserSession {self.session_id} for user {self.user_id}>' 