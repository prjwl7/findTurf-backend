from flask import Blueprint, jsonify, request
from cruds import create_order, get_orders, delete_order

orders_routes = Blueprint('orders_routes', __name__)

@orders_routes.route('/api/orders', methods=['POST'])
def add_order():
    try:
        data = request.get_json()
        new_order = create_order(data)
        return jsonify({'message': 'Order added successfully', 'order': new_order.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@orders_routes.route('/api/orders', methods=['GET'])
def list_orders():
    try:
        orders = get_orders()
        orders_list = [{
            'id': order.id,
            'name': order.name,
            'email': order.email,
            'phoneNumber': order.phoneNumber,
            'jersey': order.jersey,
            'size': order.size,
            'quantity': order.quantity,
            'amount': order.amount,
            'address': order.address
        } for order in orders]
        return jsonify(orders_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@orders_routes.route('/api/orders/<int:order_id>', methods=['DELETE'])
def remove_order(order_id):
    try:
        deleted_order = delete_order(order_id)
        return jsonify({'message': 'Order deleted successfully', 'order': deleted_order.id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
