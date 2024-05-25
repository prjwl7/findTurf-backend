from sqlalchemy import Column, Integer, String, ForeignKey, Float, Text, DateTime, DECIMAL, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship
from database import db

# MATCH MODEL
class Match(db.Model):
    __tablename__ = 'matches'

    MatchID = Column(Integer, primary_key=True, autoincrement=True)
    TournamentID = Column(Integer, ForeignKey('tournaments.TournamentID'), index=True)
    Participant1ID = Column(Integer, ForeignKey('users.UserID'), index=True)
    Participant2ID = Column(Integer, ForeignKey('users.UserID'), index=True)
    WinnerID = Column(Integer, ForeignKey('users.UserID'), index=True)
    MatchDateTime = Column(DateTime)
    Status = Column(String(50))

    tournament = relationship("Tournament", back_populates="matches")
    participant1 = relationship("User", foreign_keys=[Participant1ID])
    participant2 = relationship("User", foreign_keys=[Participant2ID])
    winner = relationship("User", foreign_keys=[WinnerID])
    results = relationship("Result", back_populates="match")

    def __init__(self, TournamentID, Participant1ID, Participant2ID, WinnerID, MatchDateTime, Status):
        self.TournamentID = TournamentID
        self.Participant1ID = Participant1ID
        self.Participant2ID = Participant2ID
        self.WinnerID = WinnerID
        self.MatchDateTime = MatchDateTime
        self.Status = Status


# USER MODEL
class User(db.Model):
    __tablename__ = 'users'

    UserID = Column(Integer, primary_key=True, autoincrement=True)
    Username = Column(String(50), nullable=False)
    Email = Column(String(100), nullable=False)
    PhoneNumber = Column(String(255), nullable=False)
    ProfilePicture = Column(String(255))
    Bio = Column(Text)

    bookings = relationship("Booking", back_populates="user")
    organized_tournaments = relationship("Tournament", back_populates="organizer")
    matches_as_participant1 = relationship("Match", foreign_keys=[Match.Participant1ID])
    matches_as_participant2 = relationship("Match", foreign_keys=[Match.Participant2ID])
    matches_as_winner = relationship("Match", foreign_keys=[Match.WinnerID])
    participations = relationship("Participation", back_populates="user")
    orders = relationship("Order", back_populates="user")
    results = relationship("Result", back_populates="participant")

    def __init__(self, Username, Email, PhoneNumber, ProfilePicture=None, Bio=None):
        self.Username = Username
        self.Email = Email
        self.PhoneNumber = PhoneNumber
        self.ProfilePicture = ProfilePicture
        self.Bio = Bio


# JERSEY MODEL
class Jersey(db.Model):
    __tablename__ = 'jersey'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False)
    team = Column(String(120), nullable=False, index=True)
    league = Column(String(120))
    type = Column(String(120))
    home_away_third = Column(String(120))
    sizes = Column(String(120))  # Store sizes as a comma-separated string
    number_of_jerseys = Column(Integer)
    price = Column(Float)
    customizable = Column(Boolean)
    discounted_price = Column(Float)
    image_url = Column(String(255))  # Field to store image URL

    order_items = relationship("OrderItem", back_populates="jersey")

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


# ORDER MODEL
class Order(db.Model):
    __tablename__ = 'orders'

    OrderID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey('users.UserID'), index=True)
    TotalPrice = Column(DECIMAL(precision=10, scale=2), nullable=False)
    Status = Column(String(50), nullable=False)
    CreatedOn = Column(TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())

    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

    def __init__(self, UserID, TotalPrice, Status):
        self.UserID = UserID
        self.TotalPrice = TotalPrice
        self.Status = Status


# ORDER ITEM MODEL
class OrderItem(db.Model):
    __tablename__ = 'orderItems'

    OrderItemID = Column(Integer, primary_key=True, autoincrement=True)
    OrderID = Column(Integer, ForeignKey('orders.OrderID'), nullable=False)
    ProductID = Column(Integer, ForeignKey('jersey.id'), nullable=False)
    Quantity = Column(Integer, nullable=False)
    Price = db.Column(db.DECIMAL(precision=10, scale=2), nullable=False)

    order = relationship("Order", back_populates="order_items")
    jersey = relationship("Jersey", back_populates="order_items")

    def __init__(self, OrderID, ProductID, Quantity, Price):
        self.OrderID = OrderID
        self.ProductID = ProductID
        self.Quantity = Quantity
        self.Price = Price


# TURF MODEL
class Turf(db.Model):
    __tablename__ = 'turfs'

    TurfID = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    location = Column(String(255), nullable=False)
    charges = Column(DECIMAL(precision=10, scale=2), nullable=False)
    availableTimeSlots = Column(Text)

    bookings = relationship("Booking", back_populates="turf")
    images = relationship('TurfImage', back_populates='turf', cascade='all, delete-orphan')
    tournaments = relationship("Tournament", back_populates="turf")

    def __init__(self, name, location, charges, availableTimeSlots):
        self.name = name
        self.location = location
        self.charges = charges
        self.availableTimeSlots = availableTimeSlots


# TURF IMAGE MODEL
class TurfImage(db.Model):
    __tablename__ = 'turfImages'

    turfImageID = Column(Integer, primary_key=True, autoincrement=True)
    TurfID = Column(Integer, ForeignKey('turfs.TurfID'), nullable=False)
    ImageURL = Column(String(1000), nullable=False)

    turf = relationship('Turf', back_populates='images')

    def __init__(self, TurfID, ImageURL):
        self.TurfID = TurfID
        self.ImageURL = ImageURL


# BOOKING MODEL
class Booking(db.Model):
    __tablename__ = 'booking'

    booking_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.UserID'), nullable=False)
    turf_id = Column(Integer, ForeignKey('turfs.TurfID'), nullable=False)
    time_slot = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)

    user = relationship("User", back_populates="bookings")
    turf = relationship("Turf", back_populates="bookings")

    def __init__(self, user_id, turf_id, time_slot, status):
        self.user_id = user_id
        self.turf_id = turf_id
        self.time_slot = time_slot
        self.status = status


# TOURNAMENT MODEL
class Tournament(db.Model):
    __tablename__ = 'tournaments'

    TournamentID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(100), nullable=False)
    Description = Column(Text)
    OrganizerID = Column(Integer, ForeignKey('users.UserID'), index=True)
    TurfID = Column(Integer, ForeignKey('turfs.TurfID'), index=True)
    Date = Column(db.Date)
    StartTime = Column(db.Time)
    EntryFees = Column(DECIMAL(10, 2))

    matches = relationship("Match", back_populates="tournament")
    organizer = relationship("User", back_populates="organized_tournaments")
    turf = relationship("Turf", back_populates="tournaments")
    participations = relationship("Participation", back_populates="tournament")

    def __init__(self, Name, Description, OrganizerID, TurfID, Date, StartTime, EntryFees):
        self.Name = Name
        self.Description = Description
        self.OrganizerID = OrganizerID
        self.TurfID = TurfID
        self.Date = Date
        self.StartTime = StartTime
        self.EntryFees = EntryFees


# PARTICIPATION MODEL
class Participation(db.Model):
    __tablename__ = 'participation'

    ParticipationID = Column(Integer, primary_key=True, autoincrement=True)
    TournamentID = Column(Integer, ForeignKey('tournaments.TournamentID'), index=True, nullable=True)
    UserID = Column(Integer, ForeignKey('users.UserID'), index=True, nullable=True)
    RegistrationDate = Column(TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    Status = Column(String(50), nullable=False)

    tournament = relationship("Tournament", back_populates="participations")
    user = relationship("User", back_populates="participations")

    def __init__(self, TournamentID, UserID, Status):
        self.TournamentID = TournamentID
        self.UserID = UserID
        self.Status = Status


# RESULT MODEL
class Result(db.Model):
    __tablename__ = 'results'

    ResultID = Column(Integer, primary_key=True, autoincrement=True)
    MatchID = Column(Integer, ForeignKey('matches.MatchID'), index=True, nullable=True)
    ParticipantID = Column(Integer, ForeignKey('users.UserID'), index=True, nullable=True)
    Score = Column(Integer, nullable=True)
    IsWinner = Column(Boolean, nullable=True)

    match = relationship("Match", back_populates="results")
    participant = relationship("User", back_populates="results")

    def __init__(self, MatchID, ParticipantID, Score, IsWinner):
        self.MatchID = MatchID
        self.ParticipantID = ParticipantID
        self.Score = Score
        self.IsWinner = IsWinner
