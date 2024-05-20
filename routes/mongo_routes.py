from flask import Blueprint, jsonify, request
from pymongo import MongoClient
import socket

mongo_routes = Blueprint('mongo_routes', __name__)

# MongoDB Configuration
client = MongoClient('mongodb+srv://prajwal1105:prajwal1105@cluster0.6dkonu9.mongodb.net/')
db = client['findTurf']
collection = db['Cluster0']

@mongo_routes.route('/api/storeFormData', methods=['POST'])
def store_form_data():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        location = data.get('location')

        if not (name and email and location):
            return jsonify({'error': 'Incomplete form data'}), 400

        result = collection.insert_one({'name': name, 'email': email, 'location': location})

        return jsonify({'message': 'Form data stored successfully', 'id': str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@mongo_routes.route('/api/checkEmailExists', methods=['POST'])
def check_email_exists():
    try:
        data = request.get_json()
        email = data.get('email')

        user = collection.find_one({'email': email})
        if user:
            return jsonify({'exists': True})
        else:
            return jsonify({'exists': False})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@mongo_routes.route('/api/insertLocation', methods=['POST'])
def insert_location():
    try:
        data = request.get_json()
        phone_number = data.get('phoneNumber')
        email = data.get('email')
        location = data.get('location')

        if not (email and location and phone_number):
            return jsonify({'error': 'Incomplete data'}), 400

        result = collection.update_one({'email': email}, {'$set': {'location': location, 'phone_number': phone_number}})

        if result.modified_count > 0:
            return jsonify({'message': 'Location updated successfully'})
        else:
            return jsonify({'message': 'Email not found'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@mongo_routes.route('/api/getIPAddress', methods=['GET'])
def get_ip_address():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return jsonify({'ip': ip_address})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
