from flask import Blueprint, render_template

main = Blueprint('main', __name__)

#@main.route('/index')
#
#def index():
#    return 'Hello World'

@main.route('/')#homepage
def home():
    return render_template('home.html')

@main.route('/profile')
def profile():
    return render_template('profile.html')