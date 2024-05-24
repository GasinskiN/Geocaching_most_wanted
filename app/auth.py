from flask import Blueprint, render_template, request, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/register')
def register():
    return render_template('register.html')

@auth.route('/register', methods=['POST'])
def register_post():
    username = request.form['username']
    password = request.form['password']
    #print(username, password)

    user = User.query.filter_by(username=username).first()

    if user:
        return render_template('error.html')

    #zapisywanie nowego użytkownika do bazy danych
    new_user = User(username=username, password=generate_password_hash(password, method='pbkdf2:sha256'))
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('main.login'))

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    
    #zapamiętywanie sesji użytkownika
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(username=username).first()

    #sprawdzanie credentiali
    if not user or not check_password_hash(user.password, password):
        #print(f"niepoprawne credentiale dla {user}")
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))