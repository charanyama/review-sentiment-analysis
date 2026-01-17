# Review Sentiment Analysis

A comprehensive web application for sentiment analysis of reviews using machine learning. Analyze text reviews or batch process CSV/Excel files with multiple ML models (Logistic Regression, Naive Bayes, SVM) and track all your analysis requests with detailed logging.

## Features

- **Text Analysis**: Analyze individual reviews in real-time with sentiment predictions
- **Batch File Processing**: Upload and analyze CSV/Excel files with multiple reviews
- **Multiple Models**: Compare predictions from three ML algorithms:
  - Logistic Regression
  - Naive Bayes
  - Support Vector Machine (SVM)
- **Confidence Scores**: Get probability scores alongside predictions
- **Request Tracking**: View complete history of all analysis requests with timestamps
- **Responsive UI**: Modern, user-friendly web interface
- **CORS Enabled**: Ready for API integration

## Table of Contents

- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Models & Training](#models--training)
- [Technologies](#technologies)
- [Configuration](#configuration)
- [Contributing](#contributing)

## Installation

### Prerequisites

- Python 3.8+
- pip or conda package manager

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/review-sentiment-analysis.git
   cd review-sentiment-analysis
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install flask flask-cors pandas scikit-learn python-dotenv openpyxl
   ```

4. **Configure environment variables**
   
   Create a .env file in the root directory.
   
   Edit `.env` file:
   ```
   HOST=0.0.0.0
   PORT=3000
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

6. **Access the web interface**
   Open your browser and navigate to: `http://localhost:3000`

## 📁 Project Structure

```
review-sentiment-analysis/
├── app/                          # Flask application
│   ├── __init__.py              # App initialization & model loading
│   ├── routes.py                # Main route handlers
│   ├── log_routes.py            # Request logging routes
│   ├── static/                  # Static assets
│   │   ├── index.css
│   │   ├── file.css
│   │   └── file.js
│   └── templates/               # HTML templates
│       ├── index.html           # Home page
│       ├── file.html            # File upload page
│       ├── text.html            # Text analysis page
│       └── components/          # Reusable components
│           ├── request_detail.html
│           └── request_item.html
│
├── src/                         # Source utilities
│   ├── sentiment.py             # Core sentiment prediction logic
│   ├── utils.py                 # Helper functions for CSV/Excel processing
│   └── logging_utils.py         # Request logging utilities
│
├── models/                      # Pre-trained ML models (pickled)
│   ├── logistic-regression-model.pkl
│   ├── naive-bayes-model.pkl
│   └── svm-model.pkl
│
├── vectorizers/                 # Trained text vectorizer
│   └── vectorizer.pkl           # TF-IDF vectorizer (fitted)
│
├── data/                        # Dataset information
│   ├── imdb-review-dataset.csv
│   └── README.md
│
├── notebooks/                   # Jupyter notebooks for model training
│   ├── logistic_regression.ipynb
│   ├── naive_bayes.ipynb
│   └── svm.ipynb
│
├── logs/                        # Request logs
│   └── requests.json            # JSON-formatted request history
│
├── main.py                      # Application entry point
├── main.ipynb                   # Main notebook
└── README.md                    # This file
```

## Web Interface UI

#### 1. **Analyze Single Review (Text)**
   - Click on "Analyze Text" or navigate to `/analyze/text`
   - Enter your review text
   - View sentiment prediction and confidence score
   - All requests are logged automatically

#### 2. **Analyze Multiple Reviews (File)**
   - Click on "Analyze File" or navigate to `/analyze/file`
   - Upload a CSV or Excel file
   - Specify the column name containing reviews (default: "review")
   - Download results with sentiment predictions and probabilities
   - File is logged with success/error status

#### 3. **View Request History**
   - Home page displays all previous analysis requests
   - Click on any request to view detailed results
   - Requests show timestamp, type, and status

### API Endpoints

#### Analyze Text
```bash
POST /predict
Content-Type: application/x-www-form-urlencoded

review=Great movie! I loved it.
```

**Response:**
```json
{
  "message": "Sentiment analyzed",
  "prediction": "positive",
  "probability": 0.95,
  "log_id": "uuid-string"
}
```

#### Analyze File
```bash
POST /analyze/file
Content-Type: multipart/form-data

fileInput: <CSV/Excel file>
featureColumn: review
```

**Response:**
```json
{
  "message": "Sentiment analysis completed",
  "columns": ["review", "lr_sentiment", "nb_sentiment", "svm_sentiment", "lr_probability", "nb_probability", "svm_probability"],
  "sentiment": [
    {
      "review": "Great movie!",
      "lr_sentiment": "positive",
      "nb_sentiment": "positive",
      "svm_sentiment": "positive",
      "lr_probability": 0.95,
      "nb_probability": 0.92,
      "svm_probability": 0.89
    }
  ],
  "log_id": "uuid-string"
}
```

#### Get Request Logs
```bash
GET /api/logs
```

#### Get Specific Request
```bash
GET /api/logs/<log_id>
```

## Models & Training

### Trained Models

The application uses three pre-trained classification models:

1. **Logistic Regression**: Fast, interpretable, good baseline
2. **Naive Bayes**: Probabilistic model, works well with text
3. **SVM**: Powerful classifier, high accuracy

### Text Vectorization

- **Vectorizer**: TF-IDF (Term Frequency-Inverse Document Frequency)
- **Training Data**: IMDB Movie Reviews Dataset (50,000 reviews)
- **Labels**: Positive/Negative sentiment (binary classification)

### Training Notebooks

Model training code and evaluation metrics are available in `/notebooks/`:
- `logistic_regression.ipynb` - Logistic Regression training
- `naive_bayes.ipynb` - Naive Bayes training
- `svm.ipynb` - SVM training

To retrain models:
1. Prepare your dataset
2. Update the notebook with your data path
3. Run the notebook to train and save models
4. Models will be saved to `/models/` directory

## Technologies

**Backend:**
- Flask - Web framework
- Pandas - Data processing
- Scikit-learn - Machine learning models
- Python-dotenv - Environment configuration

**Frontend:**
- HTML5 / CSS3
- JavaScript (Vanilla)
- Responsive design

**Data Processing:**
- CSV parsing
- Excel file support (.xlsx, .xls)
- JSON logging

## Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Server Configuration
HOST=0.0.0.0
PORT=3000

# Optional: Flask Configuration
FLASK_ENV=production
DEBUG=False
```

### Model Paths

Models are automatically loaded from:
- `models/logistic-regression-model.pkl`
- `models/naive-bayes-model.pkl`
- `models/svm-model.pkl`
- `vectorizers/vectorizer.pkl`

To use custom models, update the paths in `app/__init__.py`

## Request Logging

All requests are logged to `logs/requests.json` with:
- Unique log ID (UUID)
- Timestamp (ISO format)
- Request type (text/file)
- Success/failure status
- Input data and predictions
- Error messages (if applicable)

Example log entry:
```json
{
  "log_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2026-01-17T10:30:45.123456",
  "request_type": "text",
  "success": true,
  "review": "Amazing product, highly recommend!",
  "prediction": "positive",
  "probability": 0.97
}
```

## Error Handling

The application gracefully handles:
- Missing file uploads
- Invalid file formats
- Missing or incorrect column names
- Empty review text
- File processing errors
- Model prediction failures

All errors are logged with descriptive messages for debugging.

## Performance

- **Single Review Analysis**: < 100ms
- **Batch File Processing**: Depends on file size (processes 1000+ reviews/second)
- **Model Predictions**: Vectorization and prediction combined < 50ms per review

## Security

- CORS enabled for safe cross-origin requests
- Input validation on all routes
- Error messages don't expose sensitive information
- File upload size validation

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request