from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import get_db
from models import Order, Cart

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('', methods=['GET'])
@jwt_required()
def get_user_orders():
    user_id = get_jwt_identity()
    db = get_db()
    
    orders = Order.find_by_user_id(db, user_id)
    
    for order in orders:
        order['_id'] = str(order['_id'])
        order['user_id'] = str(order['user_id'])
        for item in order.get('items', []):
            item['product_id'] = str(item['product_id'])
    
    return jsonify(orders), 200

@orders_bp.route('/<order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    user_id = get_jwt_identity()
    db = get_db()
    
    order = Order.find_by_id(db, order_id)
    
    if not order or str(order['user_id']) != user_id:
        return jsonify({'error': 'Order not found'}), 404
    
    order['_id'] = str(order['_id'])
    order['user_id'] = str(order['user_id'])
    for item in order.get('items', []):
        item['product_id'] = str(item['product_id'])
    
    return jsonify(order), 200

@orders_bp.route('', methods=['POST'])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('shipping_address'):
        return jsonify({'error': 'Missing shipping address'}), 400
    
    db = get_db()
    
    cart = Cart.find_by_user_id(db, user_id)
    if not cart or not cart.get('items'):
        return jsonify({'error': 'Cart is empty'}), 400
    
    items = cart['items']
    total_price = 0
    
    for item in items:
        product = db['products'].find_one({'_id': item['product_id']})
        if product:
            total_price += product['price'] * item['quantity']
    
    order_id = Order.create(
        db,
        user_id,
        items,
        total_price,
        data['shipping_address']
    )
    
    Cart.clear(db, user_id)
    
    return jsonify({
        'message': 'Order created',
        'order_id': str(order_id),
        'total_price': total_price
    }), 201

@orders_bp.route('/<order_id>/status', methods=['PUT'])
@jwt_required()
def update_order_status(order_id):
    data = request.get_json()
    
    if not data or not data.get('status'):
        return jsonify({'error': 'Missing status'}), 400
    
    db = get_db()
    order = Order.find_by_id(db, order_id)
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    Order.update_status(db, order_id, data['status'])
    return jsonify({'message': 'Order status updated'}), 200
