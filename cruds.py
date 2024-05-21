from models import db, Jersey, Orders, Booking
from csv_helper import append_to_csv, write_csv

# CRUD Operations for Jersey

def create_jersey(data):
    new_jersey = Jersey(
        name=data['name'],
        team=data['team'],
        league=data['league'],
        type=data['type'],
        home_away_third=data['home_away_third'],
        sizes=','.join(data['sizes']),  # Convert list to comma-separated string
        number_of_jerseys=data['number_of_jerseys'],
        price=data['price'],
        customizable=data['customizable'],
        discounted_price=data['discounted_price'],
        image_url=data['image_url']
    )
    db.session.add(new_jersey)
    db.session.commit()
    return new_jersey

def get_jerseys(search='', sort_by='', home_away_third='', team='', price=''):
   query = Jersey.query

   if search:
        query = query.filter(
            (Jersey.name.ilike(f'%{search}%')) |
            (Jersey.team.ilike(f'%{search}%'))
        )

   if home_away_third:
        query = query.filter_by(home_away_third=home_away_third)

   if team:
        query = query.filter_by(team=team)

   if price:
        if price == 'Under 500':
            query = query.filter(Jersey.price < 500)
        elif price == '500-1000':
            query = query.filter(Jersey.price.between(500, 1000))
        elif price == 'Above 1000':
            query = query.filter(Jersey.price > 1000)

   if sort_by:
        if sort_by == 'Low-High':
            query = query.order_by(Jersey.price.asc())
        elif sort_by == 'High-Low':
            query = query.order_by(Jersey.price.desc())
        elif sort_by == 'A-Z':
            query = query.order_by(Jersey.name.asc())
        elif sort_by == 'Z-A':
            query = query.order_by(Jersey.name.desc())
   return query.all()

def update_jersey(jersey_id, data):
    jersey = Jersey.query.get(jersey_id)
    if not jersey:
        raise ValueError("Jersey not found")

    jersey.name = data.get('name', jersey.name)
    jersey.team = data.get('team', jersey.team)
    jersey.league = data.get('league', jersey.league)
    jersey.type = data.get('type', jersey.type)
    jersey.home_away_third = data.get('home_away_third', jersey.home_away_third)
    jersey.sizes = ','.join(data.get('sizes', jersey.sizes.split(',')))
    jersey.number_of_jerseys = data.get('number_of_jerseys', jersey.number_of_jerseys)
    jersey.price = data.get('price', jersey.price)
    jersey.customizable = data.get('customizable', jersey.customizable)
    jersey.discounted_price = data.get('discounted_price', jersey.discounted_price)
    jersey.image_url = data.get('image_url', jersey.image_url)

    db.session.commit()
    return jersey

def delete_jersey(jersey_id):
    jersey = Jersey.query.get(jersey_id)
    if not jersey:
        raise ValueError("Jersey not found")

    db.session.delete(jersey)
    db.session.commit()
    return jersey


# CRUD Operations for Orders
def create_order(data):
    name = data.get('name')
    email = data.get('email')
    phoneNumber = data.get('phoneNumber')
    jersey = data.get('jersey')
    size = data.get('size')
    quantity = data.get('quantity')
    amount = data.get('amount')
    address = data.get('address')
    
    if not (name and email and phoneNumber and jersey and size and quantity and amount and address):
        raise ValueError("Incomplete data")
    
    new_order = Orders(
        name=name,
        email=email,
        phoneNumber=phoneNumber,
        jersey=jersey,
        size=size,
        quantity=quantity,
        amount=amount,
        address=address
    )
    
    db.session.add(new_order)
    db.session.commit()
    
    return new_order

def get_orders():
    return Orders.query.all()

def delete_order(order_id):
    order = Orders.query.get(order_id)
    if not order:
        raise ValueError("Order not found")
    
    db.session.delete(order)
    db.session.commit()
    
    return order

# CRUD Operations for Booking
def create_booking(data):
    name = data.get('name')
    email = data.get('email')
    phoneNumber = data.get('phoneNumber')
    turf = data.get('turf')
    location = data.get('location')
    date = data.get('date')
    hours = data.get('hours')
    amount = data.get('amount')
    type = data.get('type')
    
    if not (name and email and phoneNumber and turf and location and date and hours and amount and type):
        raise ValueError("Incomplete data")
    
    new_booking = Booking(
        name=name,
        email=email,
        phoneNumber=phoneNumber,
        turf=turf,
        location=location,
        date=date,
        hours=hours,
        amount=amount,
        type=type
    )
    
    db.session.add(new_booking)
    db.session.commit()
    
    return new_booking

def get_bookings():
    return Booking.query.all()

def update_booking(booking_id, data):
    booking = Booking.query.get(booking_id)
    if not booking:
        raise ValueError("Booking not found")
    
    booking.name = data.get('name', booking.name)
    booking.email = data.get('email', booking.email)
    booking.phoneNumber = data.get('phoneNumber', booking.phoneNumber)
    booking.turf = data.get('turf', booking.turf)
    booking.location = data.get('location', booking.location)
    booking.date = data.get('date', booking.date)
    booking.hours = data.get('hours', booking.hours)
    booking.amount = data.get('amount', booking.amount)
    booking.type = data.get('type', booking.type)
    
    db.session.commit()
    
    return booking

def delete_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        raise ValueError("Booking not found")
    
    db.session.delete(booking)
    db.session.commit()
    
    return booking
