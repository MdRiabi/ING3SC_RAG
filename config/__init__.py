from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config.config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.chat import chat_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(chat_bp, url_prefix='/chat')
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app