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

from .models import User  # adapte ce chemin selon ton projet

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))