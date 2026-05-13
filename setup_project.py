import os

# Estrutura de pastas
folders = [

    # Core
    "core",
    "core/analyzer",
    "core/correlation",
    "core/detection",
    "core/blocking",
    "core/intelligence",
    "core/utils",

    # Data
    "data",
    "data/logs",
    "data/cache",
    "data/quarantine",
    "data/iocs",
    "data/reports",

    # Interface
    "ui",
    "ui/dashboard",
    "ui/assets",
    "ui/components",

    # Modules
    "modules",
    "modules/email_analyzer",
    "modules/url_scanner",
    "modules/phishing_detector",
    "modules/threat_hunter",
    "modules/campaign_detector",
    "modules/firewall_control",

    # AI
    "ai",
    "ai/models",
    "ai/training",
    "ai/datasets",

    # Config
    "config",

    # Tests
    "tests"
]

# Arquivos principais
files = {

    "main.py": "",

    "requirements.txt": """psutil
requests
dnspython
scapy
email-validator
beautifulsoup4
tldextract
fuzzywuzzy
python-Levenshtein
rich
colorama
flask
""",

    "README.md": "# SentinelX SOC\n",

    "config/settings.json": "{}",
    "config/blacklist.json": "[]",
    "config/whitelist.json": "[]",

    "core/__init__.py": "",
    "modules/__init__.py": "",
    "ai/__init__.py": ""
}

# Criar pastas
for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"[+] Pasta criada: {folder}")

# Criar arquivos
for file, content in files.items():
    with open(file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[+] Arquivo criado: {file}")

print("\n[✔] Estrutura SentinelX SOC criada com sucesso.")