import logging
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from database import db
# Create Flask application
app = Flask(__name__)
CORS(app)

# MySQL Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://sql12707487:NdNVc1wexA@sql12.freesqldatabase.com:3306/sql12707487'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # Enable SQL query logging
db.init_app(app)


# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Import models
from models import Jersey, Order, Booking, Match, User ,Turf, TurfImage, Tournament, Result, Participation, OrderItem

# Import and register blueprints
from routes.jersey_routes import jersey_routes
from routes.orders_routes import order_routes
from routes.mongo_routes import mongo_routes
from routes.booking_routes import booking_routes
from routes.user_routes import user_routes
from routes.turf_routes import turf_routes

app.register_blueprint(jersey_routes)
app.register_blueprint(order_routes)
app.register_blueprint(booking_routes)
app.register_blueprint(mongo_routes)
app.register_blueprint(user_routes)
app.register_blueprint(turf_routes)

# # Create tables if they don't exist
# with app.app_context():
#     logger.debug("Creating database tables if they don't exist...")
#     db.create_all()
#     logger.debug("Tables created.")

# # Test query to verify table creation
# with app.app_context():
#     try:
#         jersey_count = db.session.query(Jersey).count()
#         orders_count = db.session.query(Order).count()
#         logger.debug(f"Jersey table has {jersey_count} entries.")
#         logger.debug(f"Orders table has {orders_count} entries.")
#     except Exception as e:
#         logger.error(f"Error querying tables: {e}")

if __name__ == '__main__':
    app.run(debug=True)
