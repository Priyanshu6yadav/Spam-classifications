# Spam Classification API

[![CI](https://github.com/your-username/spam-classification/actions/workflows/ci.yml/badge.svg)](https://github.com/your-username/spam-classification/actions/workflows/ci.yml)

A production-ready machine learning API to classify text messages as "Spam" or "Legitimate" (Ham). This project is built with Flask and Scikit-learn and is designed for easy deployment on platforms like Render.

## Features

- **Optimized ML Model**: Uses a `CalibratedClassifierCV` with an `ExtraTreesClassifier` and `TfidfVectorizer` pipeline for accurate and reliable predictions.
- **RESTful API**: A clean, simple API endpoint for making predictions.
- **Production-Ready Code**: Follows the application factory pattern, includes robust error handling, logging, and security features like rate limiting.
- **Automated Workflow**: Includes scripts for data preparation and model training.
- **CI/CD Ready**: Comes with a GitHub Actions workflow for continuous integration.
- **One-Click Deployment**: Configured for easy deployment to Render.

## Project Architecture

```
Browser/Client --> Flask Web App (Gunicorn) --> ML Pipeline (model_optimized.pkl)
```

- The **Flask Web App** provides a UI and a `/predict` API endpoint.
- **Gunicorn** serves the application in a production environment.
- The **ML Pipeline** is a single `model_optimized.pkl` file that handles both text vectorization and classification, ensuring consistency between training and prediction.

---

## Local Setup and Running

### Prerequisites

- Python 3.9+
- `pip` and `venv`

### 1. Clone and Set Up Virtual Environment

```bash
git clone https://github.com/your-username/spam-classification.git
cd spam-classification
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Prepare Data and Train Model

Run the following scripts from the project root directory.

```bash
# 1. Convert raw data to CSV
python scripts/prepare_data.py

# 2. Train the model (creates models/model_optimized.pkl)
python scripts/train.py
```

### 4. Run the Application

```bash
gunicorn --bind 0.0.0.0:8000 wsgi:app
```

Open your browser and navigate to `http://localhost:8000`.

## API Endpoint

**Endpoint**: `/predict`
**Method**: `POST`
**Body**: JSON with a `message` key.

**Example using cURL:**
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"message": "free entry to win cash prizes"}' \
     http://localhost:8000/predict
```