
from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user, login_required
from .models import db, Comment, Bridge, User
from flasgger import swag_from

main = Blueprint('main', __name__)


@main.route('/')
def display_home():
    return render_template('homepage.html')

@main.route('/profile', methods=['GET'])
@login_required
def display_profile():
    return render_template("profile.html")

@main.route('/api/profile/user', methods=['POST'])
@login_required
def get_uesr_profile():
    user = User.query.filter_by(user_id=current_user.user_id).first()
    payload = {
        'username': user.username,
        'points': user.points,
        'visited_bridges': user.visited_bridges,
        'achievements': user.achievements
    }
    return jsonify(payload),200

@main.route('/leaderboard')
def display_leaderboard():
    return render_template('leaderboard.html')

@main.route('/api/leaderboard')
def get_users_sorte_by_points():
    users = User.query.order_by(User.points).all()
    rank = 1
    payload= []
    for user in users:
        data = {
            'rank': rank,
            'username': user.username,
            'points': user.points
        }
        payload.append(data)
        rank += 1
    return jsonify(payload), 200

@main.errorhandler(404)
def page_not_found(e):
    return render_template("error.html")