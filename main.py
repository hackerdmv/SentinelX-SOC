from modules.email_analyzer.header_analyzer import analyze_header
from modules.url_scanner.url_analyzer import analyze_url

from modules.campaign_detector.campaign_detector import (
    register_indicator,
    detect_campaigns
)

from core.blocking.firewall_blocker import (
    block_ip,
    block_domain
)


def print_section(title):
    print(f"\n====== {title} ======\n")


def print_result(result):
    for key, value in result.items():
        print(f"{key}: {value}")


def main():
    # =========================================
    # EMAIL HEADER TEST
    # =========================================

    sample_header = """Return-Path: <fake@rhtfempregos.com>
Reply-To: suporte@gmail.com
Received-SPF: fail
Authentication-Results: dmarc=fail
DKIM-Signature: fake-signature
Received: from attacker.com (185.222.81.10)

"""

    header_result = analyze_header(sample_header)

    print_section("EMAIL ANALYZER")
    print_result(header_result)

    # =========================================
    # URL TEST
    # =========================================

    url = "http://secure-login-bank-update1234.com"

    url_result = analyze_url(url)

    print_section("URL ANALYZER")
    print_result(url_result)

    # =========================================
    # REGISTER IOCS
    # =========================================

    print_section("REGISTERING IOCS")

    domain = url_result.get("domain")
    origin_ip = header_result.get("origin_ip")

    if domain:
        register_indicator("domain", domain)
        register_indicator("domain", domain)
        register_indicator("domain", domain)

    if origin_ip:
        register_indicator("ip", origin_ip)

    print("[+] IOCS registrados com sucesso.")

    # =========================================
    # DETECT CAMPAIGNS
    # =========================================

    campaigns = detect_campaigns()

    print_section("CAMPAIGN DETECTOR")

    if campaigns:
        for campaign in campaigns:
            print(f"""
[ALERTA]
Tipo: {campaign.get('type')}
Valor: {campaign.get('value')}
Ocorrências: {campaign.get('count')}
Primeira vez: {campaign.get('first_seen')}
Última vez: {campaign.get('last_seen')}
""")
    else:
        print("Nenhuma campanha suspeita detectada.")

    # =========================================
    # ACTIVE DEFENSE
    # =========================================

    print_section("ACTIVE DEFENSE")

    risk_score = url_result.get("risk_score", 0)

    if domain and risk_score >= 70:
        block_domain(domain)

    if origin_ip:
        block_ip(origin_ip)

    print("\n[✔] SentinelX SOC finalizou análise.\n")


if __name__ == "__main__":
    main()