from flask import Blueprint, render_template, request, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db
from flasgger import swag_from

auth = Blueprint('auth', __name__)


@auth.route('/register')
@swag_from({
    'responses': {
        200: {
            'description': 'Register page',
            'content': {
                'text/html': {
                    'example': '<html>Register Page</html>'
                }
            }
        }
    }
})
def register():
    return render_template('register.html')

@auth.route('/register', methods=['POST'])
@swag_from({
    'responses': {
        302: {
            'description': 'Redirect to login page on success'
        }
    },
    'parameters': [
        {
            'name': 'username',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Username for the new user'
        },
        {
            'name': 'password',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Password for the new user'
        }
    ]
})
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
@swag_from({
    'responses': {
        200: {
            'description': 'Login page',
            'content': {
                'text/html': {
                    'example': '<html>Login Page</html>'
                }
            }
        }
    }
})
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
@swag_from({
    'responses': {
        302: {
            'description': 'Redirect to profile page on success or back to login on failure'
        }
    },
    'parameters': [
        {
            'name': 'username',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Username of the user'
        },
        {
            'name': 'password',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Password of the user'
        },
        {
            'name': 'remember',
            'in': 'formData',
            'type': 'boolean',
            'required': False,
            'description': 'Remember me option'
        }
    ]
})
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
@swag_from({
    'responses': {
        302: {
            'description': 'Redirect to login page after logout'
        }
    }
})
def logout():
    logout_user()
    return redirect(url_for('auth.login'))