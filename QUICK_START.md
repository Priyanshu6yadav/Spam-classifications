# 🚀 Quick Setup Guide

## 30-Second Start

```bash
cd "/Users/priyanshuyadav/Desktop/spam classification"
pip install -r requirements.txt
python app.py
```

Open browser: **http://localhost:8000**

---

## 📋 Complete Setup Steps

### Step 1: Navigate to Project
```bash
cd "/Users/priyanshuyadav/Desktop/spam classification"
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- Flask 3.0.0 (web framework)
- scikit-learn 1.6.1 (ML algorithms)
- NumPy 1.26.4 (numerical computing)
- Werkzeug 3.0.1 (WSGI server)
- Gunicorn 21.2.0 (production server)

### Step 3: Run the Application
```bash
python app.py
```

You should see:
```
2025-12-06 00:43:31,288 - __main__ - INFO - Models loaded successfully
2025-12-06 00:43:31,288 - __main__ - INFO - Application starting on port 8000
2025-12-06 00:43:31,288 - __main__ - INFO - Open browser and visit: http://localhost:8000
 * Running on http://127.0.0.1:8000
```

### Step 4: Open in Browser
Visit: **http://localhost:8000**

---

## 🧪 Test the Application

### In Browser
1. Type or paste a message in the textarea
2. Click "Classify Message"
3. View the results with confidence scores

### Using API (Terminal)

**Test Spam:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"message": "Congratulations! You won! Claim your prize now!"}'
```

**Test Legitimate:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"message": "Hi, when are we meeting?"}'
```

---

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Use port 8001 instead
PORT=8001 python app.py
```

### Dependencies Not Installing
```bash
# Force reinstall
pip install --force-reinstall -r requirements.txt
```

### Models Not Found
```bash
# Check models directory
ls -lh models/

# Should show:
# model.pkl (6.2 MB)
# vectorizer.pkl (105 KB)
```

### scikit-learn Warnings
- Safe to ignore
- Model still works perfectly
- Warnings are just version information

---

## 📊 Project Files

```
Static Files:
- templates/index.html      (11 KB)  - Web UI
- static/styles.css         (6.5 KB) - Animations
- static/script.js          (8.2 KB) - JavaScript

Model Files:
- models/model.pkl          (6.2 MB) - ML Model
- models/vectorizer.pkl     (105 KB) - Vectorizer

Data Files:
- data/spam.csv             (486 KB) - Training data
- data/spam_raw.txt         (477 KB) - Raw data

Configuration:
- app.py                    (7.2 KB) - Flask app
- requirements.txt          (5 lines) - Dependencies
- Procfile                  (1 line)  - Deployment
- render.yaml               (8 lines) - Render config
- runtime.txt               (1 line)  - Python version
```

---

## 🎯 Features Overview

### What Can You Do?

✅ Classify messages as spam or legitimate
✅ Get confidence scores for predictions
✅ See visual probability bars
✅ Read AI analysis of messages
✅ View model performance stats
✅ Use keyboard shortcuts
✅ Get instant results (<1 second)

### Keyboard Shortcuts

- `Ctrl + Enter` - Submit form
- `Esc` - Clear results
- `Tab` - Navigate elements

---

## 📱 Mobile Usage

The app is fully responsive:
- 📱 Mobile phones (320px and up)
- 📱 Tablets (768px and up)
- 💻 Desktops (1920px and up)

Just open http://localhost:8000 on your phone!

---

## 🔌 API Response Examples

### Spam Detection
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

### Legitimate Message
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

---

## 📊 Model Performance

- **Accuracy:** 98.15%
- **Precision:** 100% (no false positives!)
- **Recall:** 89.31%
- **F1-Score:** 94.33%

**Trained on:** 5,572 SMS messages
**Features:** 3,000 TF-IDF features
**Algorithm:** ExtraTreesClassifier (50 trees)

---

## 🚀 Next Steps

1. ✅ Test locally (you're here!)
2. 📝 Read documentation (docs/ folder)
3. 🌐 Deploy on Render (DEPLOYMENT_GUIDE.md)
4. 🔄 Share with team
5. 📊 Monitor performance

---

## 📚 More Information

For detailed information, see:
- `README.md` - Main documentation
- `FINAL_SUMMARY.md` - Project summary
- `docs/DEPLOYMENT_GUIDE.md` - Cloud deployment
- `docs/IMPROVEMENTS_SUMMARY.md` - All improvements
- `PROJECT_STRUCTURE.md` - File organization

---

## 💡 Quick Tips

1. **Message Length:** Max 5000 characters
2. **Response Time:** Usually < 1 second
3. **Best Results:** Clear, natural language
4. **API Rate:** No limits (for now)
5. **Browser Cache:** CTRL+SHIFT+R to refresh

---

## ⚡ Advanced Usage

### Change Port
```bash
PORT=5000 python app.py    # Use port 5000
PORT=3000 python app.py    # Use port 3000
```

### Using with Python Requests
```python
import requests
response = requests.post(
    'http://localhost:8000/predict',
    json={'message': 'Your message here'}
)
print(response.json())
```

### Integration with JavaScript
```javascript
fetch('http://localhost:8000/predict', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({message: 'Test'})
}).then(r => r.json()).then(console.log)
```

---

## 🆘 Need Help?

1. Check this guide first
2. See TROUBLESHOOTING section above
3. Check browser console (F12) for errors
4. See app terminal output for logs
5. Contact: Priyanshu8yadav@gmail.com

---

## ✅ Checklist

- [ ] Navigated to project folder
- [ ] Installed dependencies
- [ ] Started Flask app
- [ ] Opened browser at http://localhost:8000
- [ ] Tested with sample message
- [ ] Got prediction result
- [ ] Saw confidence score
- [ ] Read documentation

**If all checked, you're good to go! 🎉**

---

**Happy Spam Detecting! 🛡️**
