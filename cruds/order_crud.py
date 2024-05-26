from models import db, Order, OrderItem

def create_order(user_id, total_price, status, order_items):
    new_order = Order(UserID=user_id, TotalPrice=total_price, Status=status)
    db.session.add(new_order)
    db.session.commit()

    # Create OrderItems
    for item in order_items:
        new_order_item = OrderItem(
            OrderID=new_order.OrderID,
            ProductID=item['ProductID'],
            Quantity=item['Quantity'],
            Price=item['Price'],
            Status=item.get('Status', 'pending')  # Assuming default status is 'pending'
        )
        db.session.add(new_order_item)
    
    db.session.commit()
    return new_order

def get_orders():
    return Order.query.all()

def get_order_by_id(order_id):
    return Order.query.get(order_id)

def update_order(order_id, data):
    order = Order.query.get(order_id)
    if not order:
        raise ValueError("Order not found")

    # Update order attributes
    if 'UserID' in data:
        order.UserID = data['UserID']
    if 'TotalPrice' in data:
        order.TotalPrice = data['TotalPrice']
    if 'Status' in data:
        order.Status = data['Status']

    db.session.commit()
    return order

def delete_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        raise ValueError("Order not found")

    db.session.delete(order)
    db.session.commit()
    return order
