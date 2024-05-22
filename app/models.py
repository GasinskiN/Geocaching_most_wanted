from . import db
from flask_login import UserMixin

#UserMixin pozwala na zapamiętywanie użytkowniknika w bazie na podstawie cookies sesji

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    #visited_bridges = db.relationship('Bridge', secondary='visited_bridges', backref='users')