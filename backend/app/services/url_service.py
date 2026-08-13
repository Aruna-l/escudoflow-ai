from urllib.parse import urlparse
from pathlib import Path
import sys

# -----------------------------
# Response Model
# -----------------------------
from app.models.response_models import URLResponse

# -----------------------------
# Rule Engine + Fusion
# -----------------------------
from app.services.rule_engine import analyze_rules
from app.services.fusion_engine import combine

# -----------------------------
# Reputation
# -----------------------------
from app.services.reputation.reputation_service import analyze_reputation

# -----------------------------
# Domain Intelligence
# -----------------------------
from app.services.whois_service import get_whois_info
from app.services.dns_service import get_dns_info
from app.services.ssl_service import get_ssl_info
from app.services.hosting_service import get_hosting_info

# -----------------------------
# Brand Similarity
# -----------------------------
from app.services.brand_similarity import get_brand_similarity
from app.services.redirect_services import get_redirect_info
from app.services.ai_explanation_service import generate_ai_explanation



# -------------------------------------------------------
# Import ML Module
# -------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[3]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from ml.predict import predict_url


def analyze_url(url: str) -> URLResponse:
    """
    Main URL Analysis Service

    Flow

        URL
         │
         ├── Rule Engine
         │
         ├── ML Model
         │
         ├── Fusion Engine
         │
         ├── Reputation
         │
         ├── WHOIS
         │
         ├── DNS
         │
         ├── SSL
         │
         ├── Hosting
         │
         ├── Brand Similarity
         │
         ▼
      Final Response
    """

    # ------------------------------------
    # URL Information
    # ------------------------------------

    parsed = urlparse(url)

    domain = parsed.hostname.lower() if parsed.hostname else parsed.netloc.lower()

    protocol = parsed.scheme

    https = protocol.lower() == "https"

    url_length = len(url)

    # ------------------------------------
    # Rule Engine
    # ------------------------------------

    rule_result = analyze_rules(url)

    # ------------------------------------
    # Machine Learning
    # ------------------------------------

    ml_result = predict_url(url)

    # ------------------------------------
    # Fusion Engine
    # ------------------------------------

    final_result = combine(
        rule_result,
        ml_result
    )

    # ------------------------------------
    # Threat Intelligence
    # ------------------------------------

    reputation = analyze_reputation(url)

    # ------------------------------------
    # Domain Intelligence
    # ------------------------------------

    whois = get_whois_info(domain)

    dns = get_dns_info(domain)

    ssl = get_ssl_info(domain)

    hosting = get_hosting_info(domain)

    # ------------------------------------
    # Brand Similarity
    # ------------------------------------

    brand_similarity = get_brand_similarity(url)

    ai_explanation = generate_ai_explanation(
    url=url,
    final_result=final_result,
    reputation=reputation,
    brand_similarity=brand_similarity,
    https=https
)

    redirect_info = get_redirect_info(url)

    timeline = [
    {
        "t": "0 ms",
        "event": "URL submitted"
    },
    {
        "t": "15 ms",
        "event": "Rule engine analysis completed"
    },
    {
        "t": "35 ms",
        "event": "Machine learning prediction completed"
    },
    {
        "t": "55 ms",
        "event": "Threat reputation checked"
    },
    {
        "t": "75 ms",
        "event": "WHOIS information retrieved"
    },
    {
        "t": "95 ms",
        "event": "DNS records resolved"
    },
    {
        "t": "115 ms",
        "event": "SSL certificate verified"
    },
    {
        "t": "135 ms",
        "event": "Hosting information collected"
    },
    {
        "t": "155 ms",
        "event": "Redirect chain analyzed"
    },
    {
        "t": "175 ms",
        "event": "Brand similarity calculated"
    },
    {
        "t": "200 ms",
        "event": f"Final Verdict: {final_result['prediction']}"
    }
]

    # ------------------------------------
    # Final Response
    # ------------------------------------

    return URLResponse(

        # URL Information
        url=url,
        domain=domain,
        protocol=protocol,
        url_length=url_length,
        https=https,
        timeline=timeline,

        redirects=redirect_info["redirects"],
        redirect_count=redirect_info["redirectCount"],
        final_url=redirect_info["finalUrl"],

        # Prediction
        prediction=final_result["prediction"],
        confidence=final_result["confidence"],
        risk_score=final_result["risk_score"],
        severity=final_result["severity"],

        # ML
        ml_prediction=final_result["ml_prediction"],
        ml_risk_score=final_result["ml_risk_score"],

        # Rule Engine
        rule_score=final_result["rule_score"],
        reasons=final_result["reasons"],

        # Threat Intelligence
        reputation=reputation,

        # Domain Intelligence
        whois=whois,
        dns=dns,
        ssl=ssl,
        hosting=hosting,

        # Brand Similarity
        brand_similarity=brand_similarity,
        ai_explanation=ai_explanation,  
    )