"""
SQLite Database Manager for CareerScan Scan History.
Provides persistent storage, querying, and deletion of risk assessment reports.
"""

import os
import sqlite3
import json
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "careerscan.db")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            company_name TEXT,
            recruiter_email TEXT,
            snippet TEXT,
            risk_score INTEGER,
            risk_level TEXT,
            badge_color TEXT,
            flags_count INTEGER,
            report_json TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_scan(result, raw_text):
    """
    Saves an analysis report into SQLite database.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create a short snippet from the raw text for list display
    clean_text = " ".join(raw_text.split())
    snippet = clean_text[:140] + ("..." if len(clean_text) > 140 else "")

    now_iso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO scans (
            timestamp, company_name, recruiter_email, snippet,
            risk_score, risk_level, badge_color, flags_count, report_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        now_iso,
        result.get("company_name", ""),
        result.get("recruiter_email", ""),
        snippet,
        result.get("risk_score", 0),
        result.get("risk_level", "Unknown"),
        result.get("badge_color", "#0866E8"),
        result.get("flags_count", 0),
        json.dumps(result)
    ))

    scan_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return scan_id


def get_all_scans(limit=100):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, timestamp, company_name, recruiter_email, snippet,
               risk_score, risk_level, badge_color, flags_count
        FROM scans
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_scan_by_id(scan_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scans WHERE id = ?", (scan_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        data = dict(row)
        data["report"] = json.loads(data["report_json"])
        return data
    return None


def delete_scan(scan_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM scans WHERE id = ?", (scan_id,))
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0


def clear_all_scans():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM scans")
    conn.commit()
    conn.close()
    return True
