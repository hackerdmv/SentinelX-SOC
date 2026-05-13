import re
from urllib.parse import urlparse

SUSPICIOUS_KEYWORDS = [
    "login",
    "verify",
    "update",
    "secure",
    "account",
    "bank",
    "password",
    "confirm"
]

SHORTENERS = [
    "bit.ly",
    "tinyurl.com",
    "goo.gl",
    "t.co"
]

def analyze_url(url):

    result = {
        "url": url,
        "domain": "",
        "https": False,
        "shortener": False,
        "suspicious_keywords": [],
        "risk_score": 0
    }

    try:

        parsed = urlparse(url)

        domain = parsed.netloc.lower()

        result["domain"] = domain

        # HTTPS CHECK
        if parsed.scheme == "https":

            result["https"] = True

        else:

            result["risk_score"] += 20

        # SHORTENER CHECK
        for short in SHORTENERS:

            if short in domain:

                result["shortener"] = True
                result["risk_score"] += 25

        # SUSPICIOUS KEYWORDS
        for keyword in SUSPICIOUS_KEYWORDS:

            if keyword in url.lower():

                result["suspicious_keywords"].append(keyword)
                result["risk_score"] += 10

        # MANY HYPHENS
        if domain.count("-") >= 2:

            result["risk_score"] += 15

        # RANDOM NUMBERS
        if re.search(r'\d{4,}', domain):

            result["risk_score"] += 15

    except Exception as e:

        print(f"[ERRO URL ANALYZER] {e}")

    return result