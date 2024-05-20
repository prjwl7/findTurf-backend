from database import db

class Jersey(db.Model):
    __tablename__ = 'jersey'

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(80), nullable=False)
    team = db.Column(db.String(120), nullable=False, index=True)
    league = db.Column(db.String(120))
    type = db.Column(db.String(120))
    home_away_third = db.Column(db.String(120))
    sizes = db.Column(db.String(120))  # Store sizes as a comma-separated string
    number_of_jerseys = db.Column(db.Integer)
    price = db.Column(db.Float)
    customizable = db.Column(db.Boolean)
    discounted_price = db.Column(db.Float)
    image_url = db.Column(db.String(255))  # Field to store image URL

    def __init__(self, name, team, league, type, home_away_third, sizes, number_of_jerseys, price, customizable, discounted_price, image_url):
        self.name = name
        self.team = team
        self.league = league
        self.type = type
        self.home_away_third = home_away_third
        self.sizes = sizes
        self.number_of_jerseys = number_of_jerseys
        self.price = price
        self.customizable = customizable
        self.discounted_price = discounted_price
        self.image_url = image_url

class Orders(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phoneNumber = db.Column(db.String(20), nullable=False)
    jersey = db.Column(db.String(80), nullable=False)
    size = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(255), nullable=False)

    def __init__(self, name, email, phoneNumber, jersey, size, quantity, amount, address):
        self.name = name
        self.email = email
        self.phoneNumber = phoneNumber
        self.jersey = jersey
        self.size = size
        self.quantity = quantity
        self.amount = amount
        self.address = address

class Booking(db.Model):
    __tablename__ = 'booking'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phoneNumber = db.Column(db.String(20), nullable=False)
    turf = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    hours = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(50), nullable=False)

    def __init__(self, name, email, phoneNumber, turf, location, date, hours, amount, type):
        self.name = name
        self.email = email
        self.phoneNumber = phoneNumber
        self.turf = turf
        self.location = location
        self.date = date
        self.hours = hours
        self.amount = amount
        self.type = type        


