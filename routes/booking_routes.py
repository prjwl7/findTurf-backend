from flask import Blueprint, jsonify, request
from cruds import create_booking, get_bookings, update_booking, delete_booking
from models import Booking
booking_routes = Blueprint('booking_routes', __name__)

@booking_routes.route('/api/bookings', methods=['POST'])
def add_booking():
    try:
        data = request.get_json()
        new_booking = create_booking(data)
        return jsonify({'message': 'Booking added successfully', 'booking': new_booking.id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@booking_routes.route('/api/bookings', methods=['GET'])
def list_bookings():
    try:
        bookings = get_bookings()
        bookings_list = [{
            'id': booking.id,
            'name': booking.name,
            'email': booking.email,
            'phoneNumber': booking.phoneNumber,
            'turf': booking.turf,
            'location': booking.location,
            'date': booking.date.strftime('%Y-%m-%d'),
            'hours': booking.hours,
            'amount': booking.amount,
            'type': booking.type
        } for booking in bookings]
        return jsonify(bookings_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@booking_routes.route('/api/bookings/<int:booking_id>', methods=['PUT'])
def edit_booking(booking_id):
    try:
        data = request.get_json()
        updated_booking = update_booking(booking_id, data)
        return jsonify({'message': 'Booking updated successfully', 'booking': updated_booking.id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@booking_routes.route('/api/bookings/<int:booking_id>', methods=['DELETE'])
def remove_booking(booking_id):
    try:
        deleted_booking = delete_booking(booking_id)
        return jsonify({'message': 'Booking deleted successfully', 'booking': deleted_booking.id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@booking_routes.route('/api/bookings/email/<string:email>', methods=['GET'])
def get_bookings_by_email(email):
    try:
        bookings = Booking.query.filter_by(email=email).all()
        if not bookings:
            return jsonify({'message': 'No bookings found for this email'}), 404

        bookings_list = [{
            'id': booking.id,
            'name': booking.name,
            'email': booking.email,
            'phoneNumber': booking.phoneNumber,
            'turf': booking.turf,
            'location': booking.location,
            'date': booking.date.strftime('%Y-%m-%d'),
            'hours': booking.hours,
            'amount': booking.amount,
            'type': booking.type
        } for booking in bookings]
        return jsonify(bookings_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
