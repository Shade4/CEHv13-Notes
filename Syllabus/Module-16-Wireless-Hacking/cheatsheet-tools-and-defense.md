# Cheat Sheet — Tool Matrix & Defensive Checklist

## Part 1 — Tool-Purpose Matrix

| Tool | Category | Purpose | Source |
|---|---|---|---|
| **airmon-ng** | Aircrack-ng suite | Switch NIC between managed ↔ monitor mode | aircrack-ng.org |
| **airodump-ng** | Aircrack-ng suite | Capture raw 802.11 frames, collect WEP IVs, list APs/clients | aircrack-ng.org |
| **aireplay-ng** | Aircrack-ng suite | Injection: deauth, fake-auth, ARP replay, handshake capture | aircrack-ng.org |
| **aircrack-ng** | Aircrack-ng suite | De facto WEP / WPA-PSK / WPA2-PSK cracking tool | aircrack-ng.org |
| **airbase-ng** | Aircrack-ng suite | Captures WPA/WPA2 handshake; can act as ad-hoc AP | aircrack-ng.org |
| **airdecap-ng** | Aircrack-ng suite | Decrypts WEP/WPA/WPA2 captures; strips wireless headers | aircrack-ng.org |
| **airdrop-ng** | Aircrack-ng suite | Targeted, rule-based de-authentication | aircrack-ng.org |
| **airolib-ng** | Aircrack-ng suite | Stores/manages ESSID + password lists for WPA/WPA2 cracking | aircrack-ng.org |
| **airgraph-ng** | Aircrack-ng suite | Client–AP relationship / probe graphs from airodump files | aircrack-ng.org |
| **airtun-ng** | Aircrack-ng suite | Virtual tunnel interface to monitor/inject encrypted traffic | aircrack-ng.org |
| **Wash** | WPS discovery | Identify WPS-enabled APs and lock state | (Reaver package) |
| **Reaver** | WPS cracking | Brute-forces WPS PIN to recover WPA/WPA2 passphrase | github.com |
| **hashcat** | Password cracking | GPU-accelerated cracking; mode 22000 for WPA/WPA2/WPA3 | hashcat.net |
| **hcxpcapngtool** | Format conversion | Converts `.cap`/`.pcapng` to hashcat's `.hccapx`/`hc22000` format | github.com (hcxtools) |
| **Fern Wifi Cracker** | Password cracking | GUI WPA/WPS brute-forcing tool (Python/Qt) | github.com |
| **cowpatty** | Password cracking | PSK cracking from captured handshakes | — |
| **John the Ripper / L0phtCrack / THC-Hydra** | Password cracking | Domain login / NetBIOS hash cracking | — |
| **mdk3 / mdk4** | DoS / SSID reveal | Beacon flood, EAPOL logoff, hidden-SSID brute-force | — |
| **Ettercap** | MITM / ARP poisoning | Sniffing, ARP poisoning, MITM attack toolkit | ettercap-project.org |
| **bettercap** | MITM | Modern modular MITM framework (successor-class tool to Ettercap) | github.com |
| **MANA Toolkit** | Rogue AP | Creates rogue APs, defeats HTTPS/HSTS, performs MITM | github.com (sensepost) |
| **hostapd-wpe** | Rogue AP / KARMA | Modified hostapd for credential-harvesting rogue APs | github.com |
| **Technitium MAC Address Changer** | MAC spoofing | GUI MAC address spoofing on Windows | technitium.com |
| **Wireshark / tshark** | Traffic analysis | Full protocol analysis, 802.11 Radiotap inspection | wireshark.org |
| **CommView for Wi-Fi** | Traffic analysis | 802.11 a/b/g/n monitor + WPA-PSK decrypt | tamos.com |
| **Kismet** | Traffic analysis / discovery | Wireless IDS/sniffer/discovery | kismetwireless.net |
| **RF Explorer** | Spectrum analysis | Handheld/PC RF spectrum analyzer | rfexplorer.com |
| **inSSIDer / Sparrow-wifi** | Wi-Fi discovery | Signal-strength mapping, channel graphing | metageek.com / github.com |
| **iCopy-X / RFIDler / Flipper Zero** | RFID cloning | Clone RFID/NFC access badges | icopyx.com / github.com / flipperzero.one |
| **Cisco Adaptive Wireless IPS / WatchGuard Wi-Fi Cloud WIPS** | Defense | Enterprise WIPS — detect/block rogue APs & attacks | cisco.com / watchguard.com |

## Part 2 — One-Page Defensive Checklist

Print this, or paste it into your own hardening runbook. Every line traces back to `10-wireless-countermeasures-and-wips.md`.

### Encryption & Authentication
- [ ] WPA3 enabled everywhere it's supported; WPA2-AES (never TKIP/WEP) as the fallback minimum.
- [ ] WPA3-SAE enabled for all compatible devices; **transition mode disabled** once all clients support WPA3.
- [ ] Wi-Fi password ≥ 12–16 characters, mixed case + digits + symbols.
- [ ] 802.1X + RADIUS for enterprise networks — no shared PSK across every employee device.
- [ ] Multi-factor authentication layered on top where possible.

### Router / AP Configuration
- [ ] Default SSID changed; SSID doesn't reveal vendor, company name, or an easy-to-guess string.
- [ ] SSID broadcast disabled/cloaked (understanding this is *defense in depth*, not a real barrier on its own).
- [ ] **WPS disabled entirely** (not just PIN-lockout — Reaver-class attacks bypass lockouts).
- [ ] TKIP disabled; AES/CCMP-only.
- [ ] Default router admin password changed; remote management disabled.
- [ ] Firmware kept current — subscribe to vendor security advisories.
- [ ] Guest network segmented (separate SSID/VLAN) from the internal network.
- [ ] DHCP disabled / static IPs used where feasible; SNMP disabled or least-privilege.
- [ ] Unused ports/services closed on the AP/router.
- [ ] Transmission power tuned down to the minimum needed for required coverage.

### Monitoring & Detection
- [ ] WIPS or equivalent RF-monitoring deployed (Cisco Adaptive WIPS, WatchGuard, Arista, etc.).
- [ ] Rogue-AP detection active: RF scanning, AP-to-AP scanning, wired-side inputs, MAC allow-listing.
- [ ] Authorized-AP inventory maintained and diffed regularly against RF scans.
- [ ] Client devices patched and running up-to-date Wi-Fi drivers (closes KRACK and similar implementation flaws).

### Network Architecture
- [ ] VPN required for sensitive traffic over any wireless segment.
- [ ] IPsec / SSL/TLS enforced for data in transit.
- [ ] Network segmentation (VLANs) isolating critical systems from general wireless access.
- [ ] DNS hardened: DoH/DoT/DNSCrypt, trusted resolvers only — the direct countermeasure to aLTEr-style DNS hijacking.
- [ ] 802.11r (fast BSS transition) disabled unless roaming is required and patched against KRACK variants.

### User-Facing Hygiene
- [ ] Users trained not to auto-connect to open/unknown SSIDs (defeats Evil Twin / Honeypot AP / KARMA-based attacks).
- [ ] HTTPS-only browsing enforced/encouraged (HTTPS Everywhere or browser-native equivalent).
- [ ] Public Wi-Fi discouraged for sensitive work; VPN mandated when it can't be avoided.
- [ ] IoT devices audited and kept off insecure/legacy Wi-Fi networks.

---
**See also:** [`cheatsheet-commands.md`](cheatsheet-commands.md) for the full command reference, and [`README.md`](README.md) for the repository map.
