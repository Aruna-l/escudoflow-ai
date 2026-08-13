import re


SUSPICIOUS_EXTENSIONS = {
    ".exe": 100,
    ".dll": 100,
    ".bat": 95,
    ".cmd": 95,
    ".scr": 95,
    ".js": 90,
    ".vbs": 90,
    ".ps1": 90,
    ".jar": 85,
    ".zip": 70,
    ".rar": 70,
    ".7z": 70,
    ".iso": 80,
    ".docm": 95,
    ".xlsm": 95,
    ".pptm": 95,
    ".doc": 50,
    ".xls": 50,
    ".ppt": 50,
    ".pdf": 20,
}


def analyze_attachments(email_body: str):
    """
    Detect filenames mentioned inside an email body
    and assign a simple risk score.
    """

    pattern = r"\b[\w\-]+\.(?:exe|dll|bat|cmd|scr|js|vbs|ps1|jar|zip|rar|7z|iso|docm|xlsm|pptm|doc|xls|ppt|pdf)\b"

    files = re.findall(pattern, email_body, flags=re.IGNORECASE)

    results = []

    for file in files:

        extension = "." + file.split(".")[-1].lower()

        risk = SUSPICIOUS_EXTENSIONS.get(extension, 20)

        results.append(
            {
                "filename": file,
                "risk_score": risk
            }
        )

    return results