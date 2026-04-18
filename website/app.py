"""
StyleVault E-Commerce Website - Main Flask Application
Modular Python Implementation with Blueprint Architecture
"""

import os
import secrets
from flask import (Flask, render_template, redirect, url_for, request,
                   flash, session, jsonify)
from flask_login import (LoginManager, login_user, logout_user,
                         login_required, current_user)
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Category, Product, CartItem, Order, OrderItem, ContactMessage

# Load .env file when running locally
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def create_app():
    """Application factory pattern for creating the Flask app."""
    app = Flask(__name__)

    # ── Security ─────────────────────────────────────────────────
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))

    # ── Database ──────────────────────────────────────────────────
    # Railway provides DATABASE_URL as mysql://... — convert to PyMySQL driver
    database_url = os.environ.get('DATABASE_URL', '')
    if database_url:
        # Convert mysql:// to mysql+pymysql:// for SQLAlchemy
        if database_url.startswith('mysql://'):
            database_url = database_url.replace('mysql://', 'mysql+pymysql://', 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # Local fallback: SQLite
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stylevault.db'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_recycle': 280,
        'pool_pre_ping': True,
        'pool_timeout': 20,
        'pool_size': 5,
        'max_overflow': 2,
    }

    db.init_app(app)

    # ── Static files via WhiteNoise (production) ────────────────
    if os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('USE_WHITENOISE'):
        try:
            from whitenoise import WhiteNoise
            app.wsgi_app = WhiteNoise(app.wsgi_app,
                                      root=os.path.join(os.path.dirname(__file__), 'static'),
                                      prefix='static')
        except ImportError:
            pass

    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ── Context Processor ───────────────────────────────────────
    @app.context_processor
    def inject_globals():
        categories = Category.query.all()
        cart_count = 0
        if current_user.is_authenticated:
            cart_count = CartItem.query.filter_by(user_id=current_user.id).count()
        return dict(categories=categories, cart_count=cart_count)

    # ── Home Page ───────────────────────────────────────────────
    @app.route('/')
    def index():
        featured = Product.query.filter_by(is_featured=True).limit(8).all()
        new_arrivals = Product.query.order_by(Product.created_at.desc()).limit(4).all()
        return render_template('index.html', featured=featured, new_arrivals=new_arrivals)

    # ── Product Routes ──────────────────────────────────────────
    @app.route('/collection')
    @app.route('/collection/<slug>')
    def products(slug=None):
        sort = request.args.get('sort', 'newest')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        size_filter = request.args.get('size')

        query = Product.query
        category = None

        if slug:
            category = Category.query.filter_by(slug=slug).first_or_404()
            query = query.filter_by(category_id=category.id)

        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        if size_filter:
            query = query.filter(Product.sizes.contains(size_filter))

        if sort == 'price_low':
            query = query.order_by(Product.price.asc())
        elif sort == 'price_high':
            query = query.order_by(Product.price.desc())
        elif sort == 'name_az':
            query = query.order_by(Product.name.asc())
        elif sort == 'name_za':
            query = query.order_by(Product.name.desc())
        else:
            query = query.order_by(Product.created_at.desc())

        products_list = query.all()
        return render_template('products.html', products=products_list,
                               category=category, current_sort=sort)

    @app.route('/product/<slug>')
    def product_detail(slug):
        product = Product.query.filter_by(slug=slug).first_or_404()
        related = Product.query.filter(
            Product.category_id == product.category_id,
            Product.id != product.id
        ).limit(4).all()
        return render_template('product_detail.html', product=product, related=related)

    @app.route('/search')
    def search():
        q = request.args.get('q', '').strip()
        if not q:
            return redirect(url_for('index'))
        results = Product.query.filter(
            db.or_(Product.name.ilike(f'%{q}%'),
                   Product.brand.ilike(f'%{q}%'),
                   Product.description.ilike(f'%{q}%'))
        ).all()
        return render_template('products.html', products=results,
                               search_query=q, category=None, current_sort='newest')

    # ── Authentication Routes ───────────────────────────────────
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        if request.method == 'POST':
            email = request.form.get('email', '').strip().lower()
            password = request.form.get('password', '')
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password_hash, password):
                login_user(user)
                flash('Welcome back!', 'success')
                next_page = request.args.get('next')
                return redirect(next_page or url_for('index'))
            flash('Invalid email or password.', 'danger')
        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        if request.method == 'POST':
            email = request.form.get('email', '').strip().lower()
            password = request.form.get('password', '')
            first_name = request.form.get('first_name', '').strip()
            last_name = request.form.get('last_name', '').strip()

            if not all([email, password, first_name, last_name]):
                flash('All fields are required.', 'danger')
                return render_template('register.html')

            if len(password) < 6:
                flash('Password must be at least 6 characters.', 'danger')
                return render_template('register.html')

            if User.query.filter_by(email=email).first():
                flash('Email already registered.', 'danger')
                return render_template('register.html')

            user = User(
                email=email,
                password_hash=generate_password_hash(password),
                first_name=first_name,
                last_name=last_name
            )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Account created successfully!', 'success')
            return redirect(url_for('index'))
        return render_template('register.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('index'))

    # ── Cart Routes ─────────────────────────────────────────────
    @app.route('/cart')
    @login_required
    def cart():
        items = CartItem.query.filter_by(user_id=current_user.id).all()
        total = sum(item.subtotal for item in items)
        return render_template('cart.html', items=items, total=total)

    @app.route('/cart/add/<int:product_id>', methods=['POST'])
    @login_required
    def add_to_cart(product_id):
        product = Product.query.get_or_404(product_id)
        size = request.form.get('size', 'M')
        quantity = int(request.form.get('quantity', 1))

        if quantity < 1:
            quantity = 1

        existing = CartItem.query.filter_by(
            user_id=current_user.id, product_id=product_id, size=size
        ).first()

        if existing:
            existing.quantity += quantity
        else:
            item = CartItem(
                user_id=current_user.id,
                product_id=product_id,
                quantity=quantity,
                size=size
            )
            db.session.add(item)

        db.session.commit()
        flash(f'{product.name} added to cart!', 'success')
        return redirect(request.referrer or url_for('products'))

    @app.route('/cart/update/<int:item_id>', methods=['POST'])
    @login_required
    def update_cart(item_id):
        item = CartItem.query.get_or_404(item_id)
        if item.user_id != current_user.id:
            return redirect(url_for('cart'))
        quantity = int(request.form.get('quantity', 1))
        if quantity < 1:
            db.session.delete(item)
        else:
            item.quantity = quantity
        db.session.commit()
        return redirect(url_for('cart'))

    @app.route('/cart/remove/<int:item_id>')
    @login_required
    def remove_from_cart(item_id):
        item = CartItem.query.get_or_404(item_id)
        if item.user_id == current_user.id:
            db.session.delete(item)
            db.session.commit()
            flash('Item removed from cart.', 'info')
        return redirect(url_for('cart'))

    # ── Checkout Routes ─────────────────────────────────────────
    @app.route('/checkout', methods=['GET', 'POST'])
    @login_required
    def checkout():
        items = CartItem.query.filter_by(user_id=current_user.id).all()
        if not items:
            flash('Your cart is empty.', 'warning')
            return redirect(url_for('products'))

        total = sum(item.subtotal for item in items)

        if request.method == 'POST':
            order = Order(
                user_id=current_user.id,
                total=total,
                shipping_address=request.form.get('address', ''),
                shipping_city=request.form.get('city', ''),
                shipping_postcode=request.form.get('postcode', ''),
                shipping_country=request.form.get('country', 'United Kingdom'),
                payment_method=request.form.get('payment_method', 'card'),
                status='confirmed'
            )
            db.session.add(order)
            db.session.flush()

            for cart_item in items:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=cart_item.product_id,
                    quantity=cart_item.quantity,
                    size=cart_item.size,
                    price_at_purchase=cart_item.product.effective_price
                )
                db.session.add(order_item)
                cart_item.product.stock -= cart_item.quantity
                db.session.delete(cart_item)

            db.session.commit()
            flash('Order placed successfully! Thank you for your purchase.', 'success')
            return redirect(url_for('order_confirmation', order_id=order.id))

        return render_template('checkout.html', items=items, total=total)

    @app.route('/order/<int:order_id>')
    @login_required
    def order_confirmation(order_id):
        order = Order.query.get_or_404(order_id)
        if order.user_id != current_user.id:
            return redirect(url_for('index'))
        return render_template('order_confirmation.html', order=order)

    # ── Contact Route ───────────────────────────────────────────
    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            subject = request.form.get('subject', '').strip()
            message = request.form.get('message', '').strip()

            if not all([name, email, subject, message]):
                flash('All fields are required.', 'danger')
                return render_template('contact.html')

            msg = ContactMessage(name=name, email=email,
                                 subject=subject, message=message)
            db.session.add(msg)
            db.session.commit()
            flash('Message sent! We will get back to you soon.', 'success')
            return redirect(url_for('contact'))

        return render_template('contact.html')

    # ── About Route ─────────────────────────────────────────────
    @app.route('/about')
    def about():
        return render_template('about.html')

    # ── Admin Dashboard ─────────────────────────────────────────
    @app.route('/admin')
    @login_required
    def admin_dashboard():
        from sqlalchemy import func
        stats = {
            'total_products': Product.query.count(),
            'total_orders': Order.query.count(),
            'total_users': User.query.count(),
            'total_messages': ContactMessage.query.count(),
        }
        recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
        products = Product.query.order_by(Product.created_at.desc()).limit(10).all()
        return render_template('admin.html', stats=stats,
                               recent_orders=recent_orders, products=products)

    # ── Admin Analytics ─────────────────────────────────────────
    @app.route('/admin/analytics')
    @login_required
    def admin_analytics():
        from sqlalchemy import func
        stats = {
            'total_products': Product.query.count(),
            'total_orders': Order.query.count(),
            'total_users': User.query.count(),
            'total_messages': ContactMessage.query.count(),
        }
        total_revenue = db.session.query(func.sum(Order.total)).scalar() or 0
        confirmed_orders = Order.query.filter_by(status='confirmed').count()
        pending_orders = Order.query.filter_by(status='pending').count()
        # Top 5 products by order count
        top_products = db.session.query(
            Product.name, func.sum(OrderItem.quantity).label('qty')
        ).join(OrderItem).group_by(Product.id).order_by(db.text('qty DESC')).limit(5).all()
        # Orders by category
        category_sales = db.session.query(
            Category.name, func.count(OrderItem.id).label('count')
        ).join(Product, Product.category_id == Category.id)\
         .join(OrderItem, OrderItem.product_id == Product.id)\
         .group_by(Category.id).all()
        return render_template('admin_analytics.html',
                               stats=stats, total_revenue=total_revenue,
                               confirmed_orders=confirmed_orders,
                               pending_orders=pending_orders,
                               top_products=top_products,
                               category_sales=category_sales)

    # ── Admin Product Management ─────────────────────────────────
    @app.route('/admin/products')
    @login_required
    def admin_products():
        products = Product.query.order_by(Product.created_at.desc()).all()
        categories = Category.query.all()
        return render_template('admin_products.html', products=products, categories=categories)

    @app.route('/admin/products/add', methods=['GET', 'POST'])
    @login_required
    def admin_add_product():
        categories = Category.query.all()
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            description = request.form.get('description', '').strip()
            price = float(request.form.get('price', 0))
            sale_price_raw = request.form.get('sale_price', '').strip()
            sale_price = float(sale_price_raw) if sale_price_raw else None
            brand = request.form.get('brand', '').strip()
            image_url = request.form.get('image_url', '').strip()
            stock = int(request.form.get('stock', 0))
            sizes = request.form.get('sizes', '').strip()
            category_id = int(request.form.get('category_id', 1))
            is_featured = 'is_featured' in request.form
            # Generate slug
            import re
            slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
            # Ensure unique slug
            existing = Product.query.filter_by(slug=slug).first()
            if existing:
                slug = f'{slug}-{Product.query.count() + 1}'
            product = Product(
                name=name, slug=slug, description=description,
                price=price, sale_price=sale_price, brand=brand,
                image_url=image_url, stock=stock, sizes=sizes,
                category_id=category_id, is_featured=is_featured
            )
            db.session.add(product)
            db.session.commit()
            flash(f'Product "{name}" added successfully!', 'success')
            return redirect(url_for('admin_products'))
        return render_template('admin_add_product.html', categories=categories)

    @app.route('/admin/products/<int:product_id>/edit', methods=['GET', 'POST'])
    @login_required
    def admin_edit_product(product_id):
        product = Product.query.get_or_404(product_id)
        categories = Category.query.all()
        if request.method == 'POST':
            product.name = request.form.get('name', product.name).strip()
            product.description = request.form.get('description', product.description).strip()
            product.price = float(request.form.get('price', product.price))
            sale_price_raw = request.form.get('sale_price', '').strip()
            product.sale_price = float(sale_price_raw) if sale_price_raw else None
            product.brand = request.form.get('brand', product.brand).strip()
            product.image_url = request.form.get('image_url', product.image_url).strip()
            product.stock = int(request.form.get('stock', product.stock))
            product.sizes = request.form.get('sizes', product.sizes).strip()
            product.category_id = int(request.form.get('category_id', product.category_id))
            product.is_featured = 'is_featured' in request.form
            db.session.commit()
            flash(f'Product "{product.name}" updated successfully!', 'success')
            return redirect(url_for('admin_products'))
        return render_template('admin_edit_product.html', product=product, categories=categories)

    @app.route('/admin/products/<int:product_id>/delete', methods=['POST'])
    @login_required
    def admin_delete_product(product_id):
        product = Product.query.get_or_404(product_id)
        name = product.name
        db.session.delete(product)
        db.session.commit()
        flash(f'Product "{name}" deleted successfully.', 'danger')
        return redirect(url_for('admin_products'))

    return app


# ── Run Application ─────────────────────────────────────────────
if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        # Seed data if empty
        if not Product.query.first():
            from seed_data import seed_database
            seed_database(db)
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(debug=debug, host='0.0.0.0', port=port)
