# CareerScan — AI-Powered Job Offer Risk Checker
**Final-Year Computer Engineering Project**

CareerScan is a full-stack web application designed to protect students, fresh graduates, and job seekers from recruitment scams, fraudulent remote employment offers, suspicious recruiters, and deceptive internship listings.

---

## 1. System Architecture & Detection Engine

CareerScan uses a **Hybrid Multi-Layered Analysis Pipeline**:

```
+-------------------------------------------------------------+
|                        Frontend UI                          |
|    Modern SaaS Dashboard (HTML5, CSS3, Vanilla JS, Lucide)  |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                 Flask REST API Backend                      |
|            Routes: /api/analyze, /api/extract-pdf           |
+------------------------------+------------------------------+
                               |
               +---------------+---------------+
               |                               |
               v                               v
    +-----------------------+      +-----------------------+
    | Heuristic Rules Engine|      | Scikit-Learn ML Model |
    |  - 5 Risk Categories  |      |  - TF-IDF N-grams     |
    |  - Regex Pattern Scan |      |  - Logistic Regression|
    |  - Snippet Extraction |      |  - Probability Metric |
    +-----------+-----------+      +-----------+-----------+
                |                              |
                +---------------+--------------+
                                |
                                v
               +--------------------------------+
               | Recruiter & Domain Verification|
               |  - Public Webmail Detection    |
               |  - Corporate Brand Mismatch    |
               +----------------+---------------+
                                |
                                v
               +--------------------------------+
               |   Composite Risk Assessment    |
               |     (0–100% Score & Verdict)   |
               +----------------+---------------+
                                |
                                v
               +--------------------------------+
               |  SQLite Persistent Audit Log   |
               |      (scans database table)    |
               +--------------------------------+
```

### The 5 Heuristic Fraud Vectors:
1. **Financial Fraud & Fake Checks:** Counterfeit cashier's checks, overpayment reimbursement traps, wire transfers (Western Union, MoneyGram), cryptocurrency (Bitcoin, USDT), and gift cards.
2. **Upfront Fees:** Mandatory training charges, background check fees, server fees, registration deposits.
3. **Suspicious Channels:** Interviews conducted exclusively via Telegram, WhatsApp, or text-only Skype; anonymous recruitment.
4. **Offer Realism & Compensation:** Exorbitant pay ($60–$90/hr) for unskilled/entry-level data entry, immediate selection without interview.
5. **Urgency & Data Harvesting:** Artificial 24-hour expiration deadlines, demands for SSN, passport, or banking credentials before onboarding.

---

## 2. Technology Stack

- **Frontend:**
  - Semantic HTML5
  - Modern CSS3 (CSS Variables, Flexbox, CSS Grid, Responsive Design)
  - Vanilla JavaScript (ES6+, asynchronous Fetch API, state management)
  - Lucide Icons (clean, modern SVG icons)
  - Inter Google Typography

- **Backend:**
  - Python 3
  - Flask (REST API, multipart file uploads, JSON endpoints)
  - pypdf (server-side PDF parsing and text extraction)

- **Machine Learning & NLP:**
  - Scikit-learn (TfidfVectorizer with unigram & bigram features, Logistic Regression classifier)
  - Joblib (model serialization and caching)

- **Database:**
  - SQLite (persistent audit log of all scans, scores, and timestamps)

---

## 3. Visual & Design System

The application strictly implements the required SaaS dashboard specifications:

| Element | Specification | Hex / Value |
| :--- | :--- | :--- |
| **Sidebar Background** | Deep Navy Blue | `#0B2347` |
| **Sidebar Active Item** | Bright SaaS Blue | `#0866E8` |
| **Primary Accent Color** | Bright Blue | `#0866E8` |
| **Typography Color** | Dark Navy Text | `#102B50` |
| **Workspace Background**| Light Slate Gray | `#F7F9FC` |
| **Card Background** | Pure White | `#FFFFFF` |
| **Input Borders** | Subtle Slate Blue | `#D5DEEC` |
| **Secondary Text** | Muted Blue-Gray | `#58677D` |
| **Success Indicator** | Emerald Green | `#218653` |
| **Warning Indicator** | Amber | `#D58A16` |
| **High-Risk Indicator** | Crimson Red | `#C83D4D` |

---

## 4. Quickstart Guide

### 1. Requirements:
- Python 3.10+
- Flask, Scikit-learn, pypdf (pre-installed in environment)

### 2. Start the Application:
```bash
cd "C:\Users\devas\.gemini\antigravity\scratch\careerscan"
python app.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

### 3. Run Automated Tests:
```bash
python test_app.py
```

---

## 5. Demonstration & Evaluation Features

1. **One-Click Quick Test Samples:**
   - **Sample 1:** Fake Check & Equipment Reimbursement Scam ($65/hr cashier check scheme).
   - **Sample 2:** Google Impersonation via Telegram Interview.
   - **Sample 3:** Paid Summer Internship with Mandatory $199 Training Fee.
   - **Sample 4:** Legitimate Tech Offer Letter (Stripe Software Engineer).

2. **PDF Offer Letter Upload:**
   - Drop or upload `.pdf` or `.txt` offer letters directly.
   - Pre-generated sample PDFs are available in `sample_data/`:
     - `sample_data/sample_scam_offer.pdf`
     - `sample_data/sample_legitimate_offer.pdf`

3. **Detailed Scan History:**
   - Saved automatically to SQLite (`careerscan.db`).
   - Filter by risk rating (All, High Risk, Moderate Risk, Low Risk).
   - Instant re-inspection of past reports.

4. **Print / Export Report:**
   - Formats the report for printing or saving as a PDF summary.
