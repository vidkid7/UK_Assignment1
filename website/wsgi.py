"""
WSGI entry point for production deployment (Railway / Gunicorn).
Gunicorn runs: gunicorn wsgi:app
"""
import os
import sys

# Ensure the website directory is on the path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from app import create_app
from models import db, Product

app = create_app()

# Auto-create tables and seed if empty on first boot
with app.app_context():
    try:
        db.create_all()
        if not Product.query.first():
            from seed_data import seed_database
            seed_database(db)
            print("[WSGI] Database seeded successfully.")
        else:
            print("[WSGI] Database already populated.")
    except Exception as e:
        print(f"[WSGI] DB init warning: {e}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
