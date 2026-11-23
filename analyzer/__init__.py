"""
CareerScan Hybrid Risk Analysis Engine.
Combines Heuristic Rule Matching, Email/Domain Verification, and Machine Learning NLP.
"""

from .rules import run_heuristic_checks
from .domain_checker import analyze_recruiter_email
from .ml_model import predict_scam_probability


def evaluate_job_offer(text, company="", email=""):
    """
    Main evaluation pipeline. Returns structured risk score, severity level,
    matched red flags, ML metrics, domain audit, and safety advice.
    """
    if not text or not text.strip():
        return {
            "error": "No job offer text provided."
        }

    # 1. Run Heuristic Rules Engine
    heuristic = run_heuristic_checks(text, company=company, email=email)

    # 2. Run Domain & Recruiter Email Verification
    domain = analyze_recruiter_email(email, company_name=company)

    # 3. Run Machine Learning Classifier
    ml = predict_scam_probability(text)

    # Combine flags from heuristics and domain check
    all_flags = list(heuristic["flags"])
    if domain.get("flags"):
        all_flags.extend(domain["flags"])

    # 4. Calculate Composite Risk Score (0 - 100)
    # Heuristic weight: 45%, ML weight: 35%, Domain weight: 20%
    base_score = (
        0.45 * heuristic["score"] +
        0.35 * ml["probability"] +
        0.20 * min(100, domain["risk_points"] * 2.0)
    )

    # Critical overrides for definitive scam indicators
    has_critical_flag = any(f.get("severity") == "Critical" for f in all_flags)
    has_fake_check = any(f.get("id") == "FIN_FAKE_CHECK" for f in all_flags)
    has_upfront_fee = any(f.get("id") == "FIN_UPFRONT_FEE" for f in all_flags)
    has_brand_mismatch = domain.get("is_brand_mismatch", False)

    if (has_fake_check or has_upfront_fee or has_brand_mismatch) and base_score < 75:
        composite_score = max(base_score, 82.0)
    elif has_critical_flag and base_score < 65:
        composite_score = max(base_score, 68.0)
    else:
        composite_score = base_score

    final_score = int(round(min(100, max(0, composite_score))))

    # 5. Determine Risk Level & Visual Badge
    if final_score <= 25:
        risk_level = "Low Risk"
        badge_color = "#218653"  # Success green
        summary = "This offer exhibits characteristics typical of legitimate employment. Standard due diligence is still recommended."
    elif final_score <= 59:
        risk_level = "Moderate Risk"
        badge_color = "#D58A16"  # Warning amber
        summary = "Several suspicious elements were detected. Verify the recruiter's credentials through official channels before proceeding."
    else:
        risk_level = "High Risk"
        badge_color = "#C83D4D"  # Danger red
        summary = "Multiple high-severity scam indicators detected. Strong likelihood of employment fraud or financial theft."

    # 6. Generate Contextual Recommendations
    recommendations = []
    if any(f.get("category") == "Financial Fraud" for f in all_flags):
        recommendations.append("Never deposit checks sent by an employer to buy equipment or return surplus funds.")
        recommendations.append("Do not pay any 'training', 'registration', or 'equipment reservation' fee. Real jobs never charge fees.")

    if any(f.get("category") == "Corporate Impersonation" for f in all_flags) or domain.get("is_free_provider"):
        recommendations.append(f"Verify this recruiter on LinkedIn or contact {company or 'the company'} directly via their official website careers page.")

    if any(f.get("category") == "Communication Channel" for f in all_flags):
        recommendations.append("Insist on a formal video interview with cameras enabled. Avoid recruitment conducted solely via Telegram or text chat.")

    if any(f.get("category") == "Identity Harvesting" for f in all_flags):
        recommendations.append("Never email copies of your SSN, passport, or bank account details prior to signed onboarding contracts.")

    if not recommendations:
        recommendations = [
            "Confirm the job listing on the company's verified website careers page.",
            "Verify your interviewer's profile on LinkedIn to ensure they work for the organization.",
            "Review typical market salary ranges for this specific role and experience level."
        ]

    return {
        "risk_score": final_score,
        "risk_level": risk_level,
        "badge_color": badge_color,
        "summary": summary,
        "flags_count": len(all_flags),
        "flags": all_flags,
        "categories_affected": list(set(f.get("category") for f in all_flags)),
        "company_name": company.strip() if company else "Not specified",
        "recruiter_email": email.strip() if email else "Not specified",
        "domain_analysis": domain,
        "ml_metrics": {
            "scam_probability": ml["probability"],
            "top_keywords": ml.get("top_scam_keywords", []),
            "heuristic_score": heuristic["score"]
        },
        "recommendations": recommendations
    }
