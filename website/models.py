"""
Database Models for StyleVault E-Commerce Website
Modular Python Implementation using Flask-SQLAlchemy
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User model for authentication and account management."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    orders = db.relationship('Order', backref='user', lazy=True)
    cart_items = db.relationship('CartItem', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'


class Category(db.Model):
    """Product category model."""
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    slug = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)

    products = db.relationship('Product', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'


class Product(db.Model):
    """Product model for the e-commerce store."""
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    sale_price = db.Column(db.Float, nullable=True)
    brand = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(500))
    stock = db.Column(db.Integer, default=0)
    sizes = db.Column(db.String(200))  # Comma-separated sizes
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    cart_items = db.relationship('CartItem', backref='product', lazy=True)
    order_items = db.relationship('OrderItem', backref='product', lazy=True)

    @property
    def effective_price(self):
        return self.sale_price if self.sale_price else self.price

    def __repr__(self):
        return f'<Product {self.name}>'


class CartItem(db.Model):
    """Shopping cart item model."""
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    size = db.Column(db.String(20))
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def subtotal(self):
        return self.product.effective_price * self.quantity


class Order(db.Model):
    """Order model."""
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pending')
    shipping_address = db.Column(db.Text)
    shipping_city = db.Column(db.String(100))
    shipping_postcode = db.Column(db.String(20))
    shipping_country = db.Column(db.String(100), default='United Kingdom')
    payment_method = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship('OrderItem', backref='order', lazy=True)

    def __repr__(self):
        return f'<Order {self.id} - {self.status}>'


class OrderItem(db.Model):
    """Order line item model."""
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    size = db.Column(db.String(20))
    price_at_purchase = db.Column(db.Float, nullable=False)

    @property
    def subtotal(self):
        return self.price_at_purchase * self.quantity


class ContactMessage(db.Model):
    """Contact form message model."""
    __tablename__ = 'contact_messages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
