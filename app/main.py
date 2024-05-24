from flask import Blueprint, render_template, request
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
@login_required
def gameplay():
    # tymczasowy template w ramach testu działania
    return render_template('gameplay_test.html')

# Powinno być post na baze danych ale w ramach testu czy działa daje na ten sam url post
@main.route('/forum', methods = ['POST', 'GET'])
def forum():
    comment = {'key1':'geeks', 'key2':'for'} 
    if request.method == 'POST':
        comment = request.form
        return render_template('forum.html', comment = comment)
    if request.method == "GET":
        return render_template('forum.html', comment = comment)


@main.errorhandler(404)
def page_not_found(e):
    return render_template("error.html")

@main.route('/commentReply',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        response = request.form
    #   respnse jest przekazywane do html
    return render_template("test.html", response = response)