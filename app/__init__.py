from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flasgger import Swagger
from werkzeug.security import generate_password_hash


db = SQLAlchemy()


def create_admin_user():
    from .models import User
    admin_username = "admin@mostwanted.com"
    admin_password = "admin"

    existing_admin = User.query.filter_by(username=admin_username).first()
    if existing_admin:
        return

    admin_user = User(
        username=admin_username,
        password=generate_password_hash(admin_password, method='pbkdf2:sha256'),
        role='admin'
    )
    db.session.add(admin_user)
    db.session.commit()



def create_app():
    app = Flask(__name__,'/static')


    #inicjacja bazy danych
    app.config['SECRET_KEY'] = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mostwanted.db'

    db.init_app(app)
    
    from . import models

    with app.app_context():
        db.create_all()
        create_admin_user()

    #login manager - niezbędne do zachowywania sesji użytkownika
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' #<- wskazuje stronę logowania
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    #inicjuje kod z auth i main(???)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from .gameplay import gameplay_bp as gameplay_blueprint
    app.register_blueprint(gameplay_blueprint)
    
    from .admin import admin_bp as admin_blueprint
    app.register_blueprint(admin_blueprint)


    swagger = Swagger(app)
    
    return app

app = create_app()
