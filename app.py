import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from database import init_db

load_dotenv()

app = Flask(__name__)

# Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/ecommerce')

# Initialize extensions
CORS(app)
jwt = JWTManager(app)
init_db(app)

# Import and register blueprints
from routes.auth import auth_bp
from routes.products import products_bp
from routes.cart import cart_bp
from routes.orders import orders_bp
from routes.payments import payments_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(products_bp, url_prefix='/api/products')
app.register_blueprint(cart_bp, url_prefix='/api/cart')
app.register_blueprint(orders_bp, url_prefix='/api/orders')
app.register_blueprint(payments_bp, url_prefix='/api/payments')

@app.route('/api/health', methods=['GET'])
def health_check():
    return {'status': 'Backend is running'}, 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
