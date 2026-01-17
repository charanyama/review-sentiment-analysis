from flask import Flask
import pickle
import os
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

LR_MODEL_PATH = os.path.join(
    os.path.dirname(__file__), "..", "models", "logistic-regression-model.pkl"
)

VECTORIZER_PATH = os.path.join(
    os.path.dirname(__file__), "..", "vectorizers", "vectorizer.pkl"
)

with open(LR_MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(VECTORIZER_PATH, "rb") as f:
    vectorizer = pickle.load(f)

from app import routes

from app.log_routes import log_bp

# Register the blueprint
app.register_blueprint(log_bp)