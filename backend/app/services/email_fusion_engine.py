def combine_email_results(

    rule_result,

    auth_result,

    reply_result,

    url_results

):

    # -------------------------
    # Base Score
    # -------------------------

    score = rule_result["score"]

    score += auth_result["score"]

    if not reply_result["match"]:
        score += 20

    if url_results:

        highest = max(u["risk_score"] for u in url_results)

        score = max(score, highest)

    score = min(score, 100)

    # -------------------------
    # Verdict
    # -------------------------

    if score >= 80:

        verdict = "Critical"

    elif score >= 60:

        verdict = "High"

    elif score >= 40:

        verdict = "Medium"

    else:

        verdict = "Low"

    confidence = min(score + 10, 100)

    # -------------------------
    # Dashboard Metrics
    # -------------------------

    phishing_probability = round(score / 100, 2)

    urgency = 1.0 if any(
        "urgent" in r.lower() or "immediately" in r.lower()
        for r in rule_result["reasons"]
    ) else 0.2

    impersonation = 0.9 if not reply_result["match"] else 0.1

    bec = (
        impersonation > 0.5
        and urgency > 0.5
    )

    spam_score = round(score / 25, 1)

    reputation = (
        "New"
        if score >= 60
        else "Trusted"
    )

    return {

        "risk_score": score,

        "confidence": confidence,

        "verdict": verdict,

        "phishingProbability": phishing_probability,

        "bec": bec,

        "spamScore": spam_score,

        "urgency": urgency,

        "impersonation": impersonation,

        "reputation": reputation

    }