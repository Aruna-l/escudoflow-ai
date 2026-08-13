from app.services.email_parser import parse_email
from app.services.email_rule_engine import analyze_email_rules
from app.services.email_auth_service import analyze_email_auth
from app.services.replyto_service import analyze_reply_to
from app.services.entity_service import extract_entities
from app.services.email_url_service import analyze_email_urls
from app.services.email_fusion_engine import combine_email_results
from app.services.explanation_service import generate_email_explanation
from app.services.attachment_service import analyze_attachments

def analyze_email(raw_email: str):
    """
    Main Email Intelligence Pipeline

        Email
          │
          ▼
      Email Parser
          │
          ▼
      Rule Engine
          │
          ▼
      Authentication
          │
          ▼
      Reply-To Analysis
          │
          ▼
      Entity Extraction
          │
          ▼
      URL Analysis
          │
          ▼
      Fusion Engine
          │
          ▼
      AI Explanation
          │
          ▼
      Final Response
    """

    # -------------------------
    # Parse Email
    # -------------------------

    email_data = parse_email(raw_email)

    # -------------------------
    # Rule Engine
    # -------------------------

    rule_result = analyze_email_rules(email_data)

    # -------------------------
    # Authentication
    # -------------------------

    auth_result = analyze_email_auth(email_data)

    # -------------------------
    # Reply-To
    # -------------------------

    reply_result = analyze_reply_to(email_data)

    # -------------------------
    # Entity Recognition
    # -------------------------

    entities = extract_entities(email_data)

    # -------------------------
    # URL Intelligence
    # -------------------------

    url_results = analyze_email_urls(email_data["urls"])
    attachment_results = analyze_attachments(email_data["body"])
    # -------------------------
    # Fusion
    # -------------------------

    fusion = combine_email_results(

        rule_result,

        auth_result,

        reply_result,

        url_results

    )

    # -------------------------
    # AI Explanation
    # -------------------------

    explanation = generate_email_explanation(

        rule_result,

        auth_result,

        reply_result,

        entities,

        fusion

    )

    # -------------------------
    # Final Response
    # -------------------------

    return {

    # -------------------------
    # Email Information
    # -------------------------

    "from_email": email_data["from"],

    "reply_to": email_data["reply_to"],

    "subject": email_data["subject"],

    "body": email_data["body"],

    # -------------------------
    # Overall Verdict
    # -------------------------

    "overallRisk": fusion["risk_score"],

    "confidence": fusion["confidence"],

    "verdict": fusion["verdict"],

    # -------------------------
    # Dashboard Metrics
    # -------------------------

    "phishingProbability": fusion["phishingProbability"],

    "bec": fusion["bec"],

    "spamScore": fusion["spamScore"],

    "urgency": fusion["urgency"],

    "impersonation": fusion["impersonation"],

    "reputation": fusion["reputation"],

    # -------------------------
    # Authentication
    # -------------------------

    "authentication": auth_result,

    "headerSummary":
        f"SPF: {auth_result['spf']} | "
        f"DKIM: {auth_result['dkim']} | "
        f"DMARC: {auth_result['dmarc']}",

    # -------------------------
    # Reply-To
    # -------------------------

    "reply_analysis": reply_result,

    "senderReputation": "New Sender",

    # -------------------------
    # Entity Recognition
    # -------------------------

    "entities": entities,

    # -------------------------
    # URLs
    # -------------------------

    "urls": url_results,

    # -------------------------
    # Attachments
    # -------------------------

    "attachments": attachment_results,

    # -------------------------
    # Rule Engine
    # -------------------------

    "rule_engine": rule_result,

    # -------------------------
    # Highlighted Sentences
    # -------------------------

    "highlighted": [

        {

            "text": reason,

            "tag": "Rule Trigger"

        }

        for reason in rule_result["reasons"]

    ],

    # -------------------------
    # AI Explanation
    # -------------------------

    "aiExplanation": explanation

}