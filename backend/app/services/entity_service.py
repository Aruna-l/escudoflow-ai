import re

def extract_entities(email_data):

    text = email_data["subject"] + " " + email_data["body"]

    amount = re.findall(r"\$[\d,]+", text)

    bank = re.findall(r"\b[A-Z][a-z]+ Bank\b", text)

    person = re.findall(
        r"[-–]\s*([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)",
        text
    )

    deadline = re.findall(
        r"\b(today|tomorrow|immediately|end of day|within 24 hours)\b",
        text,
        re.IGNORECASE
    )

    return {
        "person": list(dict.fromkeys(person)),
        "amount": list(dict.fromkeys(amount)),
        "bank": list(dict.fromkeys(bank)),
        "deadline": list(dict.fromkeys(deadline))
    }