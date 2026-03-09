from datetime import datetime
from bson.objectid import ObjectId

class User:
    collection_name = 'users'
    
    @staticmethod
    def create(db, email, password, name):
        from flask_bcrypt import Bcrypt
        bcrypt = Bcrypt()
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        
        user_data = {
            'email': email,
            'password': hashed_pw,
            'name': name,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = db[User.collection_name].insert_one(user_data)
        return result.inserted_id

    @staticmethod
    def find_by_email(db, email):
        return db[User.collection_name].find_one({'email': email})

    @staticmethod
    def find_by_id(db, user_id):
        return db[User.collection_name].find_one({'_id': ObjectId(user_id)})


class Product:
    collection_name = 'products'
    
    @staticmethod
    def create(db, name, description, price, stock, category):
        product_data = {
            'name': name,
            'description': description,
            'price': price,
            'stock': stock,
            'category': category,
            'created_at': datetime.utcnow()
        }
        result = db[Product.collection_name].insert_one(product_data)
        return result.inserted_id

    @staticmethod
    def find_all(db):
        return list(db[Product.collection_name].find({}))

    @staticmethod
    def find_by_id(db, product_id):
        return db[Product.collection_name].find_one({'_id': ObjectId(product_id)})

    @staticmethod
    def update(db, product_id, **kwargs):
        db[Product.collection_name].update_one(
            {'_id': ObjectId(product_id)},
            {'$set': {**kwargs, 'updated_at': datetime.utcnow()}}
        )

    @staticmethod
    def delete(db, product_id):
        db[Product.collection_name].delete_one({'_id': ObjectId(product_id)})


class Cart:
    collection_name = 'carts'
    
    @staticmethod
    def create(db, user_id):
        cart_data = {
            'user_id': ObjectId(user_id),
            'items': [],
            'created_at': datetime.utcnow()
        }
        result = db[Cart.collection_name].insert_one(cart_data)
        return result.inserted_id

    @staticmethod
    def find_by_user_id(db, user_id):
        return db[Cart.collection_name].find_one({'user_id': ObjectId(user_id)})

    @staticmethod
    def add_item(db, user_id, product_id, quantity):
        db[Cart.collection_name].update_one(
            {'user_id': ObjectId(user_id)},
            {'$push': {'items': {'product_id': ObjectId(product_id), 'quantity': quantity}}}
        )

    @staticmethod
    def remove_item(db, user_id, product_id):
        db[Cart.collection_name].update_one(
            {'user_id': ObjectId(user_id)},
            {'$pull': {'items': {'product_id': ObjectId(product_id)}}}
        )

    @staticmethod
    def clear(db, user_id):
        db[Cart.collection_name].update_one(
            {'user_id': ObjectId(user_id)},
            {'$set': {'items': []}}
        )


class Order:
    collection_name = 'orders'
    
    @staticmethod
    def create(db, user_id, items, total_price, shipping_address):
        order_data = {
            'user_id': ObjectId(user_id),
            'items': items,
            'total_price': total_price,
            'status': 'pending',
            'shipping_address': shipping_address,
            'payment_status': 'unpaid',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = db[Order.collection_name].insert_one(order_data)
        return result.inserted_id

    @staticmethod
    def find_by_user_id(db, user_id):
        return list(db[Order.collection_name].find({'user_id': ObjectId(user_id)}))

    @staticmethod
    def find_by_id(db, order_id):
        return db[Order.collection_name].find_one({'_id': ObjectId(order_id)})

    @staticmethod
    def update_status(db, order_id, status):
        db[Order.collection_name].update_one(
            {'_id': ObjectId(order_id)},
            {'$set': {'status': status, 'updated_at': datetime.utcnow()}}
        )

    @staticmethod
    def update_payment_status(db, order_id, payment_status):
        db[Order.collection_name].update_one(
            {'_id': ObjectId(order_id)},
            {'$set': {'payment_status': payment_status, 'updated_at': datetime.utcnow()}}
        )
