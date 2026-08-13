import re
from email import message_from_string
from email.policy import default
from bs4 import BeautifulSoup
import unicodedata

def parse_email(raw_email: str):
    """
    Parse raw email text or .eml content.
    Supports both uploaded .eml files and pasted emails.
    """

    msg = message_from_string(raw_email, policy=default)

    # -------------------------
    # Headers
    # -------------------------

    sender = msg.get("From", "")
    reply_to = msg.get("Reply-To", "")
    subject = msg.get("Subject", "")

    # Fallback for pasted emails
    if not sender:
        match = re.search(r"^From:\s*(.+)$", raw_email, re.MULTILINE | re.IGNORECASE)
        if match:
            sender = match.group(1).strip()

    if not reply_to:
        match = re.search(r"^Reply-To:\s*(.+)$", raw_email, re.MULTILINE | re.IGNORECASE)
        if match:
            reply_to = match.group(1).strip()

    if not subject:
        match = re.search(r"^Subject:\s*(.+)$", raw_email, re.MULTILINE | re.IGNORECASE)
        if match:
            subject = match.group(1).strip()

    # -------------------------
    # Body
    # -------------------------

    body = ""

    if msg.is_multipart():

    # First preference: text/plain
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                try:
                    body += part.get_content()
                except Exception:
                    pass

    # If no plain text found, use HTML
        if not body.strip():
            for part in msg.walk():
                if part.get_content_type() == "text/html":
                    try:
                        html = part.get_content()

                        soup = BeautifulSoup(html, "html.parser")

# Remove style and script tags
                        for tag in soup(["style", "script", "head", "title"]):
                            tag.decompose()

                        body = soup.get_text(separator="\n")

                        body = re.sub(r"\n+", "\n", body)
                        body = body.strip()
                    except Exception:
                        pass

    else:
        try:
            if msg.get_content_type() == "text/html":

                html = msg.get_content()

                soup = BeautifulSoup(html, "html.parser")

                for tag in soup(["style", "script", "head", "title"]):
                    tag.decompose()

                body = soup.get_text(separator="\n")

                body = re.sub(r"\n+", "\n", body)
                body = body.strip()

        except Exception:
            body = raw_email

    # Remove headers from pasted email body
    # Remove headers from pasted email body
    body = re.sub(
        r"^(From|To|Reply-To|Cc|Bcc|Subject):.*$",
        "",
        body,
        flags=re.MULTILINE | re.IGNORECASE,
    )

    # Normalize Unicode
    body = unicodedata.normalize("NFKC", body)

    # Remove invisible Unicode characters
    body = re.sub(
        r"[\u200B-\u200F\u202A-\u202E\u2060-\u206F\uFEFF]",
        "",
        body,
    )

    # Remove excessive spaces
    body = re.sub(r"[ \t]+", " ", body)

    # Remove repeated blank lines
    body = re.sub(r"\n\s*\n+", "\n\n", body)

    body = body.strip()

    # -------------------------
    # URLs
    # -------------------------

    urls = re.findall(r"https?://[^\s\"'>]+", body)

    # -------------------------
    # Attachments
    # -------------------------

    attachments = []

    # Real .eml attachments
    # First preference: text/html
    for part in msg.walk():
        if part.get_content_type() == "text/html":
            try:
                html = part.get_content()

                soup = BeautifulSoup(html, "html.parser")

                for tag in soup(["style", "script", "head", "title"]):
                    tag.decompose()

                body = soup.get_text(separator="\n")

                body = re.sub(r"\n+", "\n", body)
                body = body.strip()

                break

            except Exception:
                pass

    # If HTML not found, use plain text
    if not body.strip():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                try:
                    body += part.get_content()
                except Exception:
                    pass
    # Attachment names mentioned in body
    attachment_pattern = (
        r"\b[\w\-]+\."
        r"(?:exe|dll|bat|cmd|scr|js|vbs|ps1|jar|zip|rar|7z|iso|docm|xlsm|pptm|doc|xls|ppt|pdf)\b"
    )

    attachments.extend(
        re.findall(
            attachment_pattern,
            body,
            flags=re.IGNORECASE
        )
    )

    attachments = list(set(attachments))

    return {
        "from": sender,
        "reply_to": reply_to,
        "subject": subject,
        "body": body,
        "urls": urls,
        "attachments": attachments,
    }