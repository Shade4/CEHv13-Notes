# 📋 CHEATSHEET — Tools, Ports, and Protocols

Quick-lookup reference tables. See the linked topic file for full explanations.

---

## ICS/SCADA Port Quick Reference

| Port | Protocol |
|---|---|
| 102 | Siemens S7comm |
| 502 | Modbus |
| 1089–1091 | Fieldbus |
| 1911, 4911 | Niagara Fox |
| 1962 | PCWorx |
| 2222 | EtherNet/IP |
| 9600 | Omron FINS |
| 19999 | DNP (legacy) |
| 20000 | DNP3 |
| 20547 | ProConOS |
| 34962–34964 | PROFINET |
| 34980 | EtherCAT |
| 44818 | EtherNet/IP (I/O) |
| 46823, 46824 | HMI (varies by vendor, e.g. Sielco Sistemi Winlog) |
| 47808 | BACnet |

---

## OWASP Top 10 IoT Threats

*Full detail: [02](02-iot-attack-surface-and-vulnerabilities.md#owasp-top-10-iot-threats)*

| # | Threat |
|---|---|
| I1 | Weak, Guessable, or Hardcoded Passwords |
| I2 | Insecure Network Services |
| I3 | Insecure Ecosystem Interfaces |
| I4 | Lack of Secure Update Mechanisms |
| I5 | Use of Insecure or Outdated Components |
| I6 | Insufficient Privacy Protection |
| I7 | Insecure Data Transfer and Storage |
| I8 | Lack of Device Management |
| I9 | Insecure Default Settings |
| I10 | Lack of Physical Hardening |

## OWASP IoT Attack Surface Areas (18)

*Full detail incl. per-area vulnerabilities: [02](02-iot-attack-surface-and-vulnerabilities.md#owasp-iot-attack-surface-areas-all-18)*

1. Ecosystem (General) · 2. Device Memory · 3. Device Physical Interfaces · 4. Device Web Interface · 5. Device Firmware · 6. Device Network Services · 7. Administrative Interface · 8. Local Data Storage · 9. Cloud Web Interface · 10. Third-party Backend APIs · 11. Update Mechanism · 12. Mobile Application · 13. Vendor Backend APIs · 14. Ecosystem Communication · 15. Network Traffic · 16. Authentication/Authorization · 17. Privacy · 18. Hardware (Sensors)

## The 21 IoT Threat Categories

*Full detail: [03](03-iot-attacks-and-threats.md#the-21-iot-threat-categories)*

01. DDoS Attack · 02. Attack on HVAC Systems · 03. Rolling Code Attack · 04. BlueBorne Attack · 05. Jamming Attack · 06. Remote Access using Backdoor · 07. Remote Access using Telnet · 08. Sybil Attack · 09. Exploit Kits · 10. MITM Attack · 11. Replay Attack · 12. Forged Malicious Device · 13. Side-Channel Attack · 14. Ransomware Attack · 15. Client Impersonation · 16. SQL Injection Attack · 17. SDR-Based Attack · 18. Fault Injection Attack · 19. Network Pivoting · 20. DNS Rebinding Attack · 21. Firmware Update (FOTA) Attack

## MITRE ATT&CK for ICS — 12 Tactics

*Full detail incl. techniques: [08](08-ot-attacks-and-threats.md#mitre-attck-for-ics)*

1. Initial Access · 2. Execution · 3. Persistence · 4. Privilege Escalation · 5. Evasion · 6. Discovery · 7. Lateral Movement · 8. Collection · 9. Command and Control · 10. Inhibit Response Function · 11. Impair Process Control · 12. Impact

---

## The Purdue Model — Levels at a Glance

*Full detail: [07](07-ot-ics-concepts-and-architecture.md#the-purdue-model)*

| Zone | Level | Contains |
|---|---|---|
| Enterprise | 5 | Enterprise network |
| Enterprise | 4 | Business logistics systems |
| *Industrial DMZ* | 3.5 | Jump servers, data brokers |
| Manufacturing | 3 | Site operations (historian, MES) |
| Manufacturing | 2 | Supervisory control (SCADA, HMI) |
| Manufacturing | 1 | Basic control (PLCs, RTUs, VFDs) |
| Manufacturing | 0 | Physical process (sensors, actuators) |

---

## IoT Wireless/Wired Protocols by Range

*Full detail: [01](01-iot-concepts-and-architecture.md#iot-technologies-and-protocols)*

| Range | Protocols |
|---|---|
| **Short-range** | BLE, Li-Fi, NFC |
| **Medium-range** | HaLow (802.11ah), LTE-Advanced, 6LoWPAN |
| **Long-range** | LPWAN, LoRaWAN, Sigfox, NB-IoT, Neul, VSAT, Cellular, MQTT, QUIC |
| **Wired** | Ethernet, MoCA, Power-Line Communication (PLC) |

## OT Protocols by Purdue Level

*Full detail: [07](07-ot-ics-concepts-and-architecture.md#ot-technologies-and-protocols-per-purdue-level)*

| Level | Protocols |
|---|---|
| **4 & 5** | DCOM, FTP/SFTP, GE-SRTP, IPv4/IPv6, OPC UA, TCP/IP, SMTP/HTTP/HTTPS, Wi-Fi |
| **3** | ISA/IEC 62443, Modbus, NTP, Profinet, SuiteLink, Tase-2 (IEC 60870-6), ControlNet, Profibus PA/DP, Omron FINS, PCWorx, Sercos III, S7 Communication, WiMax, FOUNDATION Fieldbus, RDP/VNC/SSH |
| **2 & 0/1** | 6LoWPAN, DNP3, DNS/DNSSEC, FTE, HART-IP, IEC 60870-5-101/104, SOAP, DeviceNet, AS-Interface (AS-i), BACnet, EtherCAT, CANopen, Crimson, Zigbee, ISA SP100, MELSEC-Q, Niagara Fox |

---

## IoT Tools by Category

| Category | Tools |
|---|---|
| **Recon / OSINT** | Shodan, Censys, FOFA, FCC ID Search |
| **Sniffing** | NetworkMiner, Suphacap, IoT Inspector 2, ZBOSS Sniffer, tcpdump, Ubiqua Protocol Analyser, Perytons Protocol Analyzers, Cascoda Packet Sniffer, SmartRF Packet Sniffer |
| **Vulnerability Scanning** | IoTSeeker, Genzai, Nmap, beSTORM, Metasploit, IoTSploit, IoTVAS, Enterprise IoT Security (Palo Alto) |
| **Spectrum / Traffic Analysis** | Gqrx, ONEKEY |
| **SDR Attacks** | Universal Radio Hacker (URH), BladeRF, TempestSDR, HackRF One, GP-Simulator, RFCrack, RTL-SDR, GNU Radio |
| **Bus / Hardware Hacking** | EXPLIoT (Bus Auditor), JTAGulator, Attify Badge, Saleae Logic Analyzer, ChipWhisperer |
| **Camera Exploitation** | CamOver |
| **Firmware** | Firmware Mod Kit, binwalk, QEMU |
| **Zigbee / 802.15.4** | Open Sniffer, KillerBee, CatSniffer |
| **Frameworks** | PENIOT, RouterSploit, wiz_exploit |
| **Device Management** | Azure IoT Central, Oracle Fusion Cloud IoT, Golioth, AWS IoT Device Management, IBM Watson IoT Platform, openBalena |
| **Security Platforms** | SeaCat.io, Armis Centrix, ByteSweep, Entrust IoT Security, IOT ASSET DISCOVERY, FortiNAC, Microsoft Defender for IoT, Symantec CSP, Cisco Industrial Threat Defense, AWS IoT Device Defender, Forescout, NSFOCUS Anti-DDoS, Azure Sphere, Overwatch, Barbara, Sternum, Asimily |

## OT Tools by Category

| Category | Tools |
|---|---|
| **Recon / OSINT** | Shodan, Censys, CIRT.net, Kamerka-GUI, SearchDiggity, Zeek, Criminal IP, ZoomEye, ONYPHE |
| **Scanning** | Nmap (NSE scripts), NetworkMiner, Wireshark, Malcolm |
| **Vulnerability Scanning** | Nessus, Skybox Vulnerability Control, Microsoft Defender for IoT |
| **Sniffing** | SmartRF Packet Sniffer |
| **Fuzzing** | Fuzzowski |
| **Hardware Hacking (software)** | GDB, OpenOCD, Binwalk, Fritzing, Radare2, Ghidra, IDA Pro |
| **Hardware Hacking (physical)** | Signal analyzer, multimeter, memory programmer, oscilloscope, soldering equipment, digital microscope, JTAG interface, precision screwdrivers/tweezers |
| **Modbus/PLC Exploitation** | Metasploit (`modbus_findunitid`, `modbusclient`), modbus-cli, mbtget |
| **Exploitation Frameworks** | CSET, AttkFinder, ICSREF, ICSFuzz, ISF |
| **Firewalls** | FortiGate Rugged NGFW, OTIFYD Next-Gen OT Firewall |
| **Identity/Access Mgmt** | Claroty, MetaDefender IT-OT Access |
| **Asset Inventory** | SCADAfence, Otbase, Guardian, Dragos |
| **Monitoring/Anomaly Detection** | ISID, Rhebo OT Security, Flowmon, Tenable OT Security, Nozomi Networks, Forescout, FortiGuard, RAM² |
| **Deception/Honeypots** | Attivo Networks ThreatDefend, Conpot, GasPot |

---

**See also:** [CHEATSHEET-commands.md](CHEATSHEET-commands.md) for copy/paste-ready commands.
