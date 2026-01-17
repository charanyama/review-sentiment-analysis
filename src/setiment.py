import pandas as pd
import pickle
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

LR_MODEL_PATH = os.path.join(BASE_DIR, "models", "logistic-regression-model.pkl")
NB_MODEL_PATH = os.path.join(BASE_DIR, "models", "naive-bayes-model.pkl")
SVM_MODEL_PATH = os.path.join(BASE_DIR, "models", "svm-model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "vectorizers", "vectorizer.pkl")


def load_model(path):
    with open(path, "rb") as f:
        return pickle.load(f)


def load_vectorizer():
    with open(VECTORIZER_PATH, "rb") as f:
        return pickle.load(f)


# Load once
lr_model = load_model(LR_MODEL_PATH)
nb_model = load_model(NB_MODEL_PATH)
svm_model = load_model(SVM_MODEL_PATH)
vectorizer = load_vectorizer()


def predict_sentiment(df: pd.DataFrame, col: str):
    df.columns = df.columns.str.lower()

    if col not in df.columns:
        raise ValueError(f"Column '{col}' not found")

    texts = df[col].fillna("").astype(str)
    vecs = vectorizer.transform(texts)

    return {
        "lr_predictions": lr_model.predict(vecs).tolist(),
        "nb_predictions": nb_model.predict(vecs).tolist(),
        "svm_predictions": svm_model.predict(vecs).tolist(),
    }


def predict_sentiment_with_proba(df: pd.DataFrame, col: str):
    df.columns = df.columns.str.lower()

    if col not in df.columns:
        raise ValueError(f"Column '{col}' not found")

    texts = df[col].fillna("").astype(str)
    vecs = vectorizer.transform(texts)

    return {
        "lr": {
            "lr_predictions": lr_model.predict(vecs).tolist(),
            "lr_probs": lr_model.predict_proba(vecs).max(axis=1).tolist(),
        },
        "nb": {
            "nb_predictions": nb_model.predict(vecs).tolist(),
            "nb_probs": nb_model.predict_proba(vecs).max(axis=1).tolist(),
        },
        "svm": {
            "svm_predictions": svm_model.predict(vecs).tolist(),
            "svm_probs": svm_model.predict_proba(vecs).max(axis=1).tolist(),
        },
    }
