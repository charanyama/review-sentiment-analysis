from flask import Blueprint, jsonify, send_file, redirect, url_for
import os
import json
from io import BytesIO

log_bp = Blueprint("log_bp", __name__)

# Path to JSON log file
LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "logs", "requests.json")


def load_requests():
    """Load all past requests from JSON file."""
    if not os.path.exists(LOG_FILE):
        return []

    try:
        with open(LOG_FILE, "r") as f:
            requests = json.load(f)
        return requests
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_requests(requests):
    """Save requests to JSON file."""
    log_dir = os.path.dirname(LOG_FILE)
    os.makedirs(log_dir, exist_ok=True)

    with open(LOG_FILE, "w") as f:
        json.dump(requests, f, indent=2)


@log_bp.route("/api/requests", methods=["GET"])
def get_all_requests():
    """Return all past requests as JSON."""
    requests = load_requests()
    return jsonify({"requests": requests})


@log_bp.route("/api/request/<log_id>", methods=["GET"])
def get_request(log_id):
    """Return a specific request by log_id."""
    requests = load_requests()
    for req in requests:
        if req.get("log_id") == log_id:
            return jsonify(req)
    return jsonify({"error": "Request not found"}), 404


@log_bp.route("/api/request/<log_id>/delete", methods=["POST"])
def delete_log(log_id):
    """Delete a request from the JSON log."""
    requests = load_requests()

    # Filter out the request to delete
    updated_requests = [req for req in requests if req.get("log_id") != log_id]

    if len(updated_requests) == len(requests):
        return jsonify({"error": "Request ID not found"}), 404

    # Save updated requests
    save_requests(updated_requests)

    # Redirect to home page
    return redirect(url_for("home"))


@log_bp.route("/api/request/<log_id>/download", methods=["GET"])
def download_log(log_id):
    """Download request details as JSON file."""
    requests = load_requests()

    for req in requests:
        if req.get("log_id") == log_id:
            # Create in-memory file
            data_bytes = BytesIO()
            data_bytes.write(json.dumps(req, indent=2).encode("utf-8"))
            data_bytes.seek(0)

            return send_file(
                data_bytes,
                as_attachment=True,
                download_name=f"request_{log_id}.json",
                mimetype="application/json",
            )

    return jsonify({"error": "Request ID not found"}), 404
