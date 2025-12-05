# Spam Classification Application

A production-ready Flask web application for classifying messages as spam or legitimate using machine learning.

## Features

✨ **Smart Classification** - AI-powered spam detection  
🚀 **Fast & Responsive** - Instant message analysis  
🎨 **Modern UI** - Beautiful and intuitive interface  
🔒 **Secure** - Private message processing  
📊 **Confidence Scores** - See model confidence in predictions  

## Prerequisites

- Python 3.11+
- pip (Python package installer)
- Pre-trained model files: `model.pkl` and `vectorizer.pkl`

## Local Setup

### 1. Clone the repository
```bash
git clone <repository-url>
cd "spam classification"
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Prepare model files
Ensure `model.pkl` and `vectorizer.pkl` are in the project root directory.

### 5. Run the application
```bash
python app.py
```

The app will be available at `http://localhost:5000`

## Project Structure

```
spam-classification/
├── app.py                 # Flask application
├── model.ipynb           # Jupyter notebook with model training
├── requirements.txt      # Python dependencies
├── Procfile              # Heroku/Render deployment config
├── render.yaml           # Render deployment config
├── runtime.txt           # Python version specification
├── templates/
│   └── index.html        # Web interface
├── model.pkl             # Trained model (not in repo)
└── vectorizer.pkl        # Vectorizer (not in repo)
```

## Model Information

The application uses:
- **Vectorizer**: TfidfVectorizer from scikit-learn
- **Model**: Naive Bayes classifier
- **Dataset**: Trained on SMS spam dataset
- **Classes**: 0 = Legitimate, 1 = Spam

## Deployment on Render

### Prerequisites
- GitHub repository with the code
- Model files (`model.pkl` and `vectorizer.pkl`)

### Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Create Render account**
   - Go to https://render.com
   - Sign up with GitHub

3. **Create new Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select "Python" as runtime
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`

4. **Configure Environment**
   - Set Python version to 3.11 (optional, if needed)

5. **Deploy**
   - Click "Create Web Service"
   - Monitor the deployment in the dashboard

### Important Notes for Render

- **Model Files**: Upload `model.pkl` and `vectorizer.pkl` to your GitHub repository
- **PORT Environment Variable**: The app automatically uses the PORT environment variable
- **No Debug Mode**: Production uses `debug=False`
- **Host Configuration**: App binds to `0.0.0.0` for Render compatibility

## API Endpoints

### GET `/`
Returns the main web interface.

### POST `/predict`
Predicts if a message is spam.

**Parameters:**
- `message` (form data): The message to classify

**Response:**
- Renders `index.html` with prediction result
- Shows confidence score and classification

## Error Handling

The application includes:
- ✓ Input validation (empty messages, length limits)
- ✓ Logging for debugging
- ✓ Error handlers (404, 500)
- ✓ Graceful error messages to users
- ✓ Model loading error handling

## Code Quality

Features implemented:
- Type hints in docstrings
- Comprehensive logging
- Clear documentation
- Production-ready configuration
- Error handling
- Input validation
- Performance optimized

## Troubleshooting

### Model files not found
**Solution**: Ensure `model.pkl` and `vectorizer.pkl` are in the project root or `models/` directory.

### Port already in use
**Solution**: Change the port in `app.py` or set the PORT environment variable:
```bash
PORT=5001 python app.py
```

### Import errors
**Solution**: Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Deployment fails
**Solution**: Check Render dashboard logs for detailed error messages.

## Performance Tips

1. **Model Loading**: Models are loaded on first request for efficiency
2. **Input Validation**: Prevents processing of invalid inputs
3. **Logging**: Enable/disable based on environment
4. **Caching**: Consider caching predictions for repeated inputs

## Security Considerations

- No sensitive data is stored
- Messages are processed in-memory only
- No database connections
- Secure headers in production
- Input size limitations (5000 characters)

## Development

To add features:

1. Modify `app.py` for backend logic
2. Update `templates/index.html` for UI changes
3. Test locally: `python app.py`
4. Push to GitHub and redeploy

## License

This project is open source and available for educational purposes.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review application logs
3. Verify model files are present
4. Check Python version compatibility
