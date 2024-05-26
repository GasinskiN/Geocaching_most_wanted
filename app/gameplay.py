from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import User, Bridge,user_bridge_association
from datetime import datetime

# innna nazwa: gameplay_bp, bo był problem że się nazwy pokrywały
# ale dla auth i main nie ma tego problemu
gameplay_bp = Blueprint('gameplay', __name__)


def verify_user_location(selceted_bridge_name: str, user_latitude: float, user_longitude: float)->bool:
    # funkcja do sprawdzenia czy współrzędne użytkownika są zgodne z współrzędnymi wybranego mostu
    bridge = Bridge.query.filter_by(name=selceted_bridge_name).first()
    bridge_latitude = float(str(bridge.latitude)[:6])
    bridge_longitude = float(str(bridge.longitude)[:6])
    
    if bridge is None:
        return redirect(url_for('main.errorhandler'))
    
    latitude_to_validate = float(str(user_latitude)[:6])
    longitude_to_validate = float(str(user_longitude)[:6])
    
    if latitude_to_validate == bridge_latitude and longitude_to_validate == bridge_longitude:
        return True
    else:
        return False
    
def update_user_bridges(user_id: int, bridge_name: str)->None:
    # funkcja do aktualizacji listy odwiedzonych mostów przez użytkownika
    # Pobierz most na podstawie jego nazwy
    bridge = Bridge.query.filter_by(name=bridge_name).first()
    
    if bridge is None:
        return redirect(url_for('main.errorhandler'))
    
    user = User.query.get(user_id)
    
    if bridge in user.visited_bridges:
        return  redirect(url_for('main.profile'))
    
    # tego nie jestem pewien
    user.visited_bridges.append(bridge)
    
    stmt = user_bridge_association.insert().values(
        user_id=user_id,
        bridge_id=bridge.bridge_id,
        timestamp=datetime.utcnow()
    )
    db.session.execute(stmt)
    db.session.commit()

@gameplay_bp.route('/gameplay', methods = ['POST', 'GET'])
@login_required
def gameplay():
    if request.method == 'GET':
        return render_template('gameplay_page.html')
    
    if request.method == 'POST':
        bridge_name = request.form['bridgeName']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        
        if verify_user_location(bridge_name, float(latitude), float(longitude)):
            update_user_bridges(current_user.get_id(), bridge_name)
            return redirect(url_for('main.profile'))
