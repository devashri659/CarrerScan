"""
Rule-based heuristic scam detection engine for CareerScan.
Scans offer text using regular expressions and domain patterns across 5 core risk categories.
"""

import re

RULES = [
    # ---------------- 1. FINANCIAL FRAUD & FAKE CHECKS ----------------
    {
        "id": "FIN_FAKE_CHECK",
        "category": "Financial Fraud",
        "title": "Cashier's Check / Equipment Reimbursement Scheme",
        "severity": "Critical",
        "points": 35,
        "patterns": [
            r"(?:cashier(?:'s)?\s*check|certified\s*check|equipment\s*check|advance\s*check|check\s*(?:of|for)\s*\$[\d,]+)",
            r"(?:deposit\s*the\s*check|send\s*you\s*a\s*check|mail\s*you\s*a\s*check|courier\s*(?:a\s*)?check)",
            r"(?:purchase|buy)\s*(?:home\s*office\s*)?(?:equipment|laptop|workstation|software)\s*(?:from|through)\s*(?:our|the)\s*(?:approved\s*)?vendor"
        ],
        "description": "Scammers send counterfeit checks, instructing candidates to deposit them and wire back 'excess' funds to a fake equipment vendor. When the check bounces days later, the victim loses their own money."
    },
    {
        "id": "FIN_IRREVERSIBLE_PAYMENT",
        "category": "Financial Fraud",
        "title": "Untraceable / Irreversible Payment Methods",
        "severity": "Critical",
        "points": 30,
        "patterns": [
            r"\b(bitcoin|cryptocurrency|crypto\s*wallet|usdt|eth|btc)\b",
            r"\b(western\s*union|moneygram|wire\s*transfer|wire\s*funds)\b",
            r"\b(gift\s*card|apple\s*gift\s*card|steam\s*card|google\s*play\s*card)\b",
            r"\b(zelle|cash\s*app|cashapp|venmo)\b"
        ],
        "description": "Legitimate employers never demand wire transfers, cryptocurrency, gift cards, or P2P apps (Zelle/CashApp) for business expenses or equipment purchases."
    },
    {
        "id": "FIN_UPFRONT_FEE",
        "category": "Financial Fraud",
        "title": "Upfront Fees / Security Deposit Required",
        "severity": "Critical",
        "points": 35,
        "patterns": [
            r"(?:training\s*fee|registration\s*fee|onboarding\s*fee|application\s*fee|processing\s*fee)",
            r"(?:security\s*deposit|refundable\s*deposit|refundable\s*fee|pay\s*\$[\d,]+\s*before)",
            r"(?:server\s*allocation\s*fee|certification\s*fee|background\s*check\s*fee)"
        ],
        "description": "Legitimate companies never ask job applicants or interns to pay upfront fees, registration deposits, or background check costs before starting work."
    },

    # ---------------- 2. SUSPICIOUS CHANNELS & INTERVIEW PRACTICES ----------------
    {
        "id": "COMM_UNOFFICIAL_APP",
        "category": "Communication Channel",
        "title": "Chat-Only Interview via Telegram / WhatsApp / Signal",
        "severity": "High",
        "points": 25,
        "patterns": [
            r"\b(telegram|whatsapp|signal\s*app)\b",
            r"(?:download\s*telegram|message\s*on\s*telegram|contact\s*via\s*telegram|interview\s*on\s*telegram)",
            r"(?:whatsapp\s*(?:chat|number|interview)|skype\s*chat\s*(?:only|text))",
            r"@[a-zA-Z0-9_]{4,}(?:\s*(?:on|via)\s*telegram)?"
        ],
        "description": "Corporate hiring managers conduct interviews via structured video platforms (Zoom, Teams, Google Meet) or in person. Scammers frequently use encrypted chat apps to remain anonymous."
    },
    {
        "id": "COMM_GENERIC_SALUTATION",
        "category": "Communication Channel",
        "title": "Impersonal or Generic Salutation",
        "severity": "Low",
        "points": 10,
        "patterns": [
            r"\b(dear\s*applicant|dear\s*candidate|dear\s*jobseeker|attn:\s*job\s*seeker|dear\s*beneficiary)\b",
            r"\b(dear\s*sir\s*/\s*madam|to\s*whom\s*it\s*may\s*concern)\b"
        ],
        "description": "Mass spam campaigns often use impersonal salutations without referencing your actual name or specific application history."
    },
    {
        "id": "COMM_FREE_EMAIL_IN_TEXT",
        "category": "Communication Channel",
        "title": "Free Public Email Provider in Message Text",
        "severity": "Medium",
        "points": 15,
        "patterns": [
            r"[a-zA-Z0-9._%+-]+@(gmail|yahoo|outlook|hotmail|aol|proton|mail)\.com"
        ],
        "description": "Official company recruitment correspondence originates from verified corporate domains rather than free webmail services."
    },

    # ---------------- 3. UNREALISTIC COMPENSATION & IMMEDIATE HIRING ----------------
    {
        "id": "COMP_UNREALISTIC_PAY",
        "category": "Offer Realism",
        "title": "Unrealistic Compensation for Minimal / Entry-Level Work",
        "severity": "High",
        "points": 25,
        "patterns": [
            r"(?:data\s*entry|typing|virtual\s*assistant|online\s*assistant|clerk)[\s\S]{1,60}\$(?:[5-9]\d|[1-9]\d{2})\s*(?:per\s*hour|/hr|/hour|hourly)",
            r"\$(?:[5-9]\d|[1-9]\d{2})\s*(?:per\s*hour|/hr|/hour)[\s\S]{1,60}(?:no\s*experience|data\s*entry|entry\s*level)",
            r"(?:earn|make)\s*\$(?:[2-9],\d{3}|\d{4,})\s*(?:per\s*week|weekly|every\s*week)[\s\S]{1,40}(?:hours?\s*a\s*day|part[\s-]*time)"
        ],
        "description": "Offering $50-$90/hour for basic data entry, typing, or entry-level tasks with no prior experience is a hallmark bait tactic of employment fraud."
    },
    {
        "id": "COMP_INSTANT_HIRE",
        "category": "Offer Realism",
        "title": "Instant Job Offer Without Formal Interview",
        "severity": "High",
        "points": 25,
        "patterns": [
            r"(?:selected\s*immediately|hired\s*on\s*the\s*spot|selected\s*without\s*(?:an?\s*)?interview)",
            r"(?:direct\s*appointment\s*letter|immediate\s*commencement\s*without\s*interview)",
            r"(?:no\s*interview\s*rounds?|no\s*prior\s*experience\s*(?:is\s*)?required)"
        ],
        "description": "Legitimate employers never extend binding job offers without conducting at least one rigorous interview and evaluating past qualifications."
    },

    # ---------------- 4. URGENCY & PSYCHOLOGICAL PRESSURE ----------------
    {
        "id": "URG_PRESSURE_TACTIC",
        "category": "Urgency & Tactics",
        "title": "Artificial Urgency & Pressure Deadlines",
        "severity": "Medium",
        "points": 15,
        "patterns": [
            r"(?:within\s*24\s*hours|offer\s*(?:closes|expires)\s*today|accept\s*within\s*48\s*hours)",
            r"(?:strictly\s*confidential|do\s*not\s*contact\s*(?:our\s*)?(?:corporate\s*)?office)",
            r"(?:limited\s*(?:slots|seats|vacancies)\s*remaining|urgent\s*requirement|lock\s*your\s*position)"
        ],
        "description": "Scammers impose tight artificial deadlines (e.g. 24 hours) to prevent victims from consulting mentors, university career counselors, or researching the company."
    },

    # ---------------- 5. SENSITIVE DATA HARVESTING ----------------
    {
        "id": "DATA_PREMATURE_SSN",
        "category": "Identity Harvesting",
        "title": "Premature Request for Sensitive Identity / Financial Data",
        "severity": "Critical",
        "points": 30,
        "patterns": [
            r"\b(social\s*security\s*number|ssn|bank\s*routing\s*number|mother'?s\s*maiden\s*name)\b",
            r"(?:copy\s*of\s*(?:passport|driver'?s\s*license|photo\s*id)[\s\S]{1,40}(?:before\s*the\s*interview|prior\s*to\s*interview|instant\s*payroll))"
        ],
        "description": "Demanding Social Security Numbers or bank routing details in email text or before official secure HR onboarding indicates identity theft risk."
    }
]


def run_heuristic_checks(text, company="", email=""):
    """
    Executes rule-based matching across the offer text.
    Extracts matched snippets, computes category scores, and compiles detailed red flags.
    """
    matched_flags = []
    total_points = 0
    categories_hit = set()

    for rule in RULES:
        rule_matched = False
        matched_snippet = None

        for pattern in rule["patterns"]:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                rule_matched = True
                # Extract surrounding context snippet (up to 120 chars)
                start = max(0, match.start() - 25)
                end = min(len(text), match.end() + 35)
                matched_snippet = text[start:end].strip()
                break

        if rule_matched:
            total_points += rule["points"]
            categories_hit.add(rule["category"])
            matched_flags.append({
                "id": rule["id"],
                "category": rule["category"],
                "title": rule["title"],
                "severity": rule["severity"],
                "points": rule["points"],
                "snippet": f"...{matched_snippet}..." if matched_snippet else "",
                "description": rule["description"]
            })

    # Normalize heuristic score to 0 - 100
    # Capped at 100
    heuristic_score = min(100, total_points)

    return {
        "score": heuristic_score,
        "flags": matched_flags,
        "flags_count": len(matched_flags),
        "categories_affected": list(categories_hit)
    }
