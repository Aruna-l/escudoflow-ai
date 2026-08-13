from email.utils import parseaddr


def analyze_reply_to(email_data):

    sender = parseaddr(email_data["from"])[1].lower()

    reply = parseaddr(email_data["reply_to"])[1].lower()

    if not reply:

        return {

            "match": True,

            "reason": "No Reply-To address"

        }

    sender_domain = sender.split("@")[-1]

    reply_domain = reply.split("@")[-1]

    if sender_domain == reply_domain:

        return {

            "match": True,

            "reason": "Reply-To matches sender"

        }

    return {

        "match": False,

        "reason": "Reply-To domain mismatch"

    }