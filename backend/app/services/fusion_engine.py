def severity_from_score(score):

    if score <= 20:
        return "Safe"

    elif score <= 40:
        return "Low"

    elif score <= 60:
        return "Medium"

    elif score <= 80:
        return "High"

    else:
        return "Critical"


def prediction_from_score(score):

    if score <= 20:
        return "Legitimate"

    return "Phishing"


def combine(rule_result, ml_result):

    rule_score = rule_result["rule_score"]

    ml_score = ml_result["risk_score"]

    final_score = min(
        100,
        round(rule_score + ml_score)
    )

    severity = severity_from_score(
        final_score
    )

    prediction = prediction_from_score(
        final_score
    )

    return {

        "prediction": prediction,

        "severity": severity,

        "risk_score": final_score,

        "confidence": ml_result["confidence"],

        "ml_prediction": ml_result["prediction"],

        "ml_risk_score": ml_score,

        "rule_score": rule_score,

        "reasons": rule_result["reasons"]

    }