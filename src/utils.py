import pandas as pd
from src.setiment import predict_sentiment, predict_sentiment_with_proba


def predict_csv(df: pd.DataFrame, col: str) -> pd.DataFrame:
    res = predict_sentiment_with_proba(df, col)

    res_df = pd.DataFrame()
    res_df[col] = df[col]

    res_df["lr_sentiment"] = res["lr"]["lr_predictions"]
    res_df["nb_sentiment"] = res["nb"]["nb_predictions"]
    res_df["svm_sentiment"] = res["svm"]["svm_predictions"]

    res_df["lr_probability"] = res["lr"]["lr_probs"]
    res_df["nb_probability"] = res["nb"]["nb_probs"]
    res_df["svm_probability"] = res["svm"]["svm_probs"]

    return res_df


def predict_excel(df: pd.DataFrame, col: str) -> pd.DataFrame:
    preds = predict_sentiment(df, col)
    df["lr_sentiment"] = preds["lr_predictions"]
    df["nb_sentiment"] = preds["nb_predictions"]
    df["svm_sentiment"] = preds["svm_predictions"]
    return df
