"""
Production Model Training Script

This script trains the final, optimized spam classification model,
calibrates it, evaluates its performance, and saves the final pipeline
and associated metadata for production use.
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.pipeline import Pipeline
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.metrics import precision_score, recall_score, f1_score
import pickle
import os
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# ============================================================================
# 1. LOAD AND PREPARE DATA
# ============================================================================
logging.info("="*80)
logging.info("STARTING MODEL TRAINING PIPELINE (v2)")
logging.info("="*80)

logging.info("[1/4] Loading and preparing data...")
df = pd.read_csv(os.path.join(PROJECT_ROOT, 'data', 'spam.csv'))
df.columns = ['target', 'message'] # Rename columns for clarity
df['target'] = df['target'].map({'ham': 0, 'spam': 1})

print(f"  Total samples: {len(df):,}")
print(f"  Spam: {(df['target']==1).sum()} | Legitimate: {(df['target']==0).sum()}")

# Remove exact duplicates to reduce data leakage
df_unique = df.drop_duplicates(subset=['message'])
print(f"  After removing duplicates: {len(df_unique):,} unique messages")

# Split with stratification
X_train, X_test, y_train, y_test = train_test_split(
    df_unique['message'], df_unique['target'], 
    test_size=0.3, random_state=42, stratify=df_unique['target']
)

print(f"  Training set: {len(X_train):,}")
print(f"  Test set: {len(X_test):,}")

# ============================================================================
# 2. BUILD OPTIMIZED PIPELINE
# ============================================================================

logging.info("[2/4] Building optimized pipeline...")

# Optimization insights from evaluation:
# - 100-200 trees perform better (marginal improvement)
# - TF-IDF with 3000 features is good
# - Calibration improves reliability

pipe = Pipeline([
    ('tfidf', TfidfVectorizer(
        max_features=3000, 
        stop_words='english',
        max_df=0.95,  # Remove very common words
        min_df=2,      # Remove very rare words
        ngram_range=(1, 2),  # Include bigrams
        sublinear_tf=True    # Scale TF logarithmically
    )),
    ('clf', ExtraTreesClassifier(
        n_estimators=100,     # Increased from 50 for stability
        max_depth=None,
        random_state=42,
        n_jobs=-1,
        class_weight='balanced'  # Handle slight imbalance
    ))
])

logging.info("Pipeline configuration:")
logging.info("  - TfidfVectorizer: max_features=3000, ngram_range=(1,2)")
logging.info("  - ExtraTreesClassifier: 100 trees, balanced class weights")

# ============================================================================
# 3. TRAIN WITH CALIBRATION
# ============================================================================
logging.info("[3/4] Training and calibrating model...")

# Fit base pipeline
pipe.fit(X_train, y_train)

# Calibrate for better probability estimates
calib_pipe = CalibratedClassifierCV(pipe, cv=5)
calib_pipe.fit(X_train, y_train)

# Test on holdout set
y_pred = calib_pipe.predict(X_test)
y_pred_proba = calib_pipe.predict_proba(X_test)

# Performance metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)
tn, fp, fn, tp = cm.ravel()

logging.info("Performance on test set:")
logging.info(f"  - Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
logging.info(f"  - Precision: {precision:.4f}")
logging.info(f"  - Recall: {recall:.4f}")
logging.info(f"  - F1-Score: {f1:.4f}")

logging.info("Confusion matrix:")
logging.info(f"    [[{tn:4d} {fp:4d}]")
logging.info(f"     [{fn:4d} {tp:4d}]]")

# ============================================================================
# 4. SAVE MODELS & METADATA
# ============================================================================

logging.info("[4/4] Saving production model and metadata...")

models_dir = os.path.join(PROJECT_ROOT, 'models')
os.makedirs(models_dir, exist_ok=True)

# Save calibrated pipeline
model_path = os.path.join(models_dir, 'model_optimized.pkl')
with open(model_path, 'wb') as f:
    pickle.dump(calib_pipe, f)
logging.info(f"  ✓ Saved production pipeline to: {model_path}")

# Save metadata
metadata = {
    'version': '2.0',
    'metrics': {
        'accuracy': float(accuracy),
        'precision': float(precision),
        'recall': float(recall),
        'f1_score': float(f1),
    },
    'confusion_matrix': cm.tolist(),
    'model_params': {
        'features': 3000,
        'trees': 100,
        'ngrams': '(1,2)',
        'calibrated': True,
    },
    'data_summary': {
        'training_samples': len(X_train),
        'test_samples': len(X_test),
        'total_unique_messages': len(df_unique),
    }
}

metadata_path = os.path.join(models_dir, 'metadata_v2.json')
with open(metadata_path, 'w') as f:
    json.dump(metadata, f, indent=2)
logging.info(f"  ✓ Saved model metadata to: {metadata_path}")

logging.info("="*80)
logging.info("✅ MODEL TRAINING COMPLETE. ARTIFACTS SAVED.")
logging.info("="*80)
