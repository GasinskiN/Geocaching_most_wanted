from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
    
def create_app():
    app = Flask(__name__,'/static')


    #inicjacja bazy danych
    app.config['SECRET_KEY'] = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mostwanted.db'

    db.init_app(app)
    
    from . import models

    with app.app_context():
        db.create_all()

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

    return app