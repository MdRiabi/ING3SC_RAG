from flask import Blueprint, render_template, redirect, url_for, request, flash, make_response
from flask_login import login_user, logout_user, current_user, login_required
from app.services.auth_service import AuthService
from app.utils.decorators import login_required_custom, rate_limit
import json

# Déclaration unique du Blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
@rate_limit(max_requests=5, window=60)
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        email = data.get('email', '').strip()
        password = data.get('password', '')
        remember_me = data.get('remember_me', False)
        # Forcer remember_me à un booléen
        if isinstance(remember_me, str):
            remember_me = remember_me.lower() in ['true', 'on', '1', 'yes']
        else:
            remember_me = bool(remember_me)
        
        if not email or not password:
            flash('Email et mot de passe requis', 'error')
            return render_template('login.html')
        
        # Authentifier l'utilisateur
        result = AuthService.authenticate_user(email, password, remember_me)
        
        if isinstance(result, tuple) and len(result) == 3:
            success, user, session = result
        else:
            success, message = result
            user = session = None
        
        if success:
            login_user(user, remember=remember_me)
            # Créer une réponse avec le cookie de session
            response = make_response(redirect(url_for('main.index')))
            if session:
                response.set_cookie('session_id', session.session_id, max_age=30*24*60*60 if remember_me else 24*60*60)
            if user:
                flash(f'Bienvenue {user.get_full_name()} !', 'success')
            else:
                flash('Bienvenue !', 'success')
            return response
        else:
            flash(message, 'error')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
@rate_limit(max_requests=3, window=300)
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        first_name = data.get('firstName', '').strip()
        last_name = data.get('lastName', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        confirm_password = data.get('confirmPassword', '')
        
        # Validation côté serveur
        if not all([first_name, last_name, email, password, confirm_password]):
            flash('Tous les champs sont requis', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Les mots de passe ne correspondent pas', 'error')
            return render_template('register.html')
        
        # Enregistrer l'utilisateur
        success, message = AuthService.register_user(first_name, last_name, email, password)
        
        if success:
            flash(message, 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(message, 'error')
    
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required_custom
def logout():
    # Déconnecter la session
    session_id = request.cookies.get('session_id')
    if session_id:
        AuthService.logout_user(session_id)
    
    logout_user()
    
    # Supprimer le cookie de session
    response = make_response(redirect(url_for('main.index')))
    response.delete_cookie('session_id')
    
    flash('Vous avez été déconnecté avec succès', 'success')
    return response

@auth_bp.route('/profile')
@login_required_custom
def profile():
    return render_template('profile.html', user=current_user)

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required_custom
def change_password():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        current_password = data.get('currentPassword', '')
        new_password = data.get('newPassword', '')
        confirm_password = data.get('confirmPassword', '')
        
        if not current_user.check_password(current_password):
            flash('Mot de passe actuel incorrect', 'error')
            return render_template('change_password.html')
        
        if new_password != confirm_password:
            flash('Les nouveaux mots de passe ne correspondent pas', 'error')
            return render_template('change_password.html')
        
        is_valid, message = AuthService.validate_password(new_password)
        if not is_valid:
            flash(message, 'error')
            return render_template('change_password.html')
        
        current_user.set_password(new_password)
        flash('Mot de passe modifié avec succès', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('change_password.html')