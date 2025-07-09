from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config.config import Config
from app.routes import main



db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    print(">>> Début de create_app")
    app = Flask(__name__)
    app.config.from_object(Config)
    print(">>> Flask et config OK")
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    print(">>> Extensions OK")
    
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.chat import chat_bp
    
    app.register_blueprint(main)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(chat_bp, url_prefix='/chat')
    print(">>> Blueprints enregistrés")
    
    # Create tables
    with app.app_context():
        db.create_all()
    print(">>> Tables créées")
    
    return app

from .models import User, UserSession  # adapte ce chemin selon ton projet

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    from flask import flash, redirect, url_for
    flash('Vous devez être connecté pour accéder à cette page.', 'warning')
    return redirect(url_for('auth.login'))