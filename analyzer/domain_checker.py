"""
Domain and recruiter email verification utilities for CareerScan.
Detects public webmail domains, company impersonation, and typo-squatting.
"""

import re

FREE_EMAIL_DOMAINS = {
    "gmail.com", "googlemail.com", "yahoo.com", "ymail.com", "outlook.com",
    "hotmail.com", "live.com", "msn.com", "aol.com", "icloud.com", "me.com",
    "mail.com", "protonmail.com", "proton.me", "zoho.com", "gmx.com",
    "yandex.com", "tutanota.com", "fastmail.com", "rediffmail.com"
}

SUSPICIOUS_TLDS = {
    ".xyz", ".top", ".site", ".online", ".work", ".click", ".buzz",
    ".loan", ".rest", ".fit", ".monster", ".bar"
}

WELL_KNOWN_TECH_BRANDS = {
    "google": ["google.com", "alphabet.com"],
    "microsoft": ["microsoft.com"],
    "amazon": ["amazon.com", "amazon.jobs"],
    "apple": ["apple.com"],
    "meta": ["meta.com", "fb.com", "facebook.com"],
    "netflix": ["netflix.com"],
    "tesla": ["tesla.com"],
    "stripe": ["stripe.com"],
    "salesforce": ["salesforce.com"],
    "adobe": ["adobe.com"],
    "intel": ["intel.com"],
    "cisco": ["cisco.com"],
    "ibm": ["ibm.com"],
    "oracle": ["oracle.com"],
    "uber": ["uber.com"],
    "airbnb": ["airbnb.com"],
    "twitter": ["x.com", "twitter.com"],
    "spotify": ["spotify.com"],
    "accenture": ["accenture.com"],
    "tcs": ["tcs.com"],
    "infosys": ["infosys.com"],
    "wipro": ["wipro.com"],
    "deloitte": ["deloitte.com"]
}


def analyze_recruiter_email(email_str, company_name=""):
    """
    Analyzes recruiter email for suspicious patterns:
    - Free/public email provider
    - Suspicious TLD
    - Mismatch with reputed company name
    """
    results = {
        "email": email_str.strip() if email_str else "",
        "domain": "",
        "is_free_provider": False,
        "is_suspicious_tld": False,
        "is_brand_mismatch": False,
        "brand_mismatch_details": "",
        "risk_points": 0,
        "flags": []
    }

    if not email_str:
        return results

    email_clean = email_str.strip().lower()
    match = re.search(r"@([a-z0-9.-]+\.[a-z]{2,})", email_clean)
    if not match:
        results["flags"].append({
            "category": "Email Verification",
            "title": "Invalid Recruiter Email Format",
            "severity": "Warning",
            "snippet": email_str,
            "description": "The provided recruiter email does not appear to have a valid domain structure."
        })
        results["risk_points"] += 15
        return results

    domain = match.group(1)
    results["domain"] = domain

    # 1. Check free email provider
    if domain in FREE_EMAIL_DOMAINS:
        results["is_free_provider"] = True
        severity = "High" if company_name else "Medium"
        points = 25 if company_name else 15
        results["risk_points"] += points
        results["flags"].append({
            "category": "Recruiter Identity",
            "title": f"Public Webmail Used (@{domain})",
            "severity": severity,
            "snippet": email_str,
            "description": (
                f"Legitimate corporate recruiters communicate using official company domain emails. "
                f"Using free public webmail (@{domain}) is a primary tactic of fraudulent recruiters."
            )
        })

    # 2. Check suspicious TLD
    for tld in SUSPICIOUS_TLDS:
        if domain.endswith(tld):
            results["is_suspicious_tld"] = True
            results["risk_points"] += 20
            results["flags"].append({
                "category": "Domain Credibility",
                "title": f"High-Risk Domain Extension ({tld})",
                "severity": "High",
                "snippet": email_str,
                "description": (
                    f"The email domain ends with '{tld}', an extension commonly used in disposable "
                    f"phishing operations due to low registration costs and minimal verification."
                )
            })
            break

    # 3. Check Brand vs Domain Mismatch
    if company_name:
        company_clean = re.sub(r"[^a-z0-9]", "", company_name.lower())
        for brand_key, official_domains in WELL_KNOWN_TECH_BRANDS.items():
            if brand_key in company_clean:
                # If stated company is a major enterprise, check if domain matches official domains
                matched_official = any(domain == off or domain.endswith("." + off) for off in official_domains)
                if not matched_official:
                    results["is_brand_mismatch"] = True
                    results["brand_mismatch_details"] = (
                        f"Company claimed: '{company_name}', but email domain is '@{domain}'. "
                        f"Official domain should be one of: {', '.join(official_domains)}"
                    )
                    results["risk_points"] += 35
                    results["flags"].append({
                        "category": "Corporate Impersonation",
                        "title": f"Brand Mismatch: Claiming {brand_key.capitalize()} without official domain",
                        "severity": "Critical",
                        "snippet": f"Company: '{company_name}' vs Email: '{email_str}'",
                        "description": (
                            f"The job claims to be from {company_name.title()}, but uses '{domain}' rather than "
                            f"the legitimate corporate domain ({official_domains[0]}). This strongly indicates an impersonation scam."
                        )
                    })
                break

    return results
