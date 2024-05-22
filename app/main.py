from flask import Blueprint, render_template
from flask_login import current_user, login_required

main = Blueprint('main', __name__)

#@main.route('/index')
#
#def index():
#    return 'Hello World'

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.username)