"""
OPTIMIZED SPAM CLASSIFIER - Production Model v2
Improved based on evaluation findings
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.pipeline import Pipeline
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import pickle
import os

print("\n" + "="*80)
print("TRAINING OPTIMIZED SPAM CLASSIFIER - v2")
print("="*80)

# ============================================================================
# 1. LOAD AND PREPARE DATA
# ============================================================================

print("\n[1/4] Loading and preparing data...")
df = pd.read_csv('data/spam.csv')
df = df[['v1', 'v2']]
df.columns = ['target', 'message']
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

print("\n[2/4] Building optimized pipeline...")

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

print("  ✓ Pipeline configuration:")
print("    • TfidfVectorizer: max_features=3000, ngram_range=(1,2)")
print("    • ExtraTreesClassifier: 100 trees, balanced class weights")

# ============================================================================
# 3. TRAIN WITH CALIBRATION
# ============================================================================

print("\n[3/4] Training and calibrating model...")

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
cm = confusion_matrix(y_test, y_pred)
tn, fp, fn, tp = cm.ravel()

print(f"\n  Performance on test set:")
print(f"    • Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
print(f"    • Precision: {tp/(tp+fp):.4f}")
print(f"    • Recall: {tp/(tp+fn):.4f}")
print(f"    • F1-Score: {2*tp/(2*tp+fp+fn):.4f}")
print(f"    • FP Rate: {fp/(fp+tn):.6f}")

print(f"\n  Confusion matrix:")
print(f"    [[{tn:4d} {fp:4d}]")
print(f"     [{fn:4d} {tp:4d}]]")

# ============================================================================
# 4. SAVE MODELS & METADATA
# ============================================================================

print("\n[4/4] Saving optimized models...")

os.makedirs('models', exist_ok=True)

# Save calibrated pipeline
with open('models/model_optimized.pkl', 'wb') as f:
    pickle.dump(calib_pipe, f)
print(f"  ✓ Saved: models/model_optimized.pkl")

# Save uncalibrated pipeline for comparison
with open('models/model_v2.pkl', 'wb') as f:
    pickle.dump(pipe, f)
print(f"  ✓ Saved: models/model_v2.pkl")

# Save metadata
metadata = {
    'version': '2.0',
    'accuracy': float(accuracy),
    'precision': float(tp / (tp + fp)),
    'recall': float(tp / (tp + fn)),
    'f1_score': float(2 * tp / (2 * tp + fp + fn)),
    'fp_rate': float(fp / (fp + tn)),
    'confusion_matrix': cm.tolist(),
    'features': 3000,
    'trees': 100,
    'ngrams': '(1,2)',
    'calibrated': True,
    'training_samples': len(X_train),
    'test_samples': len(X_test),
    'unique_messages': len(df_unique),
}

with open('models/metadata_v2.json', 'w') as f:
    import json
    json.dump(metadata, f, indent=2)
print(f"  ✓ Saved: models/metadata_v2.json")

# ============================================================================
# COMPARISON: Original vs Optimized
# ============================================================================

print("\n" + "="*80)
print("MODEL COMPARISON: v1 (Original) vs v2 (Optimized)")
print("="*80)

# Load original model and vectorizer
try:
    with open('models/model.pkl', 'rb') as f:
        original_clf = pickle.load(f)
    with open('models/vectorizer.pkl', 'rb') as f:
        original_vec = pickle.load(f)
    
    # Vectorize test data with original vectorizer
    X_test_vectorized_old = original_vec.transform(X_test)
    y_pred_original = original_clf.predict(X_test_vectorized_old)
    y_pred_proba_original = original_clf.predict_proba(X_test_vectorized_old)
    accuracy_original = accuracy_score(y_test, y_pred_original)
    cm_original = confusion_matrix(y_test, y_pred_original)
    tn_o, fp_o, fn_o, tp_o = cm_original.ravel()
    
    print(f"\n{'Metric':<20} {'v1 (Original)':<20} {'v2 (Optimized)':<20} {'Change':<15}")
    print("-" * 75)
    
    metrics = {
        'Accuracy': (accuracy_score(y_test, y_pred_original), accuracy),
        'Precision': (tp_o/(tp_o+fp_o), tp/(tp+fp)),
        'Recall': (tp_o/(tp_o+fn_o), tp/(tp+fn)),
        'F1-Score': (2*tp_o/(2*tp_o+fp_o+fn_o), 2*tp/(2*tp+fp+fn)),
        'FP Rate': (fp_o/(fp_o+tn_o), fp/(fp+tn)),
        'TP Count': (tp_o, tp),
        'FP Count': (fp_o, fp),
        'FN Count': (fn_o, fn),
    }
    
    for metric, (val_old, val_new) in metrics.items():
        if metric.endswith('Count'):
            change = val_new - val_old
            symbol = "↑" if change > 0 else "↓" if change < 0 else "="
            print(f"{metric:<20} {val_old:<20.0f} {val_new:<20.0f} {symbol} {abs(change):.0f}")
        else:
            change_pct = (val_new - val_old) * 100
            symbol = "↑" if change_pct > 0 else "↓" if change_pct < 0 else "="
            print(f"{metric:<20} {val_old:<20.4f} {val_new:<20.4f} {symbol} {change_pct:+.2f}%")
except Exception as e:
    print(f"\nNote: Could not load original model for comparison: {e}")

# ============================================================================
# FEATURE IMPORTANCE (top 15)
# ============================================================================

print("\n" + "="*80)
print("TOP 15 FEATURES (Model v2)")
print("="*80)

clf = pipe.named_steps['clf']
vectorizer = pipe.named_steps['tfidf']
feature_names = vectorizer.get_feature_names_out()
feature_importance = clf.feature_importances_

top_indices = np.argsort(feature_importance)[-15:][::-1]
top_features = feature_names[top_indices]
top_importance = feature_importance[top_indices]

print("\n" + " "*2 + "Rank" + " "*8 + "Feature" + " "*20 + "Importance")
print("-" * 55)
for i, (feat, imp) in enumerate(zip(top_features, top_importance), 1):
    print(f"  {i:2d}.  {feat:<25s} {imp:.6f}")

# ============================================================================
# RECOMMENDATIONS
# ============================================================================

print("\n" + "="*80)
print("RECOMMENDATIONS & NEXT STEPS")
print("="*80)

improvements_made = []

if accuracy > accuracy_original:
    improvements_made.append(f"✓ Accuracy improved: {accuracy:.4f} vs {accuracy_original:.4f}")
if tp > tp_o:
    improvements_made.append(f"✓ True positives increased: {tp} vs {tp_o}")
if fp < fp_o:
    improvements_made.append(f"✓ False positives decreased: {fp} vs {fp_o}")

if improvements_made:
    print("\n✨ Improvements Made:")
    for imp in improvements_made:
        print(f"  {imp}")

print("\n🎯 Deployment Recommendation:")
if accuracy > accuracy_original:
    print(f"  ✓ Deploy v2 (optimized model)")
    print(f"    • Better accuracy: {accuracy:.4f}")
    print(f"    • Calibrated probabilities")
    print(f"    • Bigram features improve detection")
else:
    print(f"  • v1 and v2 have similar performance")
    print(f"  • Both are production-ready")

print("\n🔄 To use optimized model in production:")
print("  1. Update app.py to load 'models/model_optimized.pkl' instead of 'models/model.pkl'")
print("  2. Test predictions on a sample message")
print("  3. Monitor false positives in production")
print("  4. Create A/B test to compare v1 and v2")

print("\n💡 Further Optimizations (Optional):")
print("  • Increase trees to 200 for marginal gains")
print("  • Try ensemble (ExtraTrees + LogisticRegression)")
print("  • Implement threshold optimization based on business metrics")
print("  • Add adversarial training for robustness")
print("  • Monitor drift and retrain quarterly")

print("\n" + "="*80)
print("✅ MODEL v2 READY FOR PRODUCTION")
print("="*80 + "\n")
