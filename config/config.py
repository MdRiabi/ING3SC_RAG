import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///chatbot.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload configuration
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'app/static/uploads'
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16777216))
    
    # API Keys
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
    HUGGINGFACE_API_KEY = os.environ.get('HUGGINGFACE_API_KEY')
    
    # RAG Configuration
    EMBEDDING_MODEL = os.environ.get('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
    CHUNK_SIZE = int(os.environ.get('CHUNK_SIZE', 1000))
    CHUNK_OVERLAP = int(os.environ.get('CHUNK_OVERLAP', 200))
    
    # Supported languages
    SUPPORTED_LANGUAGES = ['fr', 'en']
    DEFAULT_LANGUAGE = 'fr'