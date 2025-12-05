"""
Spam Classification Flask Application

A production-ready web application for classifying messages as spam or ham.
This application is designed to be deployed on services like Render.
"""

# Import necessary libraries
import os
import pickle
import time
import logging
from flask import Flask, request, render_template, g
from typing import Dict, Any, Tuple
from functools import wraps

# --- Logging Configuration ---
# Configure logging to output informational messages and above
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
# Create a logger instance for this application
logger = logging.getLogger(__name__)

# --- Rate Limiting ---
# Simple in-memory rate limiting
RATE_LIMIT_REQUESTS = 15  # Max requests
RATE_LIMIT_PERIOD = 60  # Seconds
request_counts: Dict[str, list] = {}

# --- Model Initialization ---
# The pipeline will be loaded from disk when the application starts.
model = None

def load_pipeline():
    """
    Load the pre-trained pipeline from disk.
    This function is called once when the application starts.
    """
    global model
    
    # Get the absolute path to the directory of the current script.
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    
    # Define path to the model file.
    model_path = os.path.join(base_dir, 'models', 'model_optimized.pkl')
    
    try:
        logger.info("Loading model pipeline from: %s", model_path)
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        logger.info("--- Model pipeline loaded successfully ---")

    except FileNotFoundError:
        logger.critical(f"Model file not found at {model_path}. Please run the training script to create 'model_optimized.pkl'.", exc_info=True)
        exit(1) # Exit if the model is essential
    except Exception as e:
        logger.critical(f"An unexpected error occurred while loading the model: {e}", exc_info=True)
        exit(1)


def create_app():
    """
    Create and configure an instance of the Flask application.
    This follows the App Factory pattern.
    """
    app = Flask(__name__, static_folder='../static', template_folder='../templates')

    # --- Model Loading ---
    load_pipeline()

    # --- Flask Routes ---
    @app.route('/')
    def home() -> str:
        """
        Render the main page of the application (index.html).
        """
        return render_template('index.html')

    def rate_limit_decorator(f):
        """A decorator to handle rate limiting."""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = request.remote_addr
            current_time = time.time()

            if client_ip not in request_counts:
                request_counts[client_ip] = []

            # Remove timestamps older than the rate limit period
            request_counts[client_ip] = [
                ts for ts in request_counts[client_ip] if current_time - ts < RATE_LIMIT_PERIOD
            ]

            if len(request_counts[client_ip]) >= RATE_LIMIT_REQUESTS:
                logger.warning(f"Rate limit exceeded for IP: {client_ip}")
                return {
                    'error': True,
                    'message': 'Too many requests. Please wait a minute and try again.',
                    'status': 'error'
                }, 429  # HTTP 429: Too Many Requests

            request_counts[client_ip].append(current_time)
            return f(*args, **kwargs)
        return decorated_function


    @app.route('/predict', methods=['POST'])
    @rate_limit_decorator
    def predict() -> Tuple[Dict[str, Any], int]:
        """
        Handle the POST request for message classification.
        """
        try:
            # Get the message from JSON or form data
            data = request.get_json() if request.is_json else request.form
            message = data.get('message', '').strip()
            
            # --- Input Validation ---
            if not message:
                logger.warning("Prediction attempt with empty message.")
                return {
                    'error': True,
                    'message': 'Please enter a message to classify.',
                    'status': 'error'
                }, 400
            
            # Limit message length to prevent potential abuse
            if len(message) > 5000:
                logger.warning(f"Prediction attempt with overly long message ({len(message)} chars).")
                return {
                    'error': True,
                    'message': 'Message is too long. Please limit to 5000 characters.',
                    'status': 'error'
                }, 400
            
            logger.info(f"Classifying message of length {len(message)}")
            
            # --- Prediction ---
            if model is None:
                logger.error("Model not loaded!")
                raise Exception("Model is not loaded. Please restart the application.")

            # --- Prediction (Optimized to run pipeline once) ---
            confidence = model.predict_proba([message])[0]
            prediction = 1 if confidence[1] > confidence[0] else 0
            
            is_spam = (prediction == 1)
            ham_confidence = confidence[0] * 100
            spam_confidence = confidence[1] * 100
            
            logger.info(f"Prediction: {'Spam' if is_spam else 'Legitimate'}, Confidence: {confidence_score:.2f}%")
            
            return {
                'error': False,
                'status': 'spam' if is_spam else 'legitimate',
                'message': f'This message is {"🚨 SPAM" if is_spam else "💬 LEGITIMATE"}',
                'confidence': round(max(ham_confidence, spam_confidence), 1),
                'spam_confidence': round(spam_confidence, 1),
                'ham_confidence': round(ham_confidence, 1)
            }, 200
        
        except Exception as e:
            logger.error(f"An error occurred during prediction: {e}", exc_info=True)
            return {
                'error': True,
                'message': 'An unexpected server error occurred. The issue has been logged.',
                'status': 'error'
            }, 500

    # --- Error Handlers ---
    @app.errorhandler(404)
    def not_found(error: Exception) -> Tuple[str, int]:
        """Custom handler for 404 Not Found errors."""
        logger.warning(f"404 error encountered at {request.path}: {error}")
        return render_template('index.html', error_message='404 - Page Not Found'), 404

    @app.errorhandler(500)
    def internal_error(error: Exception) -> Tuple[str, int]:
        """Custom handler for 500 Internal Server errors."""
        logger.error(f"500 internal server error: {error}", exc_info=True)
        return render_template('index.html', error_message='500 - An internal server error occurred.'), 500

    return app

# --- Application Entry Point ---

if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get('PORT', 8000))
    
    try:
        logger.info("Application starting on port %d", port)
        logger.info("Open browser and visit: http://localhost:%d", port)

        # Use environment variable for debug mode, default to False
        is_debug = os.environ.get('FLASK_DEBUG', '0').lower() in ['true', '1', 't']
        if not is_debug:
            logger.warning("Starting in production mode. Use a WSGI server like Gunicorn for better performance.")

        app.run(
            host='0.0.0.0',
            port=port,
            debug=is_debug
        )
    except OSError as e:
        if "Address already in use" in str(e):
            new_port = port + 1
            logger.warning(f"Port {port} is already in use. Trying {new_port}...")
            app.run(host='0.0.0.0', port=new_port, debug=False)
        else:
            logger.critical(f"Failed to start the application: {e}", exc_info=True)
            exit(1)
    except Exception as e:
        logger.critical(f"Failed to start the application: {e}", exc_info=True)
        exit(1)
