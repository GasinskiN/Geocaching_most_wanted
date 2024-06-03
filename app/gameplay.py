from flask import Blueprint, jsonify, request, redirect, url_for, render_template
from flask_login import login_required, current_user
from . import db
from .models import User, Bridge, user_bridge_association
from datetime import datetime
from flasgger import swag_from

gameplay_bp = Blueprint('gameplay', __name__)

def verify_user_location(selected_bridge_name: str, user_latitude: float, user_longitude: float) -> bool:
    bridge = Bridge.query.filter_by(name=selected_bridge_name).first()
    if bridge is None:
        return False
    
    bridge_latitude = float(str(bridge.latitude)[:6])
    bridge_longitude = float(str(bridge.longitude)[:6])
    
    latitude_to_validate = float(str(user_latitude)[:6])
    longitude_to_validate = float(str(user_longitude)[:6])
    
    return latitude_to_validate == bridge_latitude and longitude_to_validate == bridge_longitude

def update_user_bridges(user_id: int, bridge_name: str) -> None:
    bridge = Bridge.query.filter_by(name=bridge_name).first()
    if bridge is None:
        return
    
    user = User.query.get(user_id)
    if bridge in user.visited_bridges:
        return
    
    user.visited_bridges.append(bridge)
    
    stmt = user_bridge_association.insert().values(
        user_id=user_id,
        bridge_id=bridge.bridge_id,
        timestamp=datetime.utcnow()
    )
    db.session.execute(stmt)
    user.points += 100
    db.session.commit()

@gameplay_bp.route('/gameplay', methods=['GET'])
@login_required
def gameplay_page():
    bridges = Bridge.query.all()
    return render_template('gameplay_page.html', bridges=bridges)

@gameplay_bp.route('/api/gameplay', methods=['POST'])
@login_required
@swag_from({
    'tags': ['gameplay'],
    'responses': {
        200: {
            'description': 'Location verification and update success',
            'content': {
                'application/json': {
                    'example': {'status': 'success'}
                }
            }
        },
        400: {
            'description': 'Bad Request - Invalid data or location mismatch',
            'content': {
                'application/json': {
                    'example': {'error': 'Invalid data'}
                }
            }
        }
    },
    'parameters': [
        {
            'name': 'bridgeName',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'bridgeName': {
                        'type': 'string',
                        'description': 'Name of the bridge',
                        'example': 'Most Grunwaldzki'
                    },
                    'latitude': {
                        'type': 'number',
                        'description': 'Latitude of the user location',
                        'example': 37.8199
                    },
                    'longitude': {
                        'type': 'number',
                        'description': 'Longitude of the user location',
                        'example': -122.4783
                    }
                },
                'required': ['bridgeName', 'latitude', 'longitude']
            }
        }
    ]
})
def gameplay_api():
    data = request.json
    bridge_name = data.get('bridgeName')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if not bridge_name or latitude is None or longitude is None:
        return jsonify({'error': 'Invalid data'}), 400
    
    if verify_user_location(bridge_name, float(latitude), float(longitude)):
        update_user_bridges(current_user.get_id(), bridge_name)
        return jsonify({'status': 'success'}), 200
    
    return jsonify({'error': 'Location mismatch'}), 400
