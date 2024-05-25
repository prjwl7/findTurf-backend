from flask import Blueprint, jsonify, request
from cruds.jersey_crud import create_jersey, get_jerseys, update_jersey, delete_jersey

jersey_routes = Blueprint('jersey_routes', __name__)

@jersey_routes.route('/api/jerseys', methods=['POST'])
def add_jersey():
    try:
        data = request.get_json()
        new_jersey = create_jersey(data)
        return jsonify({'message': 'Jersey added successfully', 'jersey': new_jersey.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@jersey_routes.route('/api/jerseys', methods=['GET'])
def list_jerseys():
    try:
        search = request.args.get('search', '')
        sort_by = request.args.get('sort_by', '')
        home_away_third = request.args.get('home_away_third', '')
        team = request.args.get('team', '')
        price = request.args.get('price', '')

        jerseys = get_jerseys(search, sort_by, home_away_third, team, price)
        jerseys_list = [{
            'id': j.id,
            'name': j.name,
            'team': j.team,
            'league': j.league,
            'type': j.type,
            'home_away_third': j.home_away_third,
            'sizes': j.sizes.split(','),  # Convert comma-separated string back to list
            'number_of_jerseys': j.number_of_jerseys,
            'price': j.price,
            'customizable': j.customizable,
            'discounted_price': j.discounted_price,
            'image_url': j.image_url
        } for j in jerseys]
        return jsonify(jerseys_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@jersey_routes.route('/api/jerseys/<int:jersey_id>', methods=['PUT'])
def modify_jersey(jersey_id):
    try:
        data = request.get_json()
        updated_jersey = update_jersey(jersey_id, data)
        return jsonify({'message': 'Jersey updated successfully', 'jersey': updated_jersey.id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@jersey_routes.route('/api/jerseys/<int:jersey_id>', methods=['DELETE'])
def remove_jersey(jersey_id):
    try:
        deleted_jersey = delete_jersey(jersey_id)
        return jsonify({'message': 'Jersey deleted successfully', 'jersey': deleted_jersey.id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
