"""
Main entry point for Nixpacks auto-detection.
Simply imports the app from wsgi.py to satisfy gunicorn main:app requirement.
"""
import os
import sys

# Ensure the current directory is in the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wsgi import app

__all__ = ['app']

if __name__ == '__main__':
    app.run()