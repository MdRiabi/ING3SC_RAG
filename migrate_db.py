#!/usr/bin/env python3
"""
Script de migration de la base de données
Met à jour la structure de la base de données avec les nouveaux modèles
"""

from app import create_app, db
from app.models import User, UserSession

def migrate_database():
    """Migre la base de données vers la nouvelle structure"""
    app = create_app()
    
    with app.app_context():
        print(">>> Début de la migration de la base de données...")
        
        # Supprimer toutes les tables existantes
        print(">>> Suppression des tables existantes...")
        db.drop_all()
        
        # Créer toutes les nouvelles tables
        print(">>> Création des nouvelles tables...")
        db.create_all()
        
        print(">>> Migration terminée avec succès !")
        print(">>> Les tables suivantes ont été créées :")
        
        # Lister les tables créées
        inspector = db.inspect(db.engine)
        for table_name in inspector.get_table_names():
            print(f"  - {table_name}")
        
        # Créer un utilisateur de test
        print("\n>>> Création d'un utilisateur de test...")
        test_user = User(
            first_name="Admin",
            last_name="Test",
            email="admin@test.com",
            password="Admin123!"
        )
        test_user.is_verified = True
        test_user.is_active = True
        
        db.session.add(test_user)
        db.session.commit()
        
        print(">>> Utilisateur de test créé :")
        print(f"  - Email: admin@test.com")
        print(f"  - Mot de passe: Admin123!")
        print(f"  - Nom complet: {test_user.get_full_name()}")

if __name__ == '__main__':
    migrate_database() 