"""
Logging utility for sentiment analysis requests.
Stores logs in JSON format for easy parsing and analysis.
"""

import json
import os
from datetime import datetime
import uuid


LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "logs", "requests.json")


def log_request(
    request_type,
    success,
    review=None,
    prediction=None,
    probability=None,
    file_type=None,
    filename=None,
    error=None,
):
    """
    Log a request to the JSON file and return the log_id.

    Args:
        request_type (str): Type of request ('text' or 'file')
        success (bool): Whether the request was successful
        review (str, optional): Review text for text analysis
        prediction (str, optional): Prediction result (positive/negative)
        probability (float, optional): Confidence probability (0.0 to 1.0)
        file_type (str, optional): Type of file (csv/xlsx/xls)
        filename (str, optional): Name of uploaded file
        error (str, optional): Error message if failed

    Returns:
        str: The log_id of the created log entry
    """
    # Ensure log directory exists
    log_dir = os.path.dirname(LOG_FILE)
    os.makedirs(log_dir, exist_ok=True)

    # Generate unique log_id
    log_id = str(uuid.uuid4())

    # Create base log entry
    log_entry = {
        "log_id": log_id,
        "timestamp": datetime.now().isoformat(),
        "request_type": request_type,
        "success": success,
    }

    # Add fields based on request type
    if request_type == "text":
        if review is not None:
            log_entry["review"] = review
        if prediction is not None:
            log_entry["prediction"] = prediction
        if probability is not None:
            log_entry["probability"] = probability

    elif request_type == "file":
        if file_type is not None:
            log_entry["file_type"] = file_type
        if filename is not None:
            log_entry["filename"] = filename

    # Add error if present
    if error is not None:
        log_entry["error"] = error

    # Load existing logs
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            logs = []
    else:
        logs = []

    # Append new log entry
    logs.append(log_entry)

    # Save updated logs
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

    return log_id
