from pathlib import Path

import joblib
import pandas as pd

from ml.feature_extraction import extract_features

# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"

# --------------------------------------------------
# Load ML Assets
# --------------------------------------------------

model = joblib.load(MODEL_DIR / "url_xgboost_model.pkl")
encoder = joblib.load(MODEL_DIR / "url_tld_encoder.pkl")
feature_names = joblib.load(MODEL_DIR / "url_feature_names.pkl")


def predict_url(url: str):
    # Extract features
    features = extract_features(url)

    # Encode TLD
    try:
        features["TLD"] = encoder.transform([features["TLD"]])[0]
    except ValueError:
        features["TLD"] = -1

    # Convert to DataFrame
    df = pd.DataFrame([features])

    # Match training feature order
    df = df[feature_names]

    # Prediction
    prediction = model.predict(df)[0]

    # Probability
    probability = model.predict_proba(df)[0]

    return {
        "prediction": "Phishing" if prediction == 1 else "Legitimate",
        "confidence": float(round(max(probability) * 100, 2)),
        "risk_score": float(round(probability[1] * 100, 2)),
    }


if __name__ == "__main__":
    url = "https://paypal-login-security.xyz/login?id=123"

    result = predict_url(url)

    print(result)