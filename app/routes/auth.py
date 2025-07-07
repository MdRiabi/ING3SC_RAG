from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    return render_template('login.html')



@auth_bp.route('/login', endpoint='login_direct')
def login_direct():
    return redirect(url_for('auth.login'))