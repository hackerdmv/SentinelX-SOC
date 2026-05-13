import os
import sys
import json
from datetime import datetime
from flask import Flask, render_template, request, send_file

from modules.email_analyzer.header_analyzer import analyze_header
from modules.url_scanner.url_analyzer import analyze_url
from modules.campaign_detector.campaign_detector import register_indicator, detect_campaigns
from modules.threat_intel.virustotal import check_url_virustotal
from modules.threat_intel.geoip import lookup_ip_geo
from modules.threat_intel.shodan_intel import lookup_ip_shodan
from core.blocking.firewall_blocker import block_ip, block_domain


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def reports_dir():
    path = resource_path("data/reports")
    os.makedirs(path, exist_ok=True)
    return path


def get_map_data():
    points = []

    try:
        for file in os.listdir(reports_dir()):
            if file.endswith(".json"):
                with open(os.path.join(reports_dir(), file), "r", encoding="utf-8") as f:
                    data = json.load(f)
                    geo = data.get("geoip_result", {})

                    if geo and geo.get("lat") and geo.get("lon"):
                        points.append({
                            "lat": geo.get("lat"),
                            "lon": geo.get("lon"),
                            "ip": geo.get("ip"),
                            "country": geo.get("country")
                        })
    except:
        pass

    return points


template_dir = resource_path("ui/dashboard/templates")
app = Flask(__name__, template_folder=template_dir)


@app.route("/", methods=["GET", "POST"])
def dashboard():
    result = None
    campaigns = []
    status = "Dashboard carregado com sucesso."
    error = None

    if request.method == "POST":
        url = request.form.get("url", "")
        header = request.form.get("header", "")

        email_result = {}
        url_result = {}
        geoip_result = {}
        shodan_result = {}

        try:
            if url:
                url_result = analyze_url(url)

                vt = check_url_virustotal(url)
                url_result["virustotal"] = vt

            if header:
                email_result = analyze_header(header)
                ip = email_result.get("origin_ip")

                if ip:
                    geoip_result = lookup_ip_geo(ip)
                    shodan_result = lookup_ip_shodan(ip)

                    email_result["geoip"] = geoip_result
                    email_result["shodan"] = shodan_result

            result = {
                "email": email_result,
                "url": url_result,
                "geoip": geoip_result,
                "shodan": shodan_result
            }

            report = {
                "timestamp": str(datetime.now()),
                "url_result": url_result,
                "email_result": email_result,
                "geoip_result": geoip_result,
                "shodan": shodan_result
            }

            name = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

            with open(os.path.join(reports_dir(), name), "w", encoding="utf-8") as f:
                json.dump(report, f, indent=4)

            status = "Análise concluída com sucesso."

        except Exception as e:
            error = str(e)

    return render_template(
        "index.html",
        result=result,
        campaigns=campaigns,
        status=status,
        error=error,
        map_data=get_map_data()
    )


if __name__ == "__main__":
    app.run(port=5050)