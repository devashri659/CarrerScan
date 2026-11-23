"""
CareerScan - AI-Powered Job Offer Risk Checker
Flask Application & REST Endpoints
"""

import os
import io
import traceback
from flask import Flask, render_template, request, jsonify
import pypdf

from analyzer import evaluate_job_offer
from database.db import (
    init_db, save_scan, get_all_scans,
    get_scan_by_id, delete_scan, clear_all_scans
)
from sample_data.dataset import SAMPLE_OFFERS

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB max upload

# Initialize database tables
init_db()


def extract_text_from_pdf(file_bytes):
    """
    Extracts text from uploaded PDF offer letter.
    """
    stream = io.BytesIO(file_bytes)
    reader = pypdf.PdfReader(stream)
    extracted = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            extracted.append(page_text)
    return "\n\n".join(extracted)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/samples", methods=["GET"])
def get_samples():
    """Returns preset test cases for instant demonstration."""
    return jsonify({
        "success": True,
        "samples": SAMPLE_OFFERS
    })


@app.route("/api/extract-pdf", methods=["POST"])
def extract_pdf():
    """
    Extracts text from an uploaded PDF or TXT offer letter.
    """
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"}), 400

    uploaded_file = request.files["file"]
    if uploaded_file.filename == "":
        return jsonify({"success": False, "error": "Empty filename"}), 400

    filename = uploaded_file.filename.lower()
    file_bytes = uploaded_file.read()

    try:
        if filename.endswith(".pdf"):
            text = extract_text_from_pdf(file_bytes)
        elif filename.endswith((".txt", ".text")):
            text = file_bytes.decode("utf-8", errors="ignore")
        else:
            return jsonify({
                "success": False,
                "error": "Unsupported file format. Please upload a PDF (.pdf) or Text (.txt) file."
            }), 400

        if not text.strip():
            return jsonify({
                "success": False,
                "error": "Could not extract readable text from this document. It may be scanned or empty."
            }), 400

        return jsonify({
            "success": True,
            "filename": uploaded_file.filename,
            "extracted_text": text
        })
    except Exception as e:
        return jsonify({"success": False, "error": f"Failed to parse document: {str(e)}"}), 500


@app.route("/api/analyze", methods=["POST"])
def analyze_offer():
    """
    Primary analysis endpoint.
    Accepts JSON or multipart/form-data.
    """
    try:
        text = ""
        company = ""
        email = ""

        if request.is_json:
            data = request.get_json() or {}
            text = data.get("text", "")
            company = data.get("company", "")
            email = data.get("email", "")
        else:
            text = request.form.get("text", "")
            company = request.form.get("company", "")
            email = request.form.get("email", "")

            # If user attached a file directly with the form
            if "file" in request.files:
                uploaded_file = request.files["file"]
                if uploaded_file and uploaded_file.filename != "":
                    filename = uploaded_file.filename.lower()
                    file_bytes = uploaded_file.read()
                    if filename.endswith(".pdf"):
                        extracted = extract_text_from_pdf(file_bytes)
                        if extracted.strip():
                            text = extracted
                    elif filename.endswith((".txt", ".text")):
                        text = file_bytes.decode("utf-8", errors="ignore")

        if not text or not text.strip():
            return jsonify({
                "success": False,
                "error": "Please provide job offer text or upload a valid offer letter."
            }), 400

        # Perform comprehensive risk assessment
        result = evaluate_job_offer(text, company=company, email=email)

        # Store in SQLite scan history
        scan_id = save_scan(result, text)
        result["scan_id"] = scan_id

        return jsonify({
            "success": True,
            "result": result
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": f"Internal analysis error: {str(e)}"
        }), 500


@app.route("/api/history", methods=["GET"])
def get_history():
    """Returns user's past scan reports."""
    scans = get_all_scans()
    return jsonify({
        "success": True,
        "scans": scans
    })


@app.route("/api/history/<int:scan_id>", methods=["GET"])
def get_history_detail(scan_id):
    """Retrieves full details for a previous scan."""
    scan = get_scan_by_id(scan_id)
    if not scan:
        return jsonify({"success": False, "error": "Scan record not found"}), 404
    return jsonify({
        "success": True,
        "scan": scan
    })


@app.route("/api/history/<int:scan_id>", methods=["DELETE"])
def delete_history_item(scan_id):
    """Deletes a specific scan record."""
    success = delete_scan(scan_id)
    if success:
        return jsonify({"success": True})
    return jsonify({"success": False, "error": "Record not found or already deleted"}), 404


@app.route("/api/history/clear", methods=["POST"])
def clear_history():
    """Clears all scan history."""
    clear_all_scans()
    return jsonify({"success": True, "message": "History cleared successfully"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
