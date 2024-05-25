from models import db, Booking, User, Turf

def create_booking(data):
    new_booking = Booking(
        user_id=data['user_id'],
        turf_id=data['turf_id'],
        time_slot=data['time_slot'],
        status=data['status']
    )
    db.session.add(new_booking)
    db.session.commit()
    return new_booking

def get_bookings():
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
            'Name': booking.turf.Name,
            'Location': booking.turf.Location,
            'Type': booking.turf.Type
        }
    } for booking in bookings]
    return bookings_list

def update_booking(booking_id, data):
    booking = Booking.query.get(booking_id)
    if not booking:
        raise ValueError("Booking not found")

    booking.user_id = data.get('user_id', booking.user_id)
    booking.turf_id = data.get('turf_id', booking.turf_id)
    booking.time_slot = data.get('time_slot', booking.time_slot)
    booking.status = data.get('status', booking.status)
    
    db.session.commit()
    return booking

def delete_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        raise ValueError("Booking not found")

    db.session.delete(booking)
    db.session.commit()
    return booking
