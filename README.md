# DNS Tunnel
## Allgemeine Informationen
+ Entstanden an: Hochschule Niederrhein
+ Studiengang: Digitale Forensik
+ Semester: Wintersemester 2025/2026 
+ Modul: BDF 302: Rechnernetze und Rechnernetzsicherheit
+ Autor: ezBinary

## Beschreibung
Dieses Projekt implementiert einen DNS-Tunnel-Simulation, bei dem ein Server über DNS-Kommunikation Befehle an einen Client sendet. Der Client führt diese aus (z. B. Datei lesen) und sendet die Ergebnisse zurück über DNS-Anfragen.

## Enthaltene Dateien

| Datei                    | Beschreibung                                                                 |
|--------------------------|------------------------------------------------------------------------------|
| `dns-tunnel-server.py`   | Python-Skript für den DNS-Server. Verteilt Befehle und empfängt Client-Daten |
| `dns-tunnel-client.py`   | Python-Skript für den Client. Fragt Befehle ab und sendet Ergebnisse zurück  |
| `config.yaml`            | Konfigurationsdatei mit IP-Adresse und Port für Server          |
| `data/beispiel.txt`      | Beispiel-Datei, die vom Client gelesen und zurückgesendet werden kann        |
| `anleitung-und-beschreibung.md` | Dokumentation und Anleitung zur Nutzung des Projekts                        |

## Nutzung
1. `config.yaml` anpassen mit IPs und Ports.
2. Server starten: `sudo python3 dns-tunnel-server.py`
3. Client starten: `python3 dns-tunnel-client.py`
4. Beispielhafte Dateiübertragung: Datei in `data/` ablegen, z. B. `beispiel.txt`

## Technische Beschreibung
Das Projekt besteht aus zwei Hauptkomponenten:
+ **dns-tunnel-server.py:** Ein DNS-Server, der Befehle an Clients verteilt und deren Antworten empfängt.
+ **dns-tunnel-client.py:** Ein Client, der regelmäßig DNS-Anfragen stellt, empfangene Befehle ausführt und die Ergebnisse über DNS zurücksendet.

Die Kommunikation erfolgt ausschließlich über DNS TXT-Records, wodurch die Datenübertragung in scheinbar normalen DNS-Anfragen versteckt wird.

### 1. Konfiguration
Beide Skripte laden ihre Einstellungen aus einer gemeinsamen Datei `config.yaml`, die IP-Adresse und Port des Servers enthält. Dies ermöglicht eine flexible Anpassung der Netzwerkparameter.

### 2. Server-Komponente (`dns-tunnel-server.py`)
+ **Socket-Setup:** Der Server bindet sich an die konfigurierte IP und Port (Port 53 für DNS).
+ **Empfang von DNS-Anfragen:** Er wartet auf UDP-Pakete und parst sie mithilfe von `dnslib`.
+ **Befehlsverteilung:**
    + Wenn die Anfrage ein `poll` enthält (z. B. `poll.client1.tunnel`), sendet der Server einen Befehl aus dem `commands` zurück.
+ **Datenempfang**
    + Wenn die Anfrage keine poll enthält, wird sie als Antwort vom Client interpretiert.
    + Der Server extrahiert den hex kodierten Payload aus dem 
    Subdomain-Label und speichert ihn.

### 3. Client-Komponente (`dns-tunnel-client.py`)
+ **Identifikation:** Der Client verwendet eine feste ID (client1) zur Kommunikation.
+ **Polling:**
    + Alle 5 Sekunden sendet der Client eine DNS-Anfrage mit `poll.client1.tunnel`.
    + Der Server antwortet mit einem TXT-Record, der den Befehl enthält.

+ **Antwortübertragung:**
    + Der gelesene Inhalt wird hex-kodiert.
    + In 25 Bytes Chunks wird jeder Teil als Subdomain (`<chunk>.client1.tunnel`) in einer DNS-Anfrage verpackt und an den Server gesendet.
    + Zwischen den Chunks wird eine kurze Pause (`time.sleep(0.5)`) eingelegt, um Überlastung zu vermeiden.

### Datenflussdiagramm (vereinfacht)
1. Client → poll.client1.tunnel → Server
2. Server → TXT: read_file:/pfad → Client
3. Client → hexchunk1.client1.tunnel → Server
3. Client → hexchunk2.client1.tunnel → Server
4. usw.

## Quellen
+ [9.11.2025] https://danger-team.org/the-ultimate-dns-tunneling-guide-from-zero-to-hero/
+ [9.11.2025] https://pypi.org/project/dnslib/
+ [9.11.2025] https://github.com/zrckr/dns-tunnel
+ [8.11.2025] https://johnburns.io/post/dns-exfiltration-in-python/
