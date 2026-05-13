import os
import requests


API_KEY = os.getenv("SHODAN_API_KEY", "").strip()


def lookup_ip_shodan(ip):
    if not ip:
        return {
            "enabled": False,
            "error": "IP não informado.",
            "ip": None,
            "org": None,
            "isp": None,
            "ports": [],
            "services": []
        }

    if not API_KEY:
        return {
            "enabled": False,
            "error": "Shodan API Key não configurada.",
            "ip": ip,
            "org": None,
            "isp": None,
            "ports": [],
            "services": []
        }

    try:
        url = f"https://api.shodan.io/shodan/host/{ip}?key={API_KEY}"
        response = requests.get(url, timeout=15)

        if response.status_code != 200:
            return {
                "enabled": True,
                "error": f"Erro Shodan HTTP {response.status_code}",
                "ip": ip,
                "org": None,
                "isp": None,
                "ports": [],
                "services": []
            }

        data = response.json()

        services = []
        for item in data.get("data", [])[:8]:
            services.append({
                "port": item.get("port"),
                "transport": item.get("transport"),
                "product": item.get("product"),
                "version": item.get("version"),
                "hostnames": item.get("hostnames", [])
            })

        return {
            "enabled": True,
            "error": None,
            "ip": ip,
            "org": data.get("org"),
            "isp": data.get("isp"),
            "ports": data.get("ports", []),
            "services": services
        }

    except Exception as e:
        return {
            "enabled": True,
            "error": str(e),
            "ip": ip,
            "org": None,
            "isp": None,
            "ports": [],
            "services": []
        }