"""
Main entry point for Nixpacks auto-detection.
Simply imports the app from wsgi.py to satisfy gunicorn main:app requirement.
"""
from wsgi import app

if __name__ == '__main__':
    app.run()