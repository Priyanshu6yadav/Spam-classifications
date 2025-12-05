# 🚀 Deployment Guide for Render

## Overview
Your Spam Classifier is now ready for deployment! This guide walks you through deploying to Render, a modern cloud platform.

## Pre-Deployment Checklist

✅ Model trained: `model.pkl` (ExtraTreesClassifier)  
✅ Vectorizer saved: `vectorizer.pkl` (TF-IDF, 3000 features)  
✅ Flask app configured: `app.py` (production-ready)  
✅ Beautiful UI: `templates/index.html` (responsive design)  
✅ Dependencies specified: `requirements.txt`  
✅ Deployment config: `Procfile` & `render.yaml`

## Model Performance

- **Accuracy**: 98.65%
- **Precision**: 100.00%
- **Dataset**: 5,572 SMS messages (UCI ML Repository)
- **Classes**: Ham (4,516) | Spam (653)
- **Algorithm**: ExtraTreesClassifier with TF-IDF vectorization

## Step 1: Prepare GitHub Repository

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Spam Classifier ready for deployment"

# Add remote repository (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/spam-classifier.git

# Push to main branch
git branch -M main
git push -u origin main
```

## Step 2: Sign Up for Render

1. Go to https://render.com
2. Click "Sign Up"
3. Choose "Sign up with GitHub"
4. Authorize Render to access your GitHub account

## Step 3: Create Web Service on Render

1. Click "New +" in the top right
2. Select "Web Service"
3. Connect your GitHub repository:
   - Search for your `spam-classifier` repository
   - Click "Connect"
4. Configure the service:
   - **Name**: `spam-classifier` (or choose a custom name)
   - **Runtime**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free (or paid for better performance)

5. Click "Create Web Service"

## Step 4: Monitor Deployment

- Render will automatically:
  1. Pull your code from GitHub
  2. Install dependencies
  3. Start the Flask app with Gunicorn
  4. Assign a public URL (e.g., `https://spam-classifier.onrender.com`)

- Check logs in the Render dashboard for any issues
- Wait for "Build successful" message

## Step 5: Test Your Deployed App

Once deployed, visit your app URL and test predictions:

```
https://YOUR_APP_NAME.onrender.com
```

### Test Messages

**Legitimate Messages:**
- "Hi, how are you?"
- "Can we meet tomorrow?"
- "Here's the file you requested"

**Spam Messages:**
- "CLICK HERE FOR FREE MONEY!!!"
- "You won a free iPhone! Claim now!"
- "Congratulations! You're a winner!"

## Environment Variables (Optional)

If you need to set environment variables in Render:

1. Go to your Web Service settings
2. Click "Environment"
3. Add variables (e.g., for future logging or API keys)

## Auto-Deployment from GitHub

By default, Render will automatically redeploy whenever you push to GitHub:

```bash
# Make code changes
git add .
git commit -m "Update feature"
git push origin main
```

Render will automatically rebuild and deploy your changes.

## Troubleshooting

### App takes too long to start
- **Reason**: Model loading on cold start
- **Solution**: This is normal. Model loads on first request
- **Workaround**: Use Paid tier for faster CPU (optional)

### "Model not found" error
- **Reason**: `model.pkl` or `vectorizer.pkl` missing
- **Solution**: Ensure both files are committed to GitHub and in root directory

### Port binding error
- **Reason**: App trying to use wrong port
- **Solution**: Already fixed in code - app uses `PORT` environment variable

### Build failures
- **Reason**: Dependency conflicts
- **Solution**: Check logs and update `requirements.txt` with compatible versions

### Timeout errors
- **Reason**: Request took too long (>30 seconds on free tier)
- **Solution**: Upgrade to Paid tier for longer timeout limits

## Performance Tips

1. **First Request Warmup**: First request takes ~3-5 seconds (model loading)
2. **Subsequent Requests**: ~200-500ms (normal)
3. **Caching**: Consider caching vectorizer for frequent identical inputs
4. **Optimization**: For production load, consider:
   - Upgrading to paid plan
   - Using model caching
   - Pre-loading models at startup

## Scaling Your App

### Free Plan Limits:
- 1 free instance (auto-sleeps after 15 mins of inactivity)
- Perfect for demos and learning

### Paid Plans:
- Always-running instances
- Better CPU/RAM
- No auto-sleep
- $7/month - $100+/month depending on needs

## Monitoring & Logs

### Access Logs in Render:
1. Go to your Web Service dashboard
2. Click "Logs" tab
3. See real-time application logs

### Common Log Messages:
- `Loading vectorizer from vectorizer.pkl` - App initializing
- `Loading model from model.pkl` - Model being loaded
- `Processing message of length X` - Prediction request
- `Error during prediction` - Check details

## Update Your Model

To update the model with new training data:

1. Retrain locally:
   ```bash
   python3 < training_script.py
   ```

2. Commit new model files:
   ```bash
   git add model.pkl vectorizer.pkl
   git commit -m "Update model with new training data"
   git push
   ```

3. Render automatically redeploys with new models

## API Usage

### Programmatic Access

```bash
curl -X POST https://YOUR_APP_NAME.onrender.com/predict \
  -d "message=Your%20message%20here"
```

### Python Integration

```python
import requests

url = "https://YOUR_APP_NAME.onrender.com/predict"
data = {"message": "Your test message"}
response = requests.post(url, data=data)
print(response.text)
```

## Custom Domain (Optional)

To use your own domain:

1. Go to service settings
2. Click "Custom Domain"
3. Add your domain
4. Follow DNS configuration instructions

## Backup & Version Control

Always keep your code on GitHub:
- `git push` after any changes
- Enable GitHub branch protection
- Render tracks deployment history

## Cost Estimation

| Plan | Cost | Features |
|------|------|----------|
| Free | $0 | Demo, Learning, Testing |
| Starter | $7/month | Always on, auto-scaling |
| Standard | $25/month | Better performance |
| Pro | $100+/month | High traffic, advanced features |

## Support & Resources

- **Render Documentation**: https://render.com/docs
- **Flask Documentation**: https://flask.palletsprojects.com
- **GitHub**: Push code updates for auto-deployment
- **Issues**: Check Render logs for debugging

## Next Steps

1. ✅ Deploy to Render
2. 📝 Share your app URL with others
3. 📊 Monitor usage in Render dashboard
4. 🔄 Continuously improve your model
5. 🚀 Scale as needed

---

**Your app is ready to go live!** 🎉

Once deployed, share your URL:
```
https://YOUR_APP_NAME.onrender.com
```

Enjoy your production spam classifier!
