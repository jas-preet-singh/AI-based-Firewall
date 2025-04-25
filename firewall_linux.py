import psutil
import socket
import requests
import os
import subprocess
import time

API_URL = "http://127.0.0.1:5000"
POLICIES_URL = f"{API_URL}/policies"
LOG_URL = f"{API_URL}/log"

# Fetch policies from server
def fetch_policies():
    try:
        response = requests.get(POLICIES_URL)
        if response.status_code == 200:
            return response.json()
    except requests.RequestException as e:
        print(f"❌ Error fetching policies: {e}")
    return {"blocked_ips": [], "blocked_domains": [], "blocked_protocols": []}

# Resolve domain from IP
def get_domain_from_ip(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return "Unknown"

# Block an IP using iptables (Linux)
def block_ip(ip):
    print(f"🚨 Blocking {ip} using iptables")
    os.system(f"sudo iptables -A OUTPUT -d {ip} -j DROP")

# Block a domain by modifying /etc/hosts
def block_domain(domain):
    print(f"🚨 Blocking domain {domain}")
    with open("/etc/hosts", "a") as hosts_file:
        hosts_file.write(f"\n127.0.0.1 {domain}\n")
    os.system("sudo systemctl restart networking")

# Block a protocol (TCP/UDP) using iptables
def block_protocol(protocol):
    print(f"🚨 Blocking protocol {protocol} using iptables")
    os.system(f"sudo iptables -A OUTPUT -p {protocol.lower()} -j DROP")

# Get active network connections using `ss` (Linux alternative to netstat)
def get_active_connections():
    connections = []
    try:
        result = subprocess.run(["ss", "-tunp"], capture_output=True, text=True)
        lines = result.stdout.split("\n")[1:]

        for line in lines:
            parts = line.split()
            if len(parts) < 7:
                continue

            protocol = parts[0]  # TCP or UDP
            remote = parts[4]
            app_info = parts[-1] if len(parts) > 6 else "Unknown"

            if remote == "*":
                continue

            remote_ip = remote.split(":")[0]
            domain = get_domain_from_ip(remote_ip)

            if app_info.startswith("users:"):
                app = app_info.split('"')[1]  # Extract process name
            else:
                app = "Unknown"

            connections.append((app, remote_ip, domain, protocol))

    except Exception as e:
        print(f"❌ Error fetching connections: {e}")

    return connections

# Enforce firewall policies
def enforce_policies(connections, policies):
    blocked_ips = set(policies.get("blocked_ips", []))
    blocked_domains = set(policies.get("blocked_domains", []))
    blocked_protocols = set(policies.get("blocked_protocols", []))

    for app, ip, domain, protocol in connections:
        decision = "allow"
        reason = "Normal traffic"

        if ip in blocked_ips:
            decision = "block"
            reason = "Blocked IP"
            block_ip(ip)

        if domain in blocked_domains:
            decision = "block"
            reason = "Blocked domain"
            block_domain(domain)

        if protocol.lower() in blocked_protocols:
            decision = "block"
            reason = "Blocked protocol"
            block_protocol(protocol)

        log_data = {
            "ip": ip,
            "app": app,
            "domain": domain,
            "decision": decision,
            "reason": reason
        }

        try:
            requests.post(LOG_URL, json=log_data)
        except requests.RequestException as e:
            print(f"❌ Error sending log: {e}")

        print(f"📡 {app} -> {ip} ({domain}, {protocol}) -> {decision.upper()}")

if __name__ == "__main__":
    print("🔥 Linux Firewall Agent Running...")
    while True:
        policies = fetch_policies()
        active_connections = get_active_connections()
        enforce_policies(active_connections, policies)
        time.sleep(5)
