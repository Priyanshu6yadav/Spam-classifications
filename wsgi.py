"""
WSGI entry point for the Spam Classification application.

This file is used by Gunicorn to serve the Flask application.
"""

from src.app import create_app

# Create the Flask app instance
app = create_app()
