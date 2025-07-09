from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html', user=current_user)



@main.route('/login')
def login_redirect():
    return redirect(url_for('auth.login'))




@main.route('/signup')
def signup_redirect():
    return redirect(url_for('auth.register'))