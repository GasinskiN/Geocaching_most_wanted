from flask import Blueprint, render_template
from flask_login import current_user, login_required

main = Blueprint('main', __name__)

#@main.route('/index')
#
#def index():
#    return 'Hello World'

@main.route('/')
def home():
    return render_template('homepage.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.username)


@main.route('/login')
def login():
    return render_template('login.html')


@main.route('/register')
def register():
    return render_template('register.html')


@main.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')


@main.route('/gameplay')
def gameplay():
    return render_template('gameplay.html')


@main.route('/forum')
def forum():
    return render_template('forum.html')

@main.errorhandler(404)
def page_not_found(e):
    return render_template("error.html")