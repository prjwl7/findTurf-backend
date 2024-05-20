from models import db, Jersey, Orders
from csv_helper import append_to_csv, write_csv

# CRUD Operations for Jersey
def create_jersey(data):
    name = data.get('name')
    team = data.get('team')
    league = data.get('league')
    type = data.get('type')
    home_away_third = data.get('home_away_third')
    sizes = ','.join(data.get('sizes'))  # Convert list of sizes to a comma-separated string
    number_of_jerseys = data.get('number_of_jerseys')
    price = data.get('price')
    customizable = data.get('customizable')
    discounted_price = data.get('discounted_price')
    image_url = data.get('image_url')
    
    if not (name and team and league and type and home_away_third and sizes and number_of_jerseys and price and customizable is not None and discounted_price and image_url):
        raise ValueError("Incomplete data")
    
    new_jersey = Jersey(
        name=name,
        team=team,
        league=league,
        type=type,
        home_away_third=home_away_third,
        sizes=sizes,
        number_of_jerseys=number_of_jerseys,
        price=price,
        customizable=customizable,
        discounted_price=discounted_price,
        image_url=image_url
    )
    
    db.session.add(new_jersey)
    db.session.commit()
    
    row = {
        'id': new_jersey.id,
        'name': name,
        'team': team,
        'league': league,
        'type': type,
        'home_away_third': home_away_third,
        'sizes': sizes,
        'number_of_jerseys': number_of_jerseys,
        'price': price,
        'customizable': customizable,
        'discounted_price': discounted_price,
        'image_url': image_url
    }
    append_to_csv(row)
    
    return new_jersey

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
    jerseys = get_jerseys()
    jerseys_list = [{
        'id': j.id,
        'name': j.name,
        'team': j.team,
        'league': j.league,
        'type': j.type,
        'home_away_third': j.home_away_third,
        'sizes': j.sizes,
        'number_of_jerseys': j.number_of_jerseys,
        'price': j.price,
        'customizable': j.customizable,
        'discounted_price': j.discounted_price,
        'image_url': j.image_url
    } for j in jerseys]
    write_csv(jerseys_list)
    
    return jersey

def get_jerseys():
    return Jersey.query.all()

def delete_jersey(jersey_id):
    jersey = Jersey.query.get(jersey_id)
    if not jersey:
        raise ValueError("Jersey not found")
    
    db.session.delete(jersey)
    db.session.commit()
    
    # Update CSV file
    jerseys = get_jerseys()
    jerseys_list = [{
        'id': j.id,
        'name': j.name,
        'team': j.team,
        'league': j.league,
        'type': j.type,
        'home_away_third': j.home_away_third,
        'sizes': j.sizes,
        'number_of_jerseys': j.number_of_jerseys,
        'price': j.price,
        'customizable': j.customizable,
        'discounted_price': j.discounted_price,
        'image_url': j.image_url
    } for j in jerseys]
    write_csv(jerseys_list)
    
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
