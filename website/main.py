"""
Main entry point for Nixpacks/Railway deployment.
Creates the Flask app directly to satisfy gunicorn main:app requirement.
"""
import os
import sys

# Ensure the current directory is in the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Import and create the Flask app
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
            print("[MAIN] Database seeded successfully.")
        else:
            print("[MAIN] Database already populated.")
    except Exception as e:
        print(f"[MAIN] DB init warning: {e}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)