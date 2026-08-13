import cv2


LOGIN_WORDS = [
    "login",
    "log in",
    "sign in",
    "signin",
    "continue",
    "verify",
    "next"
]

EMAIL_WORDS = [
    "email",
    "username",
    "phone"
]

PASSWORD_WORDS = [
    "password",
    "passcode"
]


def detect_login_form(ocr_result):
    """
    Detect whether the screenshot is likely
    a credential collection page.
    """

    text = " ".join(
        ocr_result.get("text", [])
    ).lower()

    email_field = any(
        word in text
        for word in EMAIL_WORDS
    )

    password_field = any(
        word in text
        for word in PASSWORD_WORDS
    )

    login_button = any(
        word in text
        for word in LOGIN_WORDS
    )

    login_form = (

        email_field
        or
        password_field
        or
        login_button

    )

    confidence = 0

    if email_field:
        confidence += 30

    if password_field:
        confidence += 40

    if login_button:
        confidence += 30

    confidence = min(confidence, 100)

    reasons = []

    if email_field:
        reasons.append("Email field detected")

    if password_field:
        reasons.append("Password field detected")

    if login_button:
        reasons.append("Login button detected")

    return {

        "loginForm": login_form,

        "emailField": email_field,

        "passwordField": password_field,

        "loginButton": login_button,

        "confidence": confidence,

        "reasons": reasons

    }