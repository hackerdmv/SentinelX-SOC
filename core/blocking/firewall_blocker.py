import subprocess

def block_ip(ip):

    try:

        rule_name = f"SentinelX_Block_{ip}"

        command = f'netsh advfirewall firewall add rule name="{rule_name}" dir=in action=block remoteip={ip}'

        subprocess.run(command, shell=True)

        print(f"[+] IP BLOQUEADO: {ip}")

    except Exception as e:

        print(f"[ERRO BLOCK IP] {e}")

def block_domain(domain):

    try:

        hosts_path = r"C:\Windows\System32\drivers\etc\hosts"

        entry = f"\n127.0.0.1 {domain}\n"

        with open(hosts_path, "a") as hosts:

            hosts.write(entry)

        print(f"[+] DOMÍNIO BLOQUEADO: {domain}")

    except Exception as e:

        print(f"[ERRO BLOCK DOMAIN] {e}")