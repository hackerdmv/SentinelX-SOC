import re

def analyze_header(raw_header):
    result = {
        "return_path": None,
        "reply_to": None,
        "spf": "UNKNOWN",
        "dkim": "MISSING",
        "dmarc": "UNKNOWN",
        "origin_ip": None,
        "risk_score": 0
    }

    try:
        # 🔍 RETURN PATH
        match = re.search(r"Return-Path:\s*<([^>]+)>", raw_header, re.IGNORECASE)
        if match:
            result["return_path"] = match.group(1)

        # 🔍 REPLY TO
        match = re.search(r"Reply-To:\s*([^\n]+)", raw_header, re.IGNORECASE)
        if match:
            result["reply_to"] = match.group(1).strip()

        # 🔍 SPF
        if "spf=fail" in raw_header.lower() or "received-spf: fail" in raw_header.lower():
            result["spf"] = "FAIL"
            result["risk_score"] += 20
        elif "spf=pass" in raw_header.lower():
            result["spf"] = "PASS"

        # 🔍 DKIM
        if "dkim=fail" in raw_header.lower():
            result["dkim"] = "FAIL"
            result["risk_score"] += 20
        elif "dkim=pass" in raw_header.lower():
            result["dkim"] = "PASS"

        # 🔍 DMARC
        if "dmarc=fail" in raw_header.lower():
            result["dmarc"] = "FAIL"
            result["risk_score"] += 20
        elif "dmarc=pass" in raw_header.lower():
            result["dmarc"] = "PASS"

        # 🔍 IP DE ORIGEM (pega o primeiro válido)
        ips = re.findall(r"\b\d{1,3}(?:\.\d{1,3}){3}\b", raw_header)
        if ips:
            result["origin_ip"] = ips[0]

        # 🔥 AJUSTE DE RISCO
        if result["origin_ip"]:
            result["risk_score"] += 10

        if result["reply_to"] and result["return_path"]:
            if result["reply_to"] not in result["return_path"]:
                result["risk_score"] += 20

    except Exception as e:
        print("Erro ao analisar header:", e)

    return result