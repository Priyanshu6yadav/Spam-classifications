# 🛡️ AI Spam Classifier - Advanced Detection System

An intelligent, production-ready spam classification system powered by machine learning. Detect spam messages with 98.15% accuracy using an advanced ExtraTreesClassifier model with a beautiful, modern web interface.

**Live Demo & Easy Deployment Ready for Render, Heroku, and other cloud platforms.**

---

## ✨ Features

### 🤖 Advanced AI Model
- **98.15% Accuracy** on test data
- **100% Precision** - Zero false positives
- **89.31% Recall** - Catches almost all spam
- Trained on 5,572 SMS messages (UCI ML Repository)
- Uses TF-IDF vectorization with 3000 features
- ExtraTreesClassifier with 50 decision trees

### 🎨 Modern Web Interface
- **Tailwind CSS** - Beautiful, responsive design
- **Glass Morphism** - Water-transparent effect
- **Real-time Predictions** - AJAX-powered instant results
- **Animated UI** - Floating blobs, shimmer effects, pulse animations
- **Dark Theme** - Professional blue-cyan-purple gradient
- **Mobile Responsive** - Works on all devices
- **Accessibility Support** - Keyboard shortcuts, reduced motion support

### 🔧 Developer-Friendly Backend
- Clean Flask API with JSON responses
- Comprehensive error handling
- Professional logging
- Docker-ready configuration
- Render deployment ready
- Modular code structure
- Well-documented

---

## 🚀 Quick Start

### Local Development

```bash
# 1. Navigate to project
cd "spam classification"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
python app.py

# 4. Open in browser
# Visit: http://localhost:8000
```

### With Port 5000 (if port 8000 is taken)
```bash
PORT=5000 python app.py
```

---

## 🎯 Project Structure

```
spam-classifier/
├── README.md                      # Main documentation
├── requirements.txt               # Python dependencies
├── app.py                         # Flask application (backend)
├── Procfile                       # Render/Heroku deployment
├── render.yaml                    # Render platform config
├── runtime.txt                    # Python version (3.11.7)
│
├── static/                        # Frontend assets
│   ├── styles.css                # Advanced animations & glass effects
│   └── script.js                 # AJAX form handling & validation
│
├── templates/                     # HTML templates
│   └── index.html                # Beautiful Tailwind UI
│
├── models/                        # Pre-trained ML models
│   ├── model.pkl                 # ExtraTreesClassifier (6.2 MB)
│   └── vectorizer.pkl            # TF-IDF Vectorizer (105 KB)
│
├── data/                          # Dataset files
│   ├── spam.csv                  # Training data (5,572 SMS)
│   └── spam_raw.txt              # Raw dataset
│
├── docs/                          # Documentation
│   ├── DEPLOYMENT_GUIDE.md       # Deploy on Render (20 min)
│   ├── IMPROVEMENTS_SUMMARY.md   # List of improvements
│   ├── COMPLETION_CHECKLIST.md   # Completion status
│   └── FILE_INVENTORY.md         # File reference
│
└── notebooks/                     # Jupyter notebooks
    └── model.ipynb               # Training pipeline
```

---

## 🧠 Model Performance

| Metric | Score |
|--------|-------|
| **Accuracy** | 98.15% |
| **Precision** | 100% |
| **Recall** | 89.31% |
| **F1-Score** | 94.33% |
| **Training Accuracy** | 99.97% |

**Dataset:** 5,572 SMS messages
- Legitimate: 4,825 messages
- Spam: 747 messages
- Train/Test Split: 70/30

---

## 🎨 UI Features

### Modern Design
- **Gradient Background** - Animated blue-cyan-purple gradients
- **Glass Effects** - Frosted glass with backdrop blur
- **Animations** - Floating blobs, shimmer effects, smooth transitions
- **Loading State** - Animated spinner during prediction

### Interactive Elements
- **Character Counter** - Real-time message length tracking
- **Confidence Bars** - Visual representation of spam vs legitimate probability
- **Status Badge** - Color-coded results (red for spam, green for legitimate)
- **AI Analysis** - Contextual analysis text based on prediction confidence
- **Model Stats** - Display of model performance metrics

### Keyboard Shortcuts
- `Ctrl + Enter` - Submit form
- `Esc` - Clear results
- Tab navigation support

---

## 🔌 API Endpoints

### POST /predict
Send a message for classification.

**Request:**
```json
{
  "message": "Win free money now!"
}
```

**Response (Spam):**
```json
{
  "error": false,
  "status": "spam",
  "message": "This message is 🚨 SPAM",
  "confidence": 90.0,
  "spam_confidence": 90.0,
  "ham_confidence": 10.0
}
```

**Response (Legitimate):**
```json
{
  "error": false,
  "status": "legitimate",
  "message": "This message is 💬 LEGITIMATE",
  "confidence": 100.0,
  "spam_confidence": 0.0,
  "ham_confidence": 100.0
}
```

**Error Response:**
```json
{
  "error": true,
  "status": "error",
  "message": "Please enter a message to classify."
}
```

---

## 🛠️ Technology Stack

### Backend
- **Flask 3.0.0** - Web framework
- **scikit-learn 1.6.1** - Machine learning
- **NumPy 1.26.4** - Numerical computing
- **Werkzeug 3.0.1** - WSGI utilities
- **Gunicorn 21.2.0** - Production WSGI server
- **Python 3.11.7** - Runtime

### Frontend
- **Tailwind CSS** - Utility-first CSS framework
- **Vanilla JavaScript** - No dependencies, pure ES6+
- **Font Awesome 6.4** - Icons library

### DevOps & Deployment
- **Git** - Version control
- **Render** - Cloud deployment platform
- **Docker** - Container support (optional)
- **GitHub** - Repository hosting

---

## 🚀 Deployment

### Deploy on Render (Recommended)

See `docs/DEPLOYMENT_GUIDE.md` for step-by-step instructions.

**Quick Summary:**
1. Push code to GitHub
2. Connect repository to Render
3. Set environment variable: `PORT=8000`
4. Deploy with one click
5. Live in ~5 minutes

### Deploy on Heroku

```bash
heroku create your-app-name
git push heroku main
```

### Deploy with Docker

```bash
docker build -t spam-classifier .
docker run -p 8000:8000 spam-classifier
```

---

## 📝 API Usage Examples

### Using curl
```bash
# Spam message
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"message": "Congratulations! You won! Claim prize now!"}'

# Legitimate message
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"message": "Meeting at 3pm tomorrow?"}'
```

### Using Python
```python
import requests
import json

url = "http://localhost:8000/predict"
headers = {"Content-Type": "application/json"}

message = "Win free money now!"
data = json.dumps({"message": message})

response = requests.post(url, headers=headers, data=data)
result = response.json()

print(f"Status: {result['status']}")
print(f"Confidence: {result['confidence']}%")
print(f"Analysis: {result['message']}")
```

### Using JavaScript/Fetch
```javascript
const message = "Claim your free prize!";

fetch('http://localhost:8000/predict', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ message: message })
})
.then(res => res.json())
.then(data => {
    console.log(`Prediction: ${data.status}`);
    console.log(`Confidence: ${data.confidence}%`);
    console.log(`Analysis: ${data.message}`);
})
.catch(err => console.error(err));
```

---

## 🔐 Security Features

- ✅ Input validation (max 5000 characters)
- ✅ Error handling (no sensitive data exposed)
- ✅ CSRF protection ready
- ✅ Secure headers configured
- ✅ Production logging
- ✅ Rate limiting ready (for deployment)
- ✅ SQL injection proof (no database)

---

## 📊 Model Training

The model was trained using:

```python
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

# Vectorization
vectorizer = TfidfVectorizer(max_features=3000, stop_words='english')
X = vectorizer.fit_transform(messages)

# Training
model = ExtraTreesClassifier(n_estimators=50, random_state=42)
model.fit(X, y)
```

**Training Data:** UCI ML Repository - SMS Spam Collection

---

## 🎓 How It Works

1. **Message Input** - User types a message
2. **Vectorization** - Message converted to 3000-dimensional TF-IDF vector
3. **Prediction** - ExtraTreesClassifier predicts class
4. **Probability** - Model returns confidence scores
5. **Analysis** - Contextual analysis generated based on confidence
6. **Display** - Results shown with beautiful visualizations

---

## 🧪 Testing

### Manual Testing
```bash
# Start app
python app.py

# Test in another terminal
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"message": "Your test message here"}'
```

### Test Messages

**Spam Examples:**
- "Win free money now!"
- "Congratulations! You won!"
- "Claim your prize here"
- "Click here for free offer"

**Legitimate Examples:**
- "What time is the meeting?"
- "Hi, how are you?"
- "Let's meet tomorrow"
- "Thanks for the update"

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Use different port
PORT=8001 python app.py

# Or find and kill process
lsof -ti:8000 | xargs kill -9
```

### Models Not Found
```bash
# Ensure models are in models/ directory
ls models/
# Should show: model.pkl, vectorizer.pkl
```

### scikit-learn Version Warnings
- Safe to ignore
- Models are compatible
- Consider upgrading: `pip install --upgrade scikit-learn`

---

## 📚 Documentation

- `docs/DEPLOYMENT_GUIDE.md` - Detailed deployment instructions
- `docs/IMPROVEMENTS_SUMMARY.md` - Complete improvement list
- `docs/COMPLETION_CHECKLIST.md` - Project status
- `docs/FILE_INVENTORY.md` - File reference guide
- `PROJECT_STRUCTURE.md` - Project organization

---

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:

- [ ] Add more languages support
- [ ] Implement caching for frequent messages
- [ ] Add admin dashboard
- [ ] Real-time model retraining
- [ ] Export predictions to CSV
- [ ] Add email notifications
- [ ] Implement rate limiting

---

## 📄 License

This project is open source and available under the MIT License.

---

## 👤 Author

**Priyanshu Yadav**

- GitHub: [@Priyanshu6yadav](https://github.com/Priyanshu6yadav)
- Email: Priyanshu8yadav@gmail.com

---

## 🙏 Acknowledgments

- UCI Machine Learning Repository for SMS Spam Collection dataset
- scikit-learn for ML algorithms
- Flask for web framework
- Tailwind CSS for styling
- Font Awesome for icons

---

## 📞 Support

For issues, questions, or suggestions:
1. Open an issue on GitHub
2. Check existing documentation
3. Review troubleshooting section
4. Contact the author

---

## 🎯 Roadmap

**Current Version: 2.0** ✅
- Advanced Tailwind UI ✅
- Glass morphism effects ✅
- AJAX predictions ✅
- 98.15% accuracy ✅
- Full documentation ✅

**Future Versions:**
- Mobile app (React Native)
- Multi-language support
- Advanced analytics dashboard
- Real-time model monitoring
- API key authentication
- WebSocket support

---

**Made with ❤️ using Python, Flask, and Machine Learning**

Visit the live demo: *[Coming Soon - Deployed on Render]*

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
