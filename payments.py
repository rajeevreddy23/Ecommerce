from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import stripe
import os
from database import get_db
from models import Order

payments_bp = Blueprint('payments', __name__)

stripe.api_key = os.getenv('STRIPE_SECRET_KEY', 'your-stripe-secret-key')

@payments_bp.route('/create-payment-intent', methods=['POST'])
@jwt_required()
def create_payment_intent():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('order_id'):
        return jsonify({'error': 'Missing order_id'}), 400
    
    db = get_db()
    order = Order.find_by_id(db, data['order_id'])
    
    if not order or str(order['user_id']) != user_id:
        return jsonify({'error': 'Order not found'}), 404
    
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(order['total_price'] * 100),
            currency='usd',
            metadata={'order_id': str(order['_id'])}
        )
        
        return jsonify({
            'client_secret': intent.client_secret,
            'payment_intent_id': intent.id
        }), 200
    
    except stripe.error.StripeError as e:
        return jsonify({'error': str(e)}), 500

@payments_bp.route('/confirm-payment', methods=['POST'])
@jwt_required()
def confirm_payment():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('order_id') or not data.get('payment_intent_id'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    db = get_db()
    order = Order.find_by_id(db, data['order_id'])
    
    if not order or str(order['user_id']) != user_id:
        return jsonify({'error': 'Order not found'}), 404
    
    try:
        intent = stripe.PaymentIntent.retrieve(data['payment_intent_id'])
        
        if intent.status == 'succeeded':
            Order.update_payment_status(db, data['order_id'], 'paid')
            Order.update_status(db, data['order_id'], 'processing')
            
            return jsonify({
                'message': 'Payment successful',
                'payment_status': 'paid'
            }), 200
        else:
            return jsonify({
                'error': 'Payment not completed',
                'status': intent.status
            }), 400
    
    except stripe.error.StripeError as e:
        return jsonify({'error': str(e)}), 500

@payments_bp.route('/payment-status/<order_id>', methods=['GET'])
@jwt_required()
def get_payment_status(order_id):
    user_id = get_jwt_identity()
    db = get_db()
    
    order = Order.find_by_id(db, order_id)
    
    if not order or str(order['user_id']) != user_id:
        return jsonify({'error': 'Order not found'}), 404
    
    return jsonify({
        'order_id': str(order['_id']),
        'payment_status': order.get('payment_status', 'unpaid'),
        'total_price': order['total_price']
    }), 200
