# Ecommerce Backend API

A complete Flask-based backend for ecommerce applications with MongoDB, JWT authentication, and Stripe payment integration.

## Features

- **User Authentication**: Register, login, and JWT token verification
- **Product Management**: Full CRUD operations for products
- **Shopping Cart**: Add/remove items, manage cart
- **Order Processing**: Create orders, track order status
- **Payment Integration**: Stripe payment intent creation and confirmation
- **Database**: MongoDB for flexible document storage

## Project Structure

```
backend/
├── app.py                 # Main Flask application
├── database.py            # MongoDB configuration
├── models.py              # Database models (User, Product, Cart, Order)
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── routes/
│   ├── auth.py           # Authentication endpoints
│   ├── products.py       # Product management endpoints
│   ├── cart.py           # Shopping cart endpoints
│   ├── orders.py         # Order processing endpoints
│   └── payments.py       # Payment processing endpoints
└── README.md             # This file
```

## Installation

1. **Clone/Navigate to the project**
   ```bash
   cd backend
   ```

2. **Create a virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your configuration:
   - Set a secure `JWT_SECRET_KEY`
   - Configure `MONGO_URI` (local MongoDB or Atlas)
   - Add your Stripe credentials

5. **Start MongoDB**
   ```bash
   # If using local MongoDB
   mongod
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/verify` - Verify JWT token

### Products
- `GET /api/products` - Get all products
- `GET /api/products/<product_id>` - Get specific product
- `POST /api/products` - Create product (requires auth)
- `PUT /api/products/<product_id>` - Update product (requires auth)
- `DELETE /api/products/<product_id>` - Delete product (requires auth)

### Shopping Cart
- `GET /api/cart` - Get user's cart (requires auth)
- `POST /api/cart/add` - Add item to cart (requires auth)
- `DELETE /api/cart/remove/<product_id>` - Remove item (requires auth)
- `DELETE /api/cart/clear` - Clear entire cart (requires auth)

### Orders
- `GET /api/orders` - Get user's orders (requires auth)
- `GET /api/orders/<order_id>` - Get specific order (requires auth)
- `POST /api/orders` - Create order (requires auth)
- `PUT /api/orders/<order_id>/status` - Update order status (requires auth)

### Payments
- `POST /api/payments/create-payment-intent` - Create Stripe payment intent (requires auth)
- `POST /api/payments/confirm-payment` - Confirm payment (requires auth)
- `GET /api/payments/payment-status/<order_id>` - Get payment status (requires auth)

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. After login, include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## Example Usage

### Register User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123","name":"John Doe"}'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'
```

### Get Products
```bash
curl http://localhost:5000/api/products
```

### Create Product
```bash
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"name":"Laptop","description":"High-end laptop","price":999.99,"stock":10,"category":"Electronics"}'
```

### Add to Cart
```bash
curl -X POST http://localhost:5000/api/cart/add \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"product_id":"<product_id>","quantity":2}'
```

## Environment Variables

Create a `.env` file with:
- `JWT_SECRET_KEY` - Secret key for JWT encoding (change in production!)
- `MONGO_URI` - MongoDB connection string
- `STRIPE_SECRET_KEY` - Stripe secret key
- `STRIPE_PUBLISHABLE_KEY` - Stripe publishable key
- `FLASK_ENV` - Development or production
- `FLASK_DEBUG` - Enable debug mode

## Dependencies

- Flask 2.3.0
- Flask-CORS 4.0.0
- Flask-JWT-Extended 4.4.4
- Flask-Bcrypt 1.0.1
- PyMongo 4.3.3
- python-dotenv 1.0.0
- Stripe 5.4.0

## Notes

- All passwords are hashed using bcrypt
- Dates and times are stored in UTC
- MongoDB ObjectIds are converted to strings in API responses
- CORS is enabled for frontend integration
- Update `.env` with real values before production deployment
