from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user, login_required
from .models import db, Comment, Bridge, User
from flasgger import swag_from

main = Blueprint('main', __name__)


@main.route('/')
@swag_from({
    'responses': {
        200: {
            'description': 'Home page',
            'content': {
                'text/html': {
                    'example': '<html>Home Page</html>'
                }
            }
        }
    }
})
def home():
    return render_template('homepage.html')



# @main.route('/profile')
# #@login_required
# def profile():
#     bridges = [{ "bridge_id": "most_grunwaldzki",
#     "name": "Most Grunwaldzki",
#     "description": "Bardzo fajny most mi się podoba" ,
#     "image_path": "../static/public/most_grunwaldzki.jpg"
# }]
#     profile = "../static/public/Profile_img.jpg"
#     # return render_template('profile.html', name=current_user.username, profile=profile)
#     return render_template("profile.html",name=current_user.username, profile = profile, bridges = bridges, points = 8000)

@main.route('/profile', methods=['GET'])
@login_required
@swag_from({
    'responses': {
        200: {
            'description': 'User profile page',
            'content': {
                'text/html': {
                    'example': '<html>Profile Page</html>'
                }
            }
        }
    }
})
def profile():
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
@swag_from({
    'tages': ['view'],
    'responses': {
        200: {
            'description': 'Leaderboard page',
            'content': {
                'text/html': {
                    'example': '<html>Leaderboard Page</html>'
                }
            }
        }
    }
})
def leaderboard():
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

@main.route('/forum/<int:bridgeid>', methods=['GET'])
@login_required
def forum(bridgeid):
    return render_template('forum.html', bridgeid=bridgeid)

@main.route("/api/forum/bridges", methods=['POST'])
@login_required
def get_bridges_forum():
    if request.method == 'POST':
        bridges = Bridge.query.all()
        payload = []
        for bridge in bridges:
            bridge_data = {
                'name': bridge.name,
                'bridge_id': bridge.bridge_id
            }
            payload.append(bridge_data)
        return jsonify(payload), 200

@main.route("/api/forum/bridge/<int:bridgeid>", methods=['POST'])
@login_required
def get_bridge_forum(bridgeid):
    if request.method == 'POST':
        bridge = Bridge.query.filter_by(bridge_id=bridgeid).first()
        payload = {
            'name': bridge.name,
            'image_path': bridge.image_path,
            'description': bridge.description
        }
        return jsonify(payload), 200

@main.route("/api/forum/getcomments/<int:bridgeid>", methods=['POST'])
@login_required
def get_comments(bridgeid):
    if request.method == 'POST':
        comments = Comment.query.filter_by(bridge_id=bridgeid).all()
        payload = []
        for comment in comments:
            user = User.query.filter_by(user_id=comment.user_id).first()
            comment_data = {
                'text': comment.text,
                'username': user.username
            }
            payload.append(comment_data)
        return jsonify(payload), 200

@main.route("/api/forum/addcomment/<int:bridgeid>", methods=['POST'])
@login_required
def add_comment(bridgeid):
    if request.method == 'POST':
        comment_text = request.form.get('text')
        if comment_text:
            new_comment = Comment(
                user_id=current_user.user_id,
                bridge_id=bridgeid,
                text=comment_text
            )
            db.session.add(new_comment)
            db.session.commit()

            return jsonify({'message': "Comment added succesfully"}), 201
        else:
            return jsonify({'message': "Comment text can't be empty"}), 400



@main.errorhandler(404)
@swag_from({
    'responses': {
        404: {
            'description': 'Page not found',
            'content': {
                'text/html': {
                    'example': '<html>404 Error Page</html>'
                }
            }
        }
    }
})
def page_not_found(e):
    return render_template("error.html")