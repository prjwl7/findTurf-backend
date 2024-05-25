from flask import Blueprint, jsonify, request
from cruds.booking_crud import get_bookings, create_booking, update_booking, delete_booking
from models import Booking, User, Turf, TurfImage
from sqlalchemy.exc import SQLAlchemyError

booking_routes = Blueprint('booking_routes', __name__)

@booking_routes.route('/api/bookings', methods=['POST'])
def add_booking():
    try:
        data = request.get_json()
        new_booking = create_booking(data)
        return jsonify({'message': 'Booking added successfully', 'booking_id': new_booking.booking_id}), 200
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@booking_routes.route('/api/bookings', methods=['GET'])
def list_bookings():
    try:
        bookings = Booking.query.join(User, Booking.user_id == User.UserID).join(Turf, Booking.turf_id == Turf.TurfID).all()
        bookings_list = [{
            'booking_id': booking.booking_id,
            'user_id': booking.user_id,
            'turf_id': booking.turf_id,
            'time_slot': booking.time_slot,
            'status': booking.status,
            'user': {
                'UserID': booking.user.UserID,
                'Username': booking.user.Username,
                'Email': booking.user.Email,
                'PhoneNumber': booking.user.PhoneNumber,
                'ProfilePicture': booking.user.ProfilePicture,
                'Bio': booking.user.Bio
            },
            'turf': {
                'TurfID': booking.turf.TurfID,
                'name': booking.turf.name,
                'location': booking.turf.location,
                'charges': str(booking.turf.charges),  # Convert to string for JSON serialization
                'availableTimeSlots': booking.turf.availableTimeSlots,
                'images': [image.ImageURL for image in booking.turf.images]  # Fetch image URLs
            }
        } for booking in bookings]
        return jsonify(bookings_list), 200
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@booking_routes.route('/api/bookings/<int:booking_id>', methods=['PUT'])
def edit_booking(booking_id):
    try:
        data = request.get_json()
        updated_booking = update_booking(booking_id, data)
        return jsonify({'message': 'Booking updated successfully', 'booking_id': updated_booking.booking_id}), 200
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@booking_routes.route('/api/bookings/<int:booking_id>', methods=['DELETE'])
def remove_booking(booking_id):
    try:
        deleted_booking = delete_booking(booking_id)
        return jsonify({'message': 'Booking deleted successfully', 'booking_id': deleted_booking.booking_id}), 200
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@booking_routes.route('/api/bookings/email/<string:email>', methods=['GET'])
def get_bookings_by_email(email):
    try:
        bookings = Booking.query.join(User, Booking.user_id == User.UserID)\
                                .join(Turf, Booking.turf_id == Turf.TurfID)\
                                .filter(User.Email == email).all()

        if not bookings:
            return jsonify({'message': 'No bookings found for this email'}), 404

        bookings_list = [{
            'booking_id': booking.booking_id,
            'user_id': booking.user_id,
            'turf_id': booking.turf_id,
            'time_slot': booking.time_slot,
            'status': booking.status,
            'user': {
                'UserID': booking.user.UserID,
                'Username': booking.user.Username,
                'Email': booking.user.Email,
                'PhoneNumber': booking.user.PhoneNumber,
                'ProfilePicture': booking.user.ProfilePicture,
                'Bio': booking.user.Bio
            },
            'turf': {
                'TurfID': booking.turf.TurfID,
                'name': booking.turf.name,
                'location': booking.turf.location,
                'charges': str(booking.turf.charges),  # Convert to string for JSON serialization
                'availableTimeSlots': booking.turf.availableTimeSlots,
                'images': [image.ImageURL for image in booking.turf.images]  # Fetch image URLs
            }
        } for booking in bookings]
        return jsonify(bookings_list), 200
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
