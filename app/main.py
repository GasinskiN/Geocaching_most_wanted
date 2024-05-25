from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

main = Blueprint('main', __name__)

#@main.route('/index')
#
#def index():
#    return 'Hello World'


@main.route('/')
def home():
    return render_template('homepage.html')



@main.route('/profile')
# @login_required
def profile():
    bridges = [{ "bridge_id": "most_grunwaldzki",
    "name": "Most Grunwaldzki",
    "description": "Bardzo fajny most mi się podoba" ,
    "image_path": "../static/public/most_grunwaldzki.jpg"
}]
    profile = "../static/public/Profile_img.jpg"
    # return render_template('profile.html', name=current_user.username, profile=profile)
    return render_template("profile.html", profile = profile, bridges = bridges, points = 8000)

@main.route('/login')
def login():
    return render_template('login.html')


@main.route('/register')
def register():
    return render_template('register.html')


@main.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')


@main.route('/gameplay')
@login_required
def gameplay():
    # tymczasowy template w ramach testu działania
    return render_template('gameplay_test.html')

# Powinno być post na baze danych ale w ramach testu czy działa daje na ten sam url post
@main.route('/forum/<bridgeid>', methods = ['POST', 'GET'])
def forum(bridgeid):
    comments = [{'text':'Komentarz pierwszy', 'username':'Pioter32'},{'text':'Fajny most', 'username':'Janusz'}]
    image = "../static/public/"+ bridgeid +".jpg"
    if request.method == 'POST':

        # Tutaj klucz to jest text a value to jest to co jest napisane w komentarzu, trzeba by to połączyć z 
        # nazwą użytkownika i dodać do bazy danych jakby co to można zobaczyć w konsoli
        for key, value in request.form.items():
            print(key, value)

        return render_template('forum.html', comments = comments, image=image)
    if request.method == "GET":
        return render_template('forum.html', comments = comments, image=image)


@main.errorhandler(404)
def page_not_found(e):
    return render_template("error.html")

@main.route('/commentReply',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        response = request.form
    #   respnse jest przekazywane do html
    return render_template("test.html", response = response)