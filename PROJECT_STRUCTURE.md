# Spam Classifier - Project Structure

```
spam-classifier/
├── README.md                 # Main project documentation
├── requirements.txt          # Python dependencies
├── Procfile                  # Deployment configuration
├── render.yaml               # Render platform config
├── runtime.txt               # Python version
├── app.py                    # Flask application (main entry point)
├── .gitignore                # Git ignore rules
│
├── docs/                     # Documentation
│   ├── DEPLOYMENT_GUIDE.md   # Step-by-step deployment guide
│   ├── IMPROVEMENTS_SUMMARY.md # List of improvements
│   ├── COMPLETION_CHECKLIST.md # Completion status report
│   └── FILE_INVENTORY.md     # File reference guide
│
├── models/                   # Pre-trained ML models
│   ├── model.pkl            # Trained ExtraTreesClassifier (6.8 MB)
│   └── vectorizer.pkl       # TF-IDF Vectorizer (103 KB)
│
├── data/                     # Dataset files
│   ├── spam.csv             # Training dataset (5,572 SMS messages)
│   └── spam_raw.txt         # Raw dataset
│
├── src/                      # Source code utilities
│   └── export_model.py      # Model export/import utility
│
├── templates/                # Web templates
│   └── index.html           # Web UI (beautiful responsive design)
│
└── notebooks/                # Jupyter notebooks
    └── model.ipynb          # Model training notebook
```

## Directory Descriptions

### Root Level Files
- **app.py** - Main Flask web application with prediction routes
- **requirements.txt** - All Python package dependencies
- **Procfile** - Deployment configuration for Render/Heroku
- **render.yaml** - Render platform specific settings
- **runtime.txt** - Specifies Python version (3.11.7)
- **README.md** - Main project documentation
- **.gitignore** - Git configuration for ignoring files

### docs/ - Documentation
Complete documentation for the project:
- Setup and installation guide
- Deployment instructions for Render
- List of all improvements made
- Project completion checklist
- File inventory and references

### models/ - Machine Learning Models
Pre-trained models ready for deployment:
- **model.pkl** - Trained ExtraTreesClassifier (98.65% accuracy)
- **vectorizer.pkl** - TF-IDF Vectorizer (3000 features)

### data/ - Dataset
Training and raw data files:
- **spam.csv** - Cleaned SMS dataset (5,572 messages)
- **spam_raw.txt** - Raw data from UCI ML Repository

### src/ - Source Code
Utility scripts and helpers:
- **export_model.py** - Functions to save/load models

### templates/ - Web Interface
HTML templates for the web application:
- **index.html** - Beautiful responsive UI with gradient design

### notebooks/ - Jupyter Notebooks
Training notebooks:
- **model.ipynb** - Complete model training pipeline with documentation

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run locally:
   ```bash
   python app.py
   ```

3. Deploy on Render:
   - Follow docs/DEPLOYMENT_GUIDE.md

## Key Files Size

- model.pkl: 6.8 MB (trained model)
- model.ipynb: 1.2 MB (training notebook)
- vectorizer.pkl: 103 KB (text vectorizer)
- spam.csv: 486 KB (dataset)
- app.py: 7.2 KB (web app)

Total: ~8.5 MB

## Model Performance

- Accuracy: 98.65%
- Precision: 100%
- Recall: 89.31%
- F1-Score: 94.33%

## Support

For detailed information, refer to the documentation in the `docs/` directory.
