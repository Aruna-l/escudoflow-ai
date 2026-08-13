from app.utils.email_keywords import EMAIL_KEYWORDS


def analyze_email_rules(email_data):

    score = 0

    reasons = []

    text = (
        email_data["subject"] + " " + email_data["body"]
    ).lower()

    for keyword, weight in EMAIL_KEYWORDS.items():

        if keyword.lower() in text:

            score += weight

            reasons.append(f"Contains '{keyword}'")

    # Reply-To mismatch

    sender = email_data["from"].lower()

    reply = email_data["reply_to"].lower()

    if reply and sender and sender != reply:

        score += 15

        reasons.append("Reply-To differs from sender")

    score = min(score, 100)

    return {

        "score": score,

        "reasons": reasons

    }