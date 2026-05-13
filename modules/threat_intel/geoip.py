import requests


def lookup_ip_geo(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)

        if response.status_code != 200:
            return {"enabled": False, "error": "Falha na API"}

        data = response.json()

        if data.get("status") != "success":
            return {"enabled": False, "error": "IP inválido"}

        return {
            "enabled": True,
            "ip": ip,
            "country": data.get("country"),
            "region": data.get("regionName"),
            "city": data.get("city"),
            "lat": data.get("lat"),
            "lon": data.get("lon"),
            "isp": data.get("isp"),
            "org": data.get("org"),
            "asn": data.get("as"),
            "error": None
        }

    except Exception as e:
        return {
            "enabled": False,
            "error": str(e)
        }