import json
import os
from datetime import datetime


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
IOC_DIR = os.path.join(BASE_DIR, "data", "iocs")
CAMPAIGNS_FILE = os.path.join(IOC_DIR, "campaigns.json")


def ensure_storage():
    os.makedirs(IOC_DIR, exist_ok=True)

    if not os.path.exists(CAMPAIGNS_FILE):
        save_campaigns([])


def load_campaigns():
    ensure_storage()

    encodings = ["utf-8", "utf-8-sig", "utf-16"]

    for encoding in encodings:
        try:
            with open(CAMPAIGNS_FILE, "r", encoding=encoding) as file:
                content = file.read().strip()

                if not content:
                    return []

                return json.loads(content)

        except UnicodeDecodeError:
            continue

        except json.JSONDecodeError:
            save_campaigns([])
            return []

    save_campaigns([])
    return []


def save_campaigns(campaigns):
    os.makedirs(IOC_DIR, exist_ok=True)

    with open(CAMPAIGNS_FILE, "w", encoding="utf-8") as file:
        json.dump(campaigns, file, indent=4, ensure_ascii=False)


def register_indicator(indicator_type, value):
    if not value:
        return

    campaigns = load_campaigns()
    now = str(datetime.now())

    for campaign in campaigns:
        if campaign.get("type") == indicator_type and campaign.get("value") == value:
            campaign["count"] = campaign.get("count", 0) + 1
            campaign["last_seen"] = now
            save_campaigns(campaigns)
            return

    campaigns.append({
        "type": indicator_type,
        "value": value,
        "count": 1,
        "first_seen": now,
        "last_seen": now
    })

    save_campaigns(campaigns)


def detect_campaigns(min_count=3):
    campaigns = load_campaigns()
    return [
        campaign for campaign in campaigns
        if campaign.get("count", 0) >= min_count
    ]