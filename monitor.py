import time
import json
import os
from datetime import datetime

from modules.url_scanner.url_analyzer import analyze_url
from modules.email_analyzer.header_analyzer import analyze_header
from modules.campaign_detector.campaign_detector import register_indicator, detect_campaigns
from modules.threat_intel.virustotal import check_url_virustotal


MONITOR_FILE = "data/monitor/targets.json"
ALERT_FILE = "data/monitor/alerts.json"


def ensure_files():
    os.makedirs("data/monitor", exist_ok=True)

    if not os.path.exists(MONITOR_FILE):
        with open(MONITOR_FILE, "w", encoding="utf-8") as file:
            json.dump({
                "urls": [],
                "headers": []
            }, file, indent=4, ensure_ascii=False)

    if not os.path.exists(ALERT_FILE):
        with open(ALERT_FILE, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4, ensure_ascii=False)


def load_targets():
    ensure_files()

    with open(MONITOR_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def load_alerts():
    ensure_files()

    with open(ALERT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_alert(alert):
    alerts = load_alerts()
    alerts.append(alert)

    with open(ALERT_FILE, "w", encoding="utf-8") as file:
        json.dump(alerts, file, indent=4, ensure_ascii=False)


def get_severity(score):
    if score >= 80:
        return "CRÍTICO"
    if score >= 60:
        return "ALTO"
    if score >= 40:
        return "MÉDIO"
    return "BAIXO"


def monitor_once():
    targets = load_targets()

    print("\n[+] SentinelX Monitor executando ciclo...\n")

    for url in targets.get("urls", []):
        url_result = analyze_url(url)
        vt_result = check_url_virustotal(url)

        url_result["virustotal"] = vt_result

        vt_score = 0
        if vt_result.get("malicious", 0) > 0:
            vt_score += 80
        if vt_result.get("suspicious", 0) > 0:
            vt_score += 40

        score = max(url_result.get("risk_score", 0), vt_score)
        severity = get_severity(score)

        domain = url_result.get("domain")

        if score >= 70 and domain:
            register_indicator("domain", domain)

        alert = {
            "timestamp": str(datetime.now()),
            "type": "url",
            "target": url,
            "score": score,
            "severity": severity,
            "result": url_result
        }

        save_alert(alert)

        print(f"[URL] {url} | Score: {score} | Severidade: {severity}")

    for header in targets.get("headers", []):
        email_result = analyze_header(header)

        score = email_result.get("risk_score", 0)
        severity = get_severity(score)
        ip = email_result.get("origin_ip")

        if score >= 70 and ip:
            register_indicator("ip", ip)

        alert = {
            "timestamp": str(datetime.now()),
            "type": "email_header",
            "target": ip,
            "score": score,
            "severity": severity,
            "result": email_result
        }

        save_alert(alert)

        print(f"[EMAIL] IP: {ip} | Score: {score} | Severidade: {severity}")

    campaigns = detect_campaigns()

    if campaigns:
        print("\n[!] Campanhas detectadas:")
        for campaign in campaigns:
            print(f"- {campaign['type']} -> {campaign['value']} ({campaign['count']}x)")


def main():
    ensure_files()

    print("================================")
    print(" SentinelX SOC - MONITOR MODE")
    print("================================")

    while True:
        monitor_once()
        print("\n[+] Próximo ciclo em 60 segundos...\n")
        time.sleep(60)


if __name__ == "__main__":
    main()