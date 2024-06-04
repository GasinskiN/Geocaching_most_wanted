
from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user, login_required
from .models import User
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
@swag_from({
    'tags': ['profile'],
    'responses': {
        200:
        {
            'description': 'Succesfully fetched data for user profile',
            'content': {
                'application/json': {}
            }
        }
    },
})
def get_user_profile():
    user = User.query.filter_by(user_id=current_user.user_id).first()
    bridges = []
    achievements = []
    for bridge in user.visited_bridges[-3:]:
        data = {
            'name': bridge.name,
            'image_path': bridge.image_path,
            'description': bridge.description
        }
        bridges.append(data)
    for achievement in user.achievements:
        data = {
            'name': achievement.name
        }
        achievements.append(data)
    payload = {
        'username': user.username,
        'points': user.points,
        'visited_bridges': bridges,
        'achievements': achievements
    }
    return jsonify(payload),200

@main.route('/leaderboard')
def display_leaderboard():
    return render_template('leaderboard.html')

@main.route('/api/leaderboard')
@swag_from({
    'tags': ['leaderboard'],
    'responses': {
        200:
        {
            'description': 'Succesfully fetched list of users sorted by rank',
            'content': {
                'application/json': {}
            }
        }
    },
})
def get_users_sorte_by_points():
    users = User.query.order_by(User.points).all()
    users.reverse()
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