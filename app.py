"""
Spam Classification Flask Application

A production-ready web application for classifying messages as spam or ham.
This application is designed to be deployed on services like Render.
"""

# Import necessary libraries
import os
import pickle
import logging
from flask import Flask, request, render_template

# --- Logging Configuration ---
# Configure logging to output informational messages and above
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
# Create a logger instance for this application
logger = logging.getLogger(__name__)

# --- Flask App Initialization ---
app = Flask(__name__)

# --- Model Loading ---
# Global variables to hold the loaded model and vectorizer
vectorizer = None
model = None


def load_model():
    """
    Load the pre-trained TF-IDF vectorizer and the ExtraTreesClassifier model
    from their respective pickle files.

    This function is designed to be robust, checking for models in the root
    directory or a 'models' subdirectory.

    Returns:
        tuple: (vectorizer, model) if successful.
    Raises:
        FileNotFoundError: If the model or vectorizer files are not found.
        Exception: For any other errors during loading.
    """
    global vectorizer, model
    
    try:
        # Define paths for the pickle files
        vectorizer_path = 'vectorizer.pkl'
        model_path = 'model.pkl'
        
        # Fallback to a 'models' directory if not found in the root
        if not os.path.exists(vectorizer_path):
            vectorizer_path = os.path.join('models', 'vectorizer.pkl')
        if not os.path.exists(model_path):
            model_path = os.path.join('models', 'model.pkl')
        
        # Load the vectorizer
        logger.info(f"Loading vectorizer from {vectorizer_path}")
        with open(vectorizer_path, 'rb') as f:
            vectorizer = pickle.load(f)
        
        # Load the model
        logger.info(f"Loading model from {model_path}")
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        
        logger.info("Models loaded successfully")
        return vectorizer, model
        
    except FileNotFoundError as e:
        logger.error(f"Model files not found: {e}")
        logger.warning("Ensure 'vectorizer.pkl' and 'model.pkl' are in the root directory or a 'models' subdirectory.")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred while loading the models: {e}")
        raise


@app.before_request
def initialize_models():
    """
    Initialize the machine learning models before the first request.
    This ensures that the models are loaded only once when the application starts.
    """
    global vectorizer, model
    if vectorizer is None or model is None:
        try:
            load_model()
        except Exception as e:
            logger.critical(f"Failed to initialize models on startup: {e}")
            # In a production environment, you might want to handle this more gracefully
            # or prevent the app from starting if models are essential.


# --- Flask Routes ---

@app.route('/')
def home():
    """
    Render the main page of the application (index.html).
    """
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """
    Handle the POST request for message classification.
    - Retrieves the message from the form.
    - Validates the input.
    - Uses the loaded model to predict if the message is spam or ham.
    - Returns the result to the user on the web page.
    """
    try:
        # Get the message from the form data and remove leading/trailing whitespace
        message = request.form.get('message', '').strip()
        
        # --- Input Validation ---
        if not message:
            logger.warning("Prediction attempt with empty message.")
            return render_template(
                'index.html',
                prediction_text='Please enter a message to classify.',
                input_text='',
                error=True
            )
        
        # Limit message length to prevent potential abuse
        if len(message) > 5000:
            logger.warning(f"Prediction attempt with overly long message ({len(message)} chars).")
            return render_template(
                'index.html',
                prediction_text='Message is too long. Please limit to 5000 characters.',
                input_text=message,
                error=True
            )
        
        logger.info(f"Classifying message of length {len(message)}")
        
        # --- Prediction ---
        # Transform the message into a numerical vector
        vect = vectorizer.transform([message]).toarray()
        
        # Predict the class (0 for ham, 1 for spam)
        prediction = model.predict(vect)[0]
        # Get the prediction probabilities for each class
        confidence = model.predict_proba(vect)[0]
        
        # --- Result Formatting ---
        is_spam = (prediction == 1)
        output = "Spam 🚨" if is_spam else "Legitimate 💬"
        confidence_score = max(confidence) * 100
        
        logger.info(f"Prediction: {output}, Confidence: {confidence_score:.2f}%")
        
        # Render the page with the classification result
        return render_template(
            'index.html',
            prediction_text=f'Classification: {output}',
            confidence_text=f'Confidence: {confidence_score:.1f}%',
            input_text=message,
            error=False
        )
    
    except Exception as e:
        # Log the full error for debugging and return a generic error to the user
        logger.error(f"An error occurred during prediction: {e}", exc_info=True)
        return render_template(
            'index.html',
            prediction_text=f'An unexpected error occurred. Please try again.',
            input_text=message,
            error=True
        )


# --- Error Handlers ---

@app.errorhandler(404)
def not_found(error):
    """Custom handler for 404 Not Found errors."""
    logger.warning(f"404 error encountered at {request.path}: {error}")
    return render_template('index.html', prediction_text='Page not found. Please check the URL.'), 404


@app.errorhandler(500)
def internal_error(error):
    """Custom handler for 500 Internal Server errors."""
    logger.error(f"500 internal server error: {error}", exc_info=True)
    return render_template('index.html', prediction_text='An internal server error occurred. The issue has been logged.'), 500


# --- Application Entry Point ---

if __name__ == "__main__":
    # Get the port from environment variables, defaulting to 5000 for local development
    port = int(os.environ.get('PORT', 5000))
    
    try:
        # Load the models before starting the server
        load_model()
        logger.info("Application starting on port %d", port)
        
        # Run the Flask app
        # host='0.0.0.0' is required for deployment on services like Render
        # debug=False is critical for production security
        app.run(
            host='0.0.0.0',
            port=port,
            debug=False
        )
    except Exception as e:
        logger.critical(f"Failed to start the application: {e}", exc_info=True)
        # Exit with an error code if the app fails to start
        exit(1)
