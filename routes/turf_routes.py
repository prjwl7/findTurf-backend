# routes/turf_routes.py

from flask import Blueprint, jsonify, request
from cruds.turf_crud import create_turf, get_turfs, get_turf_by_id, update_turf, delete_turf

turf_routes = Blueprint('turf_routes', __name__)

@turf_routes.route('/api/turfs', methods=['POST'])
def add_turf():
    try:
        data = request.get_json()
        new_turf = create_turf(data)
        return jsonify({'message': 'Turf added successfully', 'turf_id': new_turf.TurfID}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@turf_routes.route('/api/turfs', methods=['GET'])
def list_turfs():
    try:
        turfs = get_turfs()
        turfs_list = [{
            'TurfID': turf.TurfID,
            'name': turf.name,
            'location': turf.location,
            'city' : turf.city,
            'charges': turf.charges,
            'availableTimeSlots': turf.availableTimeSlots,
            'image_urls': [image.ImageURL for image in turf.images]
        } for turf in turfs]
        return jsonify(turfs_list), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 500

@turf_routes.route('/api/turfs/<int:turf_id>', methods=['GET'])
def get_turf(turf_id):
    try:
        turf = get_turf_by_id(turf_id)
        if not turf:
            return jsonify({'message': 'Turf not found'}), 404
        return jsonify({
            'TurfID': turf.TurfID,
            'name': turf.name,
            'location': turf.location,
            'city' : turf.city,
            'charges': turf.charges,
            'availableTimeSlots': turf.availableTimeSlots,
            'image_urls': [image.ImageURL for image in turf.images]
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 500

@turf_routes.route('/api/turfs/<int:turf_id>', methods=['PUT'])
def edit_turf(turf_id):
    try:
        data = request.get_json()
        updated_turf = update_turf(turf_id, data)
        return jsonify({'message': 'Turf updated successfully', 'turf_id': updated_turf.TurfID}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@turf_routes.route('/api/turfs/<int:turf_id>', methods=['DELETE'])
def remove_turf(turf_id):
    try:
        deleted_turf = delete_turf(turf_id)
        return jsonify({'message': 'Turf deleted successfully', 'turf_id': deleted_turf.TurfID}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
