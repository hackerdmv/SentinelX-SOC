import os
import requests
import time

API_KEY = os.getenv("VT_API_KEY", "").strip()


def check_url_virustotal(url):
    if not API_KEY:
        return {
            "enabled": False,
            "error": "API Key não configurada",
            "malicious": 0,
            "suspicious": 0,
            "harmless": 0,
            "undetected": 0
        }

    try:
        headers = {"x-apikey": API_KEY}

        # Envia URL
        submit = requests.post(
            "https://www.virustotal.com/api/v3/urls",
            headers=headers,
            data={"url": url},
            timeout=15
        )

        if submit.status_code not in [200, 202]:
            return {
                "enabled": True,
                "error": f"Erro envio VT HTTP {submit.status_code}",
                "malicious": 0,
                "suspicious": 0,
                "harmless": 0,
                "undetected": 0
            }

        analysis_id = submit.json()["data"]["id"]

        # 🔥 ESPERA (ESSENCIAL)
        time.sleep(3)

        report = requests.get(
            f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
            headers=headers,
            timeout=15
        )

        if report.status_code != 200:
            return {
                "enabled": True,
                "error": f"Erro consulta VT HTTP {report.status_code}",
                "malicious": 0,
                "suspicious": 0,
                "harmless": 0,
                "undetected": 0
            }

        data = report.json()["data"]["attributes"]
        stats = data.get("stats", {})

        return {
            "enabled": True,
            "error": None,
            "malicious": stats.get("malicious", 0),
            "suspicious": stats.get("suspicious", 0),
            "harmless": stats.get("harmless", 0),
            "undetected": stats.get("undetected", 0)
        }

    except Exception as e:
        return {
            "enabled": True,
            "error": str(e),
            "malicious": 0,
            "suspicious": 0,
            "harmless": 0,
            "undetected": 0
        }