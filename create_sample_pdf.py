"""
Script to generate sample PDF offer letters for testing PDF upload functionality.
Uses basic raw PDF stream syntax in pure Python.
"""
import os

def create_simple_pdf(filepath, title, lines):
    # Construct a minimal conforming PDF 1.4
    content_stream = "BT\n/F1 14 Tf\n50 720 Td\n"
    content_stream += f"({title}) Tj\n"
    content_stream += "ET\n"
    content_stream += "BT\n/F1 10 Tf\n50 690 Td\n14 TL\n"
    for line in lines:
        escaped = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        content_stream += f"({escaped}) '\n"
    content_stream += "ET\n"
    
    stream_len = len(content_stream.encode('latin1'))
    
    pdf = f"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>
endobj
4 0 obj
<< /Length {stream_len} >>
stream
{content_stream}endstream
endobj
5 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
xref
0 6
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000244 00000 n 
0000000{300 + stream_len:03d} 00000 n 
trailer
<< /Size 6 /Root 1 0 R >>
startxref
{370 + stream_len}
%%EOF
"""
    with open(filepath, "wb") as f:
        f.write(pdf.encode('latin1'))
    print(f"Created PDF: {filepath}")

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "sample_data")
    scam_lines = [
        "Position: Remote Executive Assistant / Data Entry Specialist",
        "Compensation: $65.00 per hour, 20 hours per week",
        "",
        "Dear Applicant,",
        "We are pleased to confirm your appointment at Global Logix Services.",
        "To establish your home office, a certified Cashier's Check of $3,800 will be mailed.",
        "You must deposit the check and wire the remaining balance of $3,200 via Zelle",
        "or Bitcoin to our accredited hardware supplier within 24 hours of receipt.",
        "",
        "Interview completed via Telegram chat. Contact @GlobalLogix_HR for assistance.",
        "Sincerely, HR Recruitment Team"
    ]
    create_simple_pdf(os.path.join(out_dir, "sample_scam_offer.pdf"), "GLOBAL LOGIX SERVICES - EMPLOYMENT OFFER", scam_lines)

    legit_lines = [
        "Position: Associate Software Engineer",
        "Location: Chicago, IL (Hybrid)",
        "Annual Base Salary: $95,000 with 401(k) matching",
        "",
        "Dear Candidate,",
        "We are excited to formally extend an offer of employment at CloudSphere Inc.",
        "Following your successful completion of our technical interview rounds,",
        "this letter summarizes the terms of your full-time role starting January 12.",
        "All onboarding documentation will be completed securely via our Workday portal.",
        "",
        "Sincerely,",
        "Talent Acquisition | CloudSphere Inc."
    ]
    create_simple_pdf(os.path.join(out_dir, "sample_legitimate_offer.pdf"), "CLOUDSPHERE INC - OFFICIAL OFFER LETTER", legit_lines)
