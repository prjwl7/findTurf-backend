from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
import socket
from csv_helper import append_to_csv, write_csv
app = Flask(__name__)
CORS(app)

# MongoDB Configuration
client = MongoClient('mongodb+srv://prajwal1105:prajwal1105@cluster0.6dkonu9.mongodb.net/')
db = client['findTurf']
collection = db['Cluster0']

# MySQL Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:prajwal2708@localhost/findturf'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_sql = SQLAlchemy(app)

# Define Jersey Model
class Jersey(db_sql.Model):
    __tablename__ = 'jersey'
    id = db_sql.Column(db_sql.Integer, primary_key=True, index=True)
    name = db_sql.Column(db_sql.String(80), nullable=False)
    team = db_sql.Column(db_sql.String(120), nullable=False, index=True)
    league = db_sql.Column(db_sql.String(120))
    type = db_sql.Column(db_sql.String(120))
    home_away_third = db_sql.Column(db_sql.String(120))
    size = db_sql.Column(db_sql.String(120))
    number_of_jerseys = db_sql.Column(db_sql.Integer)
    price = db_sql.Column(db_sql.Float)
    customizable = db_sql.Column(db_sql.Boolean)
    discounted_price = db_sql.Column(db_sql.Float)

    def __init__(self, name, team, league, type, home_away_third, size, number_of_jerseys, price, customizable, discounted_price):
        self.name = name
        self.team = team
        self.league = league
        self.type = type
        self.home_away_third = home_away_third
        self.size = size
        self.number_of_jerseys = number_of_jerseys
        self.price = price
        self.customizable = customizable
        self.discounted_price = discounted_price

# Create the database tables
with app.app_context():
    db_sql.create_all()

# CRUD Operations
def create_jersey(data):
    name = data.get('name')
    team = data.get('team')
    league = data.get('league')
    type = data.get('type')
    home_away_third = data.get('home_away_third')
    size = data.get('size')
    number_of_jerseys = data.get('number_of_jerseys')
    price = data.get('price')
    customizable = data.get('customizable')
    discounted_price = data.get('discounted_price')
    
    if not (name and team and league and type and home_away_third and size and number_of_jerseys and price and customizable is not None and discounted_price):
        raise ValueError("Incomplete data")
    
    new_jersey = Jersey(
        name=name,
        team=team,
        league=league,
        type=type,
        home_away_third=home_away_third,
        size=size,
        number_of_jerseys=number_of_jerseys,
        price=price,
        customizable=customizable,
        discounted_price=discounted_price
    )
    
    db_sql.session.add(new_jersey)
    db_sql.session.commit()
    
    row = {
        'id': new_jersey.id,
        'name': name,
        'team': team,
        'league': league,
        'type': type,
        'home_away_third': home_away_third,
        'size': size,
        'number_of_jerseys': number_of_jerseys,
        'price': price,
        'customizable': customizable,
        'discounted_price': discounted_price
    }
    append_to_csv(row)
    
    return new_jersey

def get_jerseys():
    return Jersey.query.all()

def update_jersey(jersey_id, data):
    jersey = Jersey.query.get(jersey_id)
    if not jersey:
        raise ValueError("Jersey not found")
    
    jersey.name = data.get('name', jersey.name)
    jersey.team = data.get('team', jersey.team)
    jersey.league = data.get('league', jersey.league)
    jersey.type = data.get('type', jersey.type)
    jersey.home_away_third = data.get('home_away_third', jersey.home_away_third)
    jersey.size = data.get('size', jersey.size)
    jersey.number_of_jerseys = data.get('number_of_jerseys', jersey.number_of_jerseys)
    jersey.price = data.get('price', jersey.price)
    jersey.customizable = data.get('customizable', jersey.customizable)
    jersey.discounted_price = data.get('discounted_price', jersey.discounted_price)
    
    db_sql.session.commit()
    
    # Update CSV file
    jerseys = get_jerseys()
    jerseys_list = [{
        'id': j.id,
        'name': j.name,
        'team': j.team,
        'league': j.league,
        'type': j.type,
        'home_away_third': j.home_away_third,
        'size': j.size,
        'number_of_jerseys': j.number_of_jerseys,
        'price': j.price,
        'customizable': j.customizable,
        'discounted_price': j.discounted_price
    } for j in jerseys]
    write_csv(jerseys_list)
    
    return jersey

def delete_jersey(jersey_id):
    jersey = Jersey.query.get(jersey_id)
    if not jersey:
        raise ValueError("Jersey not found")
    
    db_sql.session.delete(jersey)
    db_sql.session.commit()
    
    # Update CSV file
    jerseys = get_jerseys()
    jerseys_list = [{
        'id': j.id,
        'name': j.name,
        'team': j.team,
        'league': j.league,
        'type': j.type,
        'home_away_third': j.home_away_third,
        'size': j.size,
        'number_of_jerseys': j.number_of_jerseys,
        'price': j.price,
        'customizable': j.customizable,
        'discounted_price': j.discounted_price
    } for j in jerseys]
    write_csv(jerseys_list)
    
    return jersey

# Flask Routes for CRUD Operations
@app.route('/api/jerseys', methods=['POST'])
def add_jersey():
    try:
        data = request.get_json()
        new_jersey = create_jersey(data)
        return jsonify({'message': 'Jersey added successfully', 'jersey': new_jersey.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/jerseys', methods=['GET'])
def list_jerseys():
    try:
        jerseys = get_jerseys()
        jerseys_list = [{
        'id': j.id,
        'name': j.name,
        'team': j.team,
        'league': j.league,
        'type': j.type,
        'home_away_third': j.home_away_third,
        'size': j.size,
        'number_of_jerseys': j.number_of_jerseys,
        'price': j.price,
        'customizable': j.customizable,
        'discounted_price': j.discounted_price
        } for j in jerseys]
        write_csv(jerseys_list)
        jerseys_list = [{'id': jersey.id, 'name': jersey.name, 'team': jersey.team, 'league': jersey.league, 'type': jersey.type, 'home_away_third': jersey.home_away_third, 'size': jersey.size, 'number_of_jerseys': jersey.number_of_jerseys, 'price': jersey.price, 'customizable': jersey.customizable, 'discounted_price': jersey.discounted_price} for jersey in jerseys]
        return jsonify(jerseys_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/jerseys/<int:jersey_id>', methods=['PUT'])
def modify_jersey(jersey_id):
    try:
        data = request.get_json()
        updated_jersey = update_jersey(jersey_id, data)
        return jsonify({'message': 'Jersey updated successfully', 'jersey': updated_jersey.id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/jerseys/<int:jersey_id>', methods=['DELETE'])
def remove_jersey(jersey_id):
    try:
        deleted_jersey = delete_jersey(jersey_id)
        return jsonify({'message': 'Jersey deleted successfully', 'jersey': deleted_jersey.id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400



# Existing routes for MongoDB operations
@app.route('/api/storeFormData', methods=['POST'])
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

@app.route('/api/checkEmailExists', methods=['POST'])
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

@app.route('/api/insertLocation', methods=['POST'])
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

@app.route('/api/getIPAddress', methods=['GET'])
def get_ip_address():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return jsonify({'ip': ip_address})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
