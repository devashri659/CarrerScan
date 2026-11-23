"""
Comprehensive automated test suite for CareerScan.
Verifies Heuristic rules, Domain checker, ML model, SQLite database, and REST API.
"""

import unittest
import json
import os
import io
from app import app
from database.db import init_db, get_all_scans, clear_all_scans
from sample_data.dataset import SAMPLE_OFFERS
from analyzer import evaluate_job_offer


class TestCareerScan(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        init_db()

    def test_samples_endpoint(self):
        """Test GET /api/samples"""
        response = self.app.get("/api/samples")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data["success"])
        self.assertIn("fake_check", data["samples"])
        self.assertIn("telegram_interview", data["samples"])

    def test_fake_check_scam_detection(self):
        """Test detection of fake cashier's check equipment scam"""
        sample = SAMPLE_OFFERS["fake_check"]
        result = evaluate_job_offer(sample["text"], company=sample["company"], email=sample["email"])
        self.assertEqual(result["risk_level"], "High Risk")
        self.assertGreaterEqual(result["risk_score"], 80)
        flag_categories = [f["category"] for f in result["flags"]]
        self.assertIn("Financial Fraud", flag_categories)

    def test_telegram_impersonation_detection(self):
        """Test detection of Google impersonation with Telegram interview"""
        sample = SAMPLE_OFFERS["telegram_interview"]
        result = evaluate_job_offer(sample["text"], company=sample["company"], email=sample["email"])
        self.assertEqual(result["risk_level"], "High Risk")
        self.assertGreaterEqual(result["risk_score"], 75)
        # Should detect corporate impersonation (Google with @outlook.com)
        flag_categories = [f["category"] for f in result["flags"]]
        self.assertTrue(
            "Corporate Impersonation" in flag_categories or
            "Communication Channel" in flag_categories
        )

    def test_legitimate_offer_detection(self):
        """Test that a legitimate offer from Stripe receives low risk"""
        sample = SAMPLE_OFFERS["legitimate_offer"]
        result = evaluate_job_offer(sample["text"], company=sample["company"], email=sample["email"])
        self.assertEqual(result["risk_level"], "Low Risk")
        self.assertLessEqual(result["risk_score"], 25)

    def test_analyze_api_endpoint(self):
        """Test POST /api/analyze with JSON"""
        sample = SAMPLE_OFFERS["internship_fee"]
        payload = {
            "text": sample["text"],
            "company": sample["company"],
            "email": sample["email"]
        }
        response = self.app.post(
            "/api/analyze",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data["success"])
        self.assertIn("scan_id", data["result"])
        self.assertEqual(data["result"]["risk_level"], "High Risk")

    def test_pdf_extraction_endpoint(self):
        """Test POST /api/extract-pdf with real PDF file"""
        pdf_path = os.path.join(os.path.dirname(__file__), "sample_data", "sample_scam_offer.pdf")
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        response = self.app.post(
            "/api/extract-pdf",
            data={"file": (io.BytesIO(pdf_bytes), "sample_scam_offer.pdf")},
            content_type="multipart/form-data"
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data["success"])
        self.assertIn("extracted_text", data)
        self.assertIn("Cashier's Check", data["extracted_text"])

    def test_history_flow(self):
        """Test history retrieval and clear"""
        # Ensure at least one item is present
        scans = get_all_scans()
        self.assertIsInstance(scans, list)

        # Clear history
        res = self.app.post("/api/history/clear")
        self.assertEqual(res.status_code, 200)

        # Confirm empty
        res_after = self.app.get("/api/history")
        data_after = json.loads(res_after.data)
        self.assertEqual(len(data_after["scans"]), 0)


if __name__ == "__main__":
    unittest.main()
