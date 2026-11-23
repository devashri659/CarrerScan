# CareerScan 
### AI-Powered Job & Internship Scam Detection

CareerScan is a Python-based AI agent that helps students identify potential job and internship scams by analyzing job offers and detecting suspicious recruiter information.

## Features
- **Scam Detection:** Identifies suspicious patterns using rule-based checks and machine learning.
- **Risk Assessment:** Generates a risk score and highlights potential red flags.
- **Email Verification:** Flags suspicious recruiter email domains and possible company impersonation.
- **PDF Analysis:** Extracts and analyzes text from job offer documents.
- **Scan History:** Stores previous analysis results for future reference.

## Tech Stack
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask
- **Machine Learning:** Scikit-learn, TF-IDF, Logistic Regression
- **Database:** SQLite
- **PDF Processing:** pypdf

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/devashri659/CarrerScan.git
   ```

2. Navigate to the project folder:
   ```bash
   cd CarrerScan
   ```

3. Install the dependencies:
   ```bash
   pip install flask scikit-learn pypdf joblib
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Open `http://127.0.0.1:5000` in your browser.

## Disclaimer
CareerScan provides risk assessments based on detected patterns. It cannot guarantee whether a job offer is genuine or fraudulent. Always verify opportunities through official company channels.
