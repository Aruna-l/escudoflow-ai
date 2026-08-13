def generate_visual_explanation(

    ocr_result,

    logo_result,

    qr_result,

    brand_similarity,

    metrics,

    risk,

    fusion=None,

    form_result=None,

    clone_result=None

):
    """
    Generate a detailed explainable
    visual phishing report.
    """

    # calculate_visual_risk returns "riskScore", not "overallRisk"
    summary = (
        f"This screenshot has been classified as "
        f"{risk['verdict']} risk with an overall "
        f"score of {risk['riskScore']}%."
    )

    # -----------------------------------
    # Brand Analysis
    # -----------------------------------

    if brand_similarity["matchedBrand"] != "Unknown":

        brand_analysis = (
            f"The screenshot appears to represent "
            f"{brand_similarity['matchedBrand']}."
        )

    else:

        brand_analysis = (
            "No recognizable brand was detected."
        )

    # -----------------------------------
    # Visual Analysis
    # -----------------------------------

    visual_analysis = (

        f"Visual similarity with the official "
        f"reference page is "
        f"{round(metrics['visualSimilarity']*100)}%."

    )

    # -----------------------------------
    # Credential Collection
    # -----------------------------------

    if form_result:

        if form_result["loginForm"]:

            credential_analysis = (
                "A credential collection form was "
                "detected containing login elements."
            )

        else:

            credential_analysis = (
                "No login form was detected."
            )

    else:

        credential_analysis = (
            "Credential analysis unavailable."
        )

    # -----------------------------------
    # Domain Analysis
    # -----------------------------------

    if fusion:

        if fusion["domain"]["match"]:

            domain_analysis = (
                "The supplied URL matches the "
                "official brand domain."
            )

        else:

            domain_analysis = (
                "The supplied URL does not match "
                "the detected brand."
            )

    else:

        domain_analysis = (
            "No URL was available for comparison."
        )

    # -----------------------------------
    # Clone Analysis
    # -----------------------------------

    if clone_result:

        if clone_result["isClone"]:

            clone_analysis = (
                f"The page is highly likely to be a "
                f"clone of {clone_result['matchedBrand']}."
            )

        else:

            clone_analysis = (
                "No evidence of visual cloning detected."
            )

    else:

        clone_analysis = (
            "Clone analysis unavailable."
        )

    # -----------------------------------
    # Evidence
    # -----------------------------------

    evidence = [

        {

            "type": "Logo",

            "result": logo_result["brand"],

            "confidence": logo_result["confidence"]

        },

        {

            "type": "Visual Similarity",

            "result": round(
                metrics["visualSimilarity"] * 100
            )

        },

        {

            "type": "QR Code",

            "result": qr_result["count"]

        },

        {

            "type": "Brand",

            "result": brand_similarity["matchedBrand"]

        }

    ]

    if fusion:

        evidence.append({

            "type": "Domain",

            "result": fusion["domain"]["reason"]

        })

    # -----------------------------------
    # MITRE ATT&CK
    # -----------------------------------

    if form_result and form_result["loginForm"]:

        attack = {

            "technique": "T1566",

            "name": "Phishing"

        }

    else:

        attack = {

            "technique": "Unknown",

            "name": "Unknown"

        }

    # -----------------------------------
    # Recommendations
    # -----------------------------------

    recommendations = [

        "Verify the URL before entering credentials.",

        "Compare the page with the official website.",

        "Avoid scanning unknown QR codes.",

        "Do not submit passwords on suspicious pages.",

        "Report suspicious websites to your security team."

    ]

    return {

        "summary": summary,

        "brandAnalysis": brand_analysis,

        "visualAnalysis": visual_analysis,

        "credentialAnalysis": credential_analysis,

        "domainAnalysis": domain_analysis,

        "cloneAnalysis": clone_analysis,

        "evidence": evidence,

        "mitre": attack,

        "recommendations": recommendations

    }