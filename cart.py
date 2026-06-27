from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import get_db
from models import Cart, Product

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('', methods=['GET'])
@jwt_required()
def get_cart():
    user_id = get_jwt_identity()
    db = get_db()
    
    cart = Cart.find_by_user_id(db, user_id)
    
    if not cart:
        cart = {}
        cart['_id'] = str(Cart.create(db, user_id))
        cart['items'] = []
    else:
        cart['_id'] = str(cart['_id'])
        cart['user_id'] = str(cart['user_id'])
    
    return jsonify(cart), 200

@cart_bp.route('/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('product_id') or not data.get('quantity'):
        return jsonify({'error': 'Missing product_id or quantity'}), 400
    
    db = get_db()
    
    product = Product.find_by_id(db, data['product_id'])
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    cart = Cart.find_by_user_id(db, user_id)
    if not cart:
        Cart.create(db, user_id)
    
    Cart.add_item(db, user_id, data['product_id'], data['quantity'])
    return jsonify({'message': 'Item added to cart'}), 200

@cart_bp.route('/remove/<product_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(product_id):
    user_id = get_jwt_identity()
    db = get_db()
    
    Cart.remove_item(db, user_id, product_id)
    return jsonify({'message': 'Item removed from cart'}), 200

@cart_bp.route('/clear', methods=['DELETE'])
@jwt_required()
def clear_cart():
    user_id = get_jwt_identity()
    db = get_db()
    
    Cart.clear(db, user_id)
    return jsonify({'message': 'Cart cleared'}), 200
