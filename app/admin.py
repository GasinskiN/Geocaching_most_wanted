from flask import Blueprint, jsonify, request, render_template
from flask_login import login_required
from . import db
from .models import Bridge, Achievement
from .decorators import admin_required
from flasgger import swag_from

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/api/add_bridge', methods=['GET'])
@login_required
@admin_required
def show_add_bridge_form():
    return render_template('add_bridge.html')

@admin_bp.route('/api/add_bridge', methods=['POST'])
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



@admin_bp.route('/api/delete_bridge', methods=['GET'])
@login_required
@admin_required
@swag_from({
    'tags': ['Admin'],
    'responses': {
        200: {
            'description': 'Form to delete a bridge',
            'content': {
                'text/html': {
                    'example': '<html>Delete Bridge Form</html>'
                }
            }
        },
        401: {
            'description': 'Unauthorized'
        },
        403: {
            'description': 'Forbidden'
        }
    }
})
def show_delete_bridge_form():
    return render_template('delete_bridge.html')


@admin_bp.route('/api/delete_bridge/<int:bridge_id>', methods=['DELETE'])
@login_required
@admin_required
@swag_from({
    'tags': ['Admin'],
    'parameters': [
        {
            'name': 'bridge_id',
            'in': 'path',
            'description': 'ID of the bridge to delete',
            'required': True,
            'schema': {
                'type': 'integer'
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Bridge successfully deleted',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        },
        400: {
            'description': 'Invalid bridge ID'
        },
        404: {
            'description': 'Bridge not found'
        },
        401: {
            'description': 'Unauthorized'
        },
        403: {
            'description': 'Forbidden'
        }
    }
})
def delete_bridge(bridge_id):
    bridge = Bridge.query.get(bridge_id)
    if bridge is None:
        return jsonify({'error': 'Bridge not found'}), 404

    db.session.delete(bridge)
    db.session.commit()
    return jsonify({'message': 'Bridge successfully deleted'}), 200




@admin_bp.route('/api/delete_achievement', methods=['GET'])
@login_required
@admin_required
@swag_from({
    'tags': ['Admin'],
    'responses': {
        200: {
            'description': 'Form to delete an achievement',
            'content': {
                'text/html': {
                    'example': '<html>Delete Achievement Form</html>'
                }
            }
        },
        401: {
            'description': 'Unauthorized'
        },
        403: {
            'description': 'Forbidden'
        }
    }
})
def show_delete_achievement_form():
    achievements = Achievement.query.all()
    return render_template('delete_achievement.html', achievements=achievements)

# Obsługa żądania usunięcia osiągnięcia
@admin_bp.route('/api/delete_achievement', methods=['POST'])
@login_required
@admin_required
@swag_from({
    'tags': ['Admin'],
    'parameters': [
        {
            'name': 'achievement_id',
            'in': 'body',
            'description': 'ID of the achievement to delete',
            'schema': {
                'type': 'object',
                'properties': {
                    'achievement_id': {'type': 'integer'}
                },
                'required': ['achievement_id']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Achievement successfully deleted',
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
def delete_achievement():
    data = request.get_json()
    achievement_id = data.get('achievement_id')

    achievement = Achievement.query.get(achievement_id)
    if achievement is None:
        return jsonify({'error': 'Invalid input'}), 400

    db.session.delete(achievement)
    db.session.commit()
    return jsonify({'message': 'Achievement successfully deleted'}), 200


@admin_bp.route('/api/add_achievement', methods=['GET'])
@login_required
@admin_required
@swag_from({
    'tags': ['Admin'],
    'responses': {
        200: {
            'description': 'Form to add an achievement',
            'content': {
                'text/html': {
                    'example': '<html>Add Achievement Form</html>'
                }
            }
        },
        401: {
            'description': 'Unauthorized'
        },
        403: {
            'description': 'Forbidden'
        }
    }
})
def show_add_achievement_form():
    return render_template('add_achievement.html')

# Obsługa żądania dodania osiągnięcia
@admin_bp.route('/api/add_achievement', methods=['POST'])
@login_required
@admin_required
@swag_from({
    'tags': ['Admin'],
    'parameters': [
        {
            'name': 'achievement',
            'in': 'body',
            'description': 'Achievement to add',
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'description': {'type': 'string'}
                },
                'required': ['name']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Achievement successfully added',
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
def add_achievement():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if not name:
        return jsonify({'error': 'Invalid input'}), 400

    new_achievement = Achievement(
        name=name,
        description=description
    )
    db.session.add(new_achievement)
    db.session.commit()
    return jsonify({'message': 'Achievement successfully added'}), 201