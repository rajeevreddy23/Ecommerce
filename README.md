# 🛍️ Ecommerce Platform

A full-stack e-commerce application with a responsive HTML/CSS frontend and a robust Flask backend featuring authentication, product management, shopping cart, order processing, and Stripe payment integration.

## ✨ Features

### Frontend
- 📱 Responsive web design
- 🏠 Home page with navigation
- 🛍️ Product listings and details
- 📦 Contact page
- 🎨 Modern CSS styling

### Backend
- 👤 **User Authentication** - Register, login, JWT token verification
- 📦 **Product Management** - Full CRUD operations, product catalog
- 🛒 **Shopping Cart** - Add/remove items, cart management
- 📋 **Order Processing** - Create orders, track status
- 💳 **Payment Integration** - Stripe payment system
- 🔐 **Security** - JWT authentication, bcrypt password hashing
- 🗄️ **Database** - MongoDB for flexible document storage

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3

### Backend
- **Framework**: Flask 2.3.0
- **Database**: MongoDB
- **Authentication**: JWT (Flask-JWT-Extended)
- **Password Hashing**: Bcrypt
- **Payments**: Stripe API
- **CORS**: Flask-CORS
- **Environment**: Python-Dotenv

## 📂 Project Structure

```
Ecommerce/
├── index.html             # Home page
├── products.html          # Products page
├── contact.html           # Contact page
├── home.html              # Additional home page
├── style.css              # Stylesheet
│
└── backend/
    ├── app.py             # Main Flask application
    ├── database.py        # MongoDB configuration
    ├── models.py          # Data models
    ├── requirements.txt   # Python dependencies
    ├── README.md          # Backend documentation
    │
    └── routes/
        ├── auth.py        # Authentication endpoints
        ├── products.py    # Product management
        ├── cart.py        # Shopping cart
        ├── orders.py      # Order processing
        └── payments.py    # Payment processing
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- MongoDB
- Node.js (optional, for frontend tooling)
- Stripe account for payment testing

### Backend Installation

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file** with your configuration
   ```bash
   # Add the following variables:
   MONGODB_URI=your_mongodb_connection_string
   JWT_SECRET_KEY=your_secret_key
   STRIPE_SECRET_KEY=your_stripe_secret_key
   FLASK_ENV=development
   ```

5. **Run the backend server**
   ```bash
   python app.py
   ```
   The server will start at `http://localhost:5000`

### Frontend Setup

1. Open `index.html` in your browser or serve using a local server:
   ```bash
   # Using Python:
   python -m http.server 8000
   
   # Or use any other local server
   ```

2. Access the frontend at `http://localhost:8000`

## 📚 API Endpoints

### Authentication (`/api/auth`)
- `POST /register` - Register new user
- `POST /login` - Login user
- `GET /verify` - Verify JWT token

### Products (`/api/products`)
- `GET /` - Get all products
- `GET /<id>` - Get product by ID
- `POST /` - Create product (admin)
- `PUT /<id>` - Update product (admin)
- `DELETE /<id>` - Delete product (admin)

### Cart (`/api/cart`)
- `GET /` - Get user cart
- `POST /add` - Add item to cart
- `DELETE /remove` - Remove item from cart
- `PUT /update` - Update cart item quantity

### Orders (`/api/orders`)
- `GET /` - Get user orders
- `POST /` - Create new order
- `GET /<id>` - Get order details
- `PUT /<id>` - Update order status

### Payments (`/api/payments`)
- `POST /intent` - Create payment intent
- `POST /confirm` - Confirm payment

## 🔑 Environment Variables

Create a `.env` file in the backend directory:

```
MONGODB_URI=mongodb://localhost:27017/ecommerce
JWT_SECRET_KEY=your_jwt_secret_key_here
STRIPE_SECRET_KEY=sk_test_your_stripe_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_key
FLASK_ENV=development
FLASK_DEBUG=1
```

## 🧪 Testing

### Test the Backend API
```bash
# Using curl or Postman:
curl http://localhost:5000/api/products


```

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For support, please open an issue on GitHub or contact the project maintainers.

---
