"""
seed_railway.py — Standalone script to seed the Railway MySQL database.
Run locally: python seed_railway.py
It connects directly to Railway MySQL, creates tables, and inserts all seed data.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from app import create_app
from models import db, Product, Category, User

print("[SEED] Connecting to database...")
app = create_app()

with app.app_context():
    print("[SEED] Creating all tables...")
    db.create_all()
    print("[SEED] Tables created.")

    existing = Product.query.first()
    if existing:
        ans = input("[SEED] Database already has products. Re-seed? (y/n): ").strip().lower()
        if ans != 'y':
            print("[SEED] Aborted.")
            sys.exit(0)
        # Clear existing data in correct order (foreign keys)
        from models import OrderItem, CartItem, Order, ContactMessage
        OrderItem.query.delete()
        CartItem.query.delete()
        Order.query.delete()
        ContactMessage.query.delete()
        Product.query.delete()
        Category.query.delete()
        User.query.delete()
        db.session.commit()
        print("[SEED] Existing data cleared.")

    from seed_data import seed_database
    seed_database(db)
    print(f"[SEED] Done! Products: {Product.query.count()}, Categories: {Category.query.count()}, Users: {User.query.count()}")
