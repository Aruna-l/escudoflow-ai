import requests


def get_redirect_info(url: str):
    """
    Analyze the redirect chain of a URL.
    """

    try:

        response = requests.get(
            url,
            allow_redirects=True,
            timeout=10,
            headers={
                "User-Agent": "EscudoFlowAI/1.0"
            }
        )

        redirects = []

        for r in response.history:
            redirects.append(r.url)

        redirects.append(response.url)

        return {

            "redirectCount": len(response.history),

            "redirects": redirects,

            "finalUrl": response.url

        }

    except Exception as e:

        print(f"[REDIRECT ERROR] {e}")

        return {

            "redirectCount": 0,

            "redirects": [],

            "finalUrl": url

        }