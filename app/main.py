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

@main.route('/profile')
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
    # Fetch the current user from the database
    user = User.query.get(current_user.get_id())
    
    # Get the count of visited bridges
    visited_bridges_count = len(user.visited_bridges)
    
    # Fetch the last 3 visited bridges
    last_three_bridges = user.visited_bridges[-3:]
    
    profile_img = "../static/public/Profile_img.jpg"

    achievements = [("Konto że hej", "../static/public/koty_za_ploty.png")]

     
    if visited_bridges_count > 1:
        achievements.append(("Pierwsze koty za płoty", "../static/public/koty_za_ploty.png"))
    
    if visited_bridges_count > 3:
        achievements.append(("Teraz już tylko z górki", "../static/public/koty_za_ploty.png"))

    if user.points > 9000:
        achievements.append(("Jest większe niż 9000", "../static/public/koty_za_ploty.png"))


    return render_template("profile.html", 
                           name=current_user.user_id, 
                           profile=profile_img, 
                           bridges=last_three_bridges, 
                           points=visited_bridges_count,
                           achievements=achievements
                           )

@main.route('/login')
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


@main.route('/register')
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



@main.route('/gameplay')
@login_required
@swag_from({
    'responses': {
        200: {
            'description': 'Gameplay page',
            'content': {
                'text/html': {
                    'example': '<html>Gameplay Page</html>'
                }
            }
        }
    }
})
def gameplay():
    # tymczasowy template w ramach testu działania
    return render_template('gameplay_page.html')

# Powinno być post na baze danych ale w ramach testu czy działa daje na ten sam url post
# @main.route('/forum/<bridgeid>', methods = ['POST', 'GET'])
# @login_required
# def forum(bridgeid):
#     comments = [{'text':'Komentarz pierwszy', 'username':'Pioter32'},{'text':'Fajny most', 'username':'Janusz'}]
#     image = "../static/public/"+ bridgeid +".jpg"
#     if request.method == 'POST':

#         # Tutaj klucz to jest text a value to jest to co jest napisane w komentarzu, trzeba by to połączyć z 
#         # nazwą użytkownika i dodać do bazy danych jakby co to można zobaczyć w konsoli
#         for key, value in request.form.items():
#             print(key, value)

#         return render_template('forum.html', comments = comments, image=image)
#     if request.method == "GET":
#         return render_template('forum.html', comments = comments, image=image)

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
def get_bridge_forum(bridegeid):
    if request.method == 'POST':
        bridge = Bridge.query.filter_by(bridge_id=bridegeid)
        payload = {
            'name': bridge.name,
            'image_path': bridge.image_path,
            'description': bridge.description
        }
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
                'user': user.username
            }
            payload.append(comment)
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