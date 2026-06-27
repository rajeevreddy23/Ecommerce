from flask import Blueprint, request, jsonify
from database import get_db
from models import Product

products_bp = Blueprint('products', __name__)

@products_bp.route('', methods=['GET'])
def get_products():
    db = get_db()
    products = Product.find_all(db)
    
    for product in products:
        product['_id'] = str(product['_id'])
    
    return jsonify(products), 200

@products_bp.route('/<product_id>', methods=['GET'])
def get_product(product_id):
    db = get_db()
    product = Product.find_by_id(db, product_id)
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    product['_id'] = str(product['_id'])
    return jsonify(product), 200

@products_bp.route('', methods=['POST'])
def create_product():
    from flask_jwt_extended import jwt_required, get_jwt_identity
    
    @jwt_required()
    def create():
        data = request.get_json()
        
        if not data or not data.get('name') or not data.get('price'):
            return jsonify({'error': 'Missing required fields'}), 400
        
        db = get_db()
        
        product_id = Product.create(
            db,
            data['name'],
            data.get('description', ''),
            data['price'],
            data.get('stock', 0),
            data.get('category', '')
        )
        
        return jsonify({'message': 'Product created', 'product_id': str(product_id)}), 201
    
    return create()

@products_bp.route('/<product_id>', methods=['PUT'])
def update_product(product_id):
    from flask_jwt_extended import jwt_required
    
    @jwt_required()
    def update():
        data = request.get_json()
        db = get_db()
        
        product = Product.find_by_id(db, product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        Product.update(db, product_id, **data)
        return jsonify({'message': 'Product updated'}), 200
    
    return update()

@products_bp.route('/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    from flask_jwt_extended import jwt_required
    
    @jwt_required()
    def delete():
        db = get_db()
        product = Product.find_by_id(db, product_id)
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        Product.delete(db, product_id)
        return jsonify({'message': 'Product deleted'}), 200
    
    return delete()
