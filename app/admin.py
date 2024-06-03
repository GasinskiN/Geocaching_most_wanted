from flask import Blueprint, jsonify, request, render_template
from flask_login import login_required
from . import db
from .models import Bridge
from .decorators import admin_required
from flasgger import swag_from

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/bridges', methods=['GET'])
@login_required
@admin_required
def show_add_bridge_form():
    return render_template('add_bridge.html')

@admin_bp.route('/bridges', methods=['POST'])
@login_required
@admin_required
@swag_from({
    'tags': ['Admin'],
    'parameters': [
        {
            'name': 'bridge',
            'in': 'body',
            'description': 'Bridge to add',
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'description': {'type': 'string'},
                    'image_path': {'type': 'string'},
                    'latitude': {'type': 'number'},
                    'longitude': {'type': 'number'}
                },
                'required': ['name', 'image_path', 'latitude', 'longitude']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Bridge successfully added',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        },
        400: {
            'description': 'Invalid input'
        },
        401: {
            'description': 'Unauthorized'
        },
        403: {
            'description': 'Forbidden'
        }
    }
})
def add_bridge():
    data = request.get_json()

    name = data.get('name')
    description = data.get('description')
    image_path = data.get('image_path')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if not name or not image_path or latitude is None or longitude is None:
        return jsonify({'error': 'Invalid input'}), 400

    new_bridge = Bridge(
        name=name,
        description=description,
        image_path=image_path,
        latitude=latitude,
        longitude=longitude
    )
    db.session.add(new_bridge)
    db.session.commit()
    return jsonify({'message': 'Bridge successfully added'}), 201
