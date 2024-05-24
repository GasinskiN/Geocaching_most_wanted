from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from . import db
from .models import User, Bridge

# innna nazwa: gameplay_bp, bo był problem że się nazwy pokrywały
# ale dla auth i main nie ma tego problemu
gameplay_bp = Blueprint('gameplay', __name__)


def verify_user_location():
    # funkcja do sprawdzenia czy współrzędne użytkownika są zgodne z współrzędnymi wybranego mostu
    raise NotImplementedError

def update_user_bridges():
    # funkcja do aktualizacji listy odwiedzonych mostów przez użytkownika
    raise NotImplementedError


@gameplay_bp.route('/gameplay', methods = ['POST', 'GET'])
@login_required
def gameplay():
    if request.method == 'GET':
        return render_template('gameplay_test.html')
    
    if request.method == 'POST':
        bridge_name = request.form['bridgeName']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
