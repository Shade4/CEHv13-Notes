# Tool Matrix — Module 03

| Tool | Primary role | Module relevance |
|---|---|---|
| Nmap | Host/port/service/OS scanning | Central tool |
| Hping3 | Packet crafting/probing | TCP/UDP/ICMP experiments |
| Metasploit | Security framework/scanners | Auxiliary port/service discovery |
| Wireshark | Packet capture/analysis | OS fingerprinting + TCP behavior |
| Unicornscan | Active discovery/fingerprinting | OS discovery |
| Angry IP Scanner | Ping sweep | Host discovery |
| NetScanTools Pro | Network diagnostics | Discovery/monitoring |
| Colasoft Packet Builder | Custom packet creation | Evasion/packet crafting |
| Burp Suite | HTTP proxy/interception | Proxy/intermediary concepts |
| Tor | Anonymizing network | Anonymizer concepts |
| Whonix | Privacy-oriented workstation/gateway design | Anonymizer concepts |
| Tails | Privacy-focused live OS | Anonymizer/privacy concepts |
| ExtraHop | Network visibility/detection | Scan detection |
| Splunk Enterprise Security | SIEM/security analytics | Scan detection |
| Scanlogd | Scan logging/detection | Port-scan detection |
| Vectra | Network threat detection | Defensive visibility |
| IBM Security QRadar XDR | Detection/response | Defensive visibility |
| Cynet 360 AutoXDR | XDR | Defensive visibility |

## Selection guide

```text
Need live hosts?           → Nmap / Angry IP Scanner
Need packet-level proof?   → Wireshark / Hping3
Need service versions?     → Nmap
Need scripted checks?      → Nmap NSE
Need broader pentest?      → Metasploit
Need custom packets?       → Colasoft Packet Builder / Hping3
Need proxying?             → Burp / HTTP proxy / Tor
Need scan detection?       → IDS/IPS / SIEM / NDR tools
```
