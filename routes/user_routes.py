from flask import Blueprint, request, jsonify
from cruds.user_crud import create_user, get_users, get_user_by_id, update_user, delete_user, get_user_by_email

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/api/users', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        new_user = create_user(data)
        return jsonify({'message': 'User added successfully', 'user_id': new_user.UserID}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@user_routes.route('/api/users', methods=['GET'])
def list_users():
    try:
        users = get_users()
        users_list = [{
            'UserID': user.UserID,
            'Username': user.Username,
            'Email': user.Email,
            'PhoneNumber': user.PhoneNumber,
            'ProfilePicture': user.ProfilePicture,
            'Bio': user.Bio
        } for user in users]
        return jsonify(users_list), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 500

@user_routes.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = get_user_by_id(user_id)
        return jsonify({
            'UserID': user.UserID,
            'Username': user.Username,
            'Email': user.Email,
            'PhoneNumber': user.PhoneNumber,
            'ProfilePicture': user.ProfilePicture,
            'Bio': user.Bio
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@user_routes.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    try:
        data = request.get_json()
        updated_user = update_user(user_id, data)
        return jsonify({'message': 'User updated successfully', 'user_id': updated_user.UserID}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@user_routes.route('/api/users/<int:user_id>', methods=['DELETE'])
def remove_user(user_id):
    try:
        deleted_user = delete_user(user_id)
        return jsonify({'message': 'User deleted successfully', 'user_id': deleted_user.UserID}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@user_routes.route('/api/users/by_email', methods=['GET'])
def get_user_id_by_email():
    try:
        email = request.args.get('email')
        if not email:
            return jsonify({'error': 'Email parameter is missing'}), 400

        user = get_user_by_email(email)
        if not user:
            return jsonify({'error': 'User with the provided email not found'}), 404

        return jsonify({'UserID': user.UserID}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 500
