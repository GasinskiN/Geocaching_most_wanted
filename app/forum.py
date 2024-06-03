#Autor Krzysztof Orlikowski
from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user, login_required
from .models import db, Comment, Bridge, User
from flasgger import swag_from

forum = Blueprint('forum', __name__)

#Ścierzka do wywałania widoku forum dla odpowiedniego mostu
@forum.route('/forum/<int:bridgeid>', methods=['GET'])
@login_required
def display_forum(bridgeid):
    return render_template('forum.html', bridgeid=bridgeid)

#Punkty końcowe potrzebne do obsługi forum

#Zapytanie o dostępne mosty
@forum.route("/api/forum/bridges", methods=['POST'])
@swag_from({
    'tags': ['forum'],
    'responses': {
        200:
        {
            'description': 'Succesfully fetched list of available bridges',
            'content': {
                'application/json': {}
            }
        }
    },
})
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

#Zapytanie o nazwę, ścieżkę do icony oraz opis mostu według id
@forum.route("/api/forum/bridge/<int:bridgeid>", methods=['POST'])
@login_required
@swag_from({
    'tags': ['forum'],
    'responses': {
        200: 
        {
            'description': 'Succesfully fetched data of bridge',
            'content': {
                'application/json': {}
            }
        }
    },
    'parameters': [
        {
            'name': 'bridgeid',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Id of bridge to fetch'
        }
    ],
})
def get_bridge_forum(bridgeid):
    if request.method == 'POST':
        bridge = Bridge.query.filter_by(bridge_id=bridgeid).first()
        payload = {
            'name': bridge.name,
            'image_path': bridge.image_path,
            'description': bridge.description
        }
        return jsonify(payload), 200

#Zapytanie o wszystkie komentarze dla danego mostu
@forum.route("/api/forum/getcomments/<int:bridgeid>", methods=['POST'])
@login_required
@swag_from({
    'tags': ['forum'],
    'responses': {
        200:
        {
            'description': 'Succesfully fetched comments for a bridge',
            'content': {
                'application/json': {}
            }
        }
    },
    'parameters': [
        {
            'name': 'bridgeid',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Id of bridge for which to fetch comments'
        }
    ],
})
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

#Zapytanie dodające komentarz na forum mostu
@forum.route("/api/forum/addcomment/<int:bridgeid>", methods=['POST'])
@login_required
@swag_from({
    'tags': ['forum'],
    'responses': {
        200:
        {
            'description': 'Succesfully added comment',
            'content': {
                'application/json': {}
            }
        },
        400:
        {
            'description': 'Bad request, text field empty',
            'content': {
                'application/json': {}
            }
        }
    },
    'parameters': [
        {
            'name': 'bridgeid',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Id of bridge for which to add comment'
        },
        {
            'name': 'text',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Text of comment to add'
        }
    ]
})
def add_comment(bridgeid):
    if request.method == 'POST':
        comment_text = request.form.get('text')
        print(comment_text)
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