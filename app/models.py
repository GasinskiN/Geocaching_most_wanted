from . import db
from flask_login import UserMixin

#Tabele asocjacyjne

user_bridge_association = db.Table(
    'user_bridge', db.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')),
    db.Column('bridge_id', db.Integer, db.ForeignKey('bridge.bridge_id'))
)


user_achievement_association = db.Table(
    'user_achievement', db.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')),
    db.Column('achievement_id', db.Integer, db.ForeignKey('achievement.achievement_id'))
)

#Mapowanie tabel bazy danych na objekty python wyokrzystując SQLAlchemy

#UserMixin pozwala na zapamiętywanie użytkowniknika w bazie na podstawie cookies sesji

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    points = db.Column(db.Integer, default=0)

    visited_bridges = db.relationship('Bridge', secondary=user_bridge_association, back_populates='user')
    comments = db.relationship('Comment', back_populates='user')
    achievements = db.relationship('Achievement', secondary=user_achievement_association, back_populates='user')

class Bridge(db.Model):
    __tablename__ = 'bridge'
    bridge_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200))
    image_path = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    users = db.relationship('User', secondary=user_bridge_association, back_populates='visited_bridges')

class Comment(db.Model):
    __tablename__ = 'comment'
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    bridge_id = db.Column(db.Integer, db.ForeignKey('bridge.bridge_id'), nullable=False)
    text = db.Column(db.String, nullable=False)
    like_count = db.Column(db.Integer, default=0)
    dislike_count = db.Column(db.Integer, default=0)

    user = db.relationship('User', back_populates='comments')
    bridge = db.relationship('Bridge')

class Achievement(db.Model):
    __tablename__ = 'achievement'
    achievement_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    
    users = db.relationship('User', secondary=user_achievement_association, back_populates='achievements')
