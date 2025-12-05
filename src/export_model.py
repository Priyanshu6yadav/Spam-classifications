"""
Model Export Script
Exports the trained vectorizer and model from the notebook to pickle files.
Run this after training your model in model.ipynb

Usage:
    python export_model.py
"""

import pickle
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def export_model(vectorizer, model, output_dir=None):
    """
    Export vectorizer and model to pickle files.
    
    Args:
        vectorizer: Trained TfidfVectorizer object
        model: Trained model object
        output_dir: Directory to save files (default: current directory)
    """
    if output_dir is None:
        output_dir = Path.cwd()
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Export vectorizer
        vectorizer_path = output_dir / 'vectorizer.pkl'
        with open(vectorizer_path, 'wb') as f:
            pickle.dump(vectorizer, f)
        logger.info(f"Vectorizer exported to {vectorizer_path}")
        
        # Export model
        model_path = output_dir / 'model.pkl'
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        logger.info(f"Model exported to {model_path}")
        
        return True
    except Exception as e:
        logger.error(f"Error exporting model: {e}")
        return False


def load_model(vectorizer_path='vectorizer.pkl', model_path='model.pkl'):
    """
    Load vectorizer and model from pickle files.
    
    Args:
        vectorizer_path: Path to vectorizer.pkl
        model_path: Path to model.pkl
    
    Returns:
        tuple: (vectorizer, model)
    """
    try:
        with open(vectorizer_path, 'rb') as f:
            vectorizer = pickle.load(f)
        logger.info(f"Vectorizer loaded from {vectorizer_path}")
        
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        logger.info(f"Model loaded from {model_path}")
        
        return vectorizer, model
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return None, None
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return None, None


if __name__ == "__main__":
    # Example usage:
    # After training in your notebook, uncomment and modify the following:
    
    # from model import vectorizer, model  # Import your trained objects
    # export_model(vectorizer, model)
    
    print("Model export script loaded successfully!")
    print("Import this script in your notebook to export trained models:")
    print("  from export_model import export_model")
    print("  export_model(vectorizer, model)")
