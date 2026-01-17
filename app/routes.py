from flask import render_template, request, jsonify, redirect, url_for
from app import app, model, vectorizer
from src.utils import predict_csv, predict_excel
from src.logging_utils import log_request
import pandas as pd
import json
import os


# Helper function to load requests from log file
def load_requests():
    """Load all requests from the log file"""
    log_file = os.path.join(os.path.dirname(__file__), "..", "logs", "requests.json")
    
    if not os.path.exists(log_file):
        return []
    
    try:
        with open(log_file, 'r') as f:
            return json.load(f)
    except:
        return []


# Helper function to get a specific request by log_id
def get_request_by_id(log_id):
    """Get a specific request by log_id"""
    requests = load_requests()
    for req in requests:
        if req.get('log_id') == log_id:
            return req
    return None


@app.route("/")
def home():
    """Main page with request list and details"""
    requests = load_requests()
    # Reverse to show newest first
    requests.reverse()
    
    # Get selected request if log_id is in query params
    selected_log_id = request.args.get('log_id')
    selected_request = None
    if selected_log_id:
        selected_request = get_request_by_id(selected_log_id)
    
    return render_template('index.html', 
                         requests=requests, 
                         selected_request=selected_request)


@app.route("/analyze/file", methods=["GET"])
def file_page():
    """File upload page with request list in sidebar"""
    requests = load_requests()
    requests.reverse()
    return render_template("file.html", requests=requests)


@app.route("/analyze/text", methods=["GET"])
def text_page():
    """Text analysis page with request list in sidebar"""
    requests = load_requests()
    requests.reverse()
    return render_template("text.html", requests=requests)


@app.route("/analyze/file", methods=["POST"])
def analyze_file():
    try:
        if "fileInput" not in request.files:
            raise ValueError("File not provided")

        file = request.files["fileInput"]

        if file.filename == "":
            raise ValueError("No file selected")

        col = request.form.get("featureColumn", 'review')
        col = col.lower()

        filename = file.filename.lower()

        if filename.endswith(".csv"):
            df = pd.read_csv(file)
            res_df = predict_csv(df, col)
            file_type = "csv"

        elif filename.endswith((".xlsx", ".xls")):
            df = pd.read_excel(file)
            res_df = predict_excel(df, col)
            file_type = "excel"

        else:
            raise ValueError("Unsupported file type")

        res_df = res_df.fillna("")

        # Log the request and get the log_id
        log_id = log_request(
            request_type="file",
            file_type=file_type,
            filename=file.filename,
            success=True,
        )

        # Check if request is from browser form (not AJAX)
        if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
            # Redirect to home page with the log_id to show the result
            return redirect(url_for('home', log_id=log_id))

        return jsonify(
            {
                "message": "Sentiment analysis completed",
                "columns": list(res_df.columns),
                "sentiment": res_df.to_dict(orient="records"),
                "log_id": log_id
            }
        )

    except Exception as e:
        log_request(
            request_type="file",
            success=False,
            error=str(e),
        )
        print(e)
        
        # Check if request is from browser form (not AJAX)
        if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
            # Redirect back to file page with error
            return render_template("file.html", 
                                 requests=load_requests()[::-1],
                                 error=str(e))
        
        return jsonify({"error": str(e)}), 500


@app.route("/predict", methods=["POST"])
def predict():
    data = request.form.get("review", "").strip()

    if not data:
        log_request(
            request_type="text",
            success=False,
            error="No review text provided",
        )
        
        # Check if request is from browser form (not AJAX)
        if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
            return render_template("text.html",
                                 requests=load_requests()[::-1],
                                 error="No review text provided")
        
        return jsonify({"error": "No review text provided"}), 400

    try:
        vectorized_input = vectorizer.transform([data])

        if vectorized_input.nnz == 0:
            response = {
                "review": data,
                "prediction": "neutral",
                "probability": 0.0,
            }

            log_id = log_request(
                request_type="text",
                review=data,
                prediction=response['prediction'],
                probability=response['probability'],
                success=True,
            )

            # Check if request is from browser form (not AJAX)
            if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
                return redirect(url_for('home', log_id=log_id))

            return jsonify({**response, "log_id": log_id})

        prediction = model.predict(vectorized_input)[0]
        probability = float(model.predict_proba(vectorized_input).max())

        response = {
            "review": data,
            "prediction": prediction,
            "probability": probability,
        }

        log_id = log_request(
            request_type="text",
            review=data,
            prediction=response['prediction'],
            probability=response['probability'],
            success=True,
        )

        # Check if request is from browser form (not AJAX)
        if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
            return redirect(url_for('home', log_id=log_id))

        return jsonify({**response, "log_id": log_id})

    except Exception as e:
        log_request(
            request_type="text",
            review=data,
            success=False,
            error=str(e),
        )
        
        # Check if request is from browser form (not AJAX)
        if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
            return render_template("text.html",
                                 requests=load_requests()[::-1],
                                 error=str(e))
        
        return jsonify({"error": str(e)}), 500