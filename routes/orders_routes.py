from flask import Blueprint, jsonify, request
from cruds.order_crud import create_order, get_orders, get_order_by_id, update_order, delete_order
from models import Order, OrderItem, User
order_routes = Blueprint('order_routes', __name__)

@order_routes.route('/api/orders', methods=['POST'])
def add_order():
    data = request.get_json()
    try:
        user_id = data['UserID']
        total_price = data['TotalPrice']
        status = data['Status']
        order_items = data['OrderItems']  # Get the order items from the request

        new_order = create_order(user_id, total_price, status, order_items)
        return jsonify({'message': 'Order added successfully', 'order_id': new_order.OrderID}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@order_routes.route('/api/orders', methods=['GET'])
def list_orders():
    orders = get_orders()
    orders_list = [{'OrderID': order.OrderID, 'UserID': order.UserID, 'TotalPrice': float(order.TotalPrice), 'Status': order.Status, 'CreatedOn': order.CreatedOn} for order in orders]
    return jsonify(orders_list), 200

@order_routes.route('/api/orders/<int:user_id>', methods=['GET'])
def get_orders_by_user(user_id):
    try:
        orders = Order.query.filter_by(UserID=user_id).all()

        if not orders:
            return jsonify({'message': 'No orders found for this user'}), 404

        orders_list = []
        for order in orders:
            order_details = {
                'OrderID': order.OrderID,
                'UserID': order.UserID,
                'Username': order.user.Username,
                'Email': order.user.Email,
                'PhoneNumber': order.user.PhoneNumber,
                'OrderItems': []
            }

            order_items = OrderItem.query.filter_by(OrderID=order.OrderID).all()
            for order_item in order_items:
                order_item_details = {
                    'OrderItemID': order_item.OrderItemID,
                    'ProductID': order_item.ProductID,
                    'ProductName': order_item.product.ProductName,
                    'Quantity': order_item.Quantity,
                    'Price': order_item.Price,
                    'Status': order_item.Status
                }
                order_details['OrderItems'].append(order_item_details)

            orders_list.append(order_details)

        return jsonify(orders_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@order_routes.route('/api/orders/<int:order_id>', methods=['PUT'])
def update_an_order(order_id):
    data = request.get_json()
    try:
        updated_order = update_order(order_id, data)
        return jsonify({'message': 'Order updated successfully', 'order_id': updated_order.OrderID}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@order_routes.route('/api/orders/<int:order_id>', methods=['DELETE'])
def remove_an_order(order_id):
    try:
        deleted_order = delete_order(order_id)
        return jsonify({'message': 'Order deleted successfully', 'order_id': deleted_order.OrderID}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@order_routes.route('/api/orders/user/<string:user_email>', methods=['GET'])
def get_orders_by_user_email(user_email):
    try:
        user = User.query.filter_by(Email=user_email).first()

        if not user:
            return jsonify({'message': 'User not found'}), 404

        orders = Order.query.filter_by(UserID=user.UserID).all()

        if not orders:
            return jsonify({'message': 'No orders found for this user'}), 404

        orders_list = []
        for order in orders:
            order_details = {
                'OrderID': order.OrderID,
                'UserID': order.UserID,
                'Username': user.Username,
                'Email': user.Email,
                'PhoneNumber': user.PhoneNumber,
                'OrderItems': []
            }

            order_items = OrderItem.query.filter_by(OrderID=order.OrderID).all()
            for order_item in order_items:
                order_item_details = {
                    'OrderItemID': order_item.OrderItemID,
                    'ProductID': order_item.ProductID,
                    'ProductName': order_item.jersey.name,
                    'Quantity': order_item.Quantity,
                    'Price': order_item.Price,
                }
                order_details['OrderItems'].append(order_item_details)

            orders_list.append(order_details)

        return jsonify(orders_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500