from flask import Blueprint, render_template
from flask_login import current_user, login_required

main = Blueprint('main', __name__)

@main.route('/')
def dashboard():
    return render_template('dashboard.html', user=current_user)