# CEH v13 — Module 18: IoT and OT Hacking

A complete, hands-on reference library covering **Internet of Things (IoT)** and **Operational Technology (OT) / Industrial Control System (ICS)** security — built from CEH v13 Module 18 courseware (258 slides) and expanded with extra context, real tool syntax, and additional background research.

This is not a slide summary. Every topic file below explains the underlying concept in plain language, then backs it up with **real, runnable commands** — the same tools a penetration tester or ICS security assessor would actually reach for during an engagement.

> ⚠️ **Legal & Ethical Notice**
> Everything documented here — Shodan queries, Nmap NSE scripts, Modbus/PLC interaction commands, SDR replay tooling, firmware analysis workflows, and the malware case studies — is intended strictly for **authorized security testing, CTF practice, home-lab research, and CEH/OSCP-style exam preparation**. IoT devices and OT/ICS environments (SCADA, PLCs, RTUs) frequently control physical processes — pumps, valves, HVAC, power grids, manufacturing lines. Interacting with a live industrial system without **written authorization** can cause real-world physical damage, safety incidents, and is a criminal offense in virtually every jurisdiction. Only ever run these tools against systems you own or have explicit, documented permission to test (a home lab, a vendor-provided test rig, or a scoped penetration test).

---

## 📚 Table of Contents

### IoT Hacking

| # | Topic | What's inside |
|---|-------|----------------|
| 01 | [IoT Concepts and Architecture](01-iot-concepts-and-architecture.md) | What IoT is, the 4-layer IoT architecture, application sectors, short/medium/long-range wireless & wired protocols, communication models, IoT operating systems |
| 02 | [IoT Attack Surface and Vulnerabilities](02-iot-attack-surface-and-vulnerabilities.md) | OWASP IoT Top 10, OWASP's 18 Attack Surface Areas (full vulnerability breakdown), the IoT security-layer model |
| 03 | [IoT Attacks and Threats](03-iot-attacks-and-threats.md) | All 21 IoT threat categories (DDoS, HVAC exploitation, rolling-code, BlueBorne, jamming, SDR attacks, fault injection, Sybil, MITM, side-channel, etc.) with full attack walkthroughs and sector-by-sector attack tables |
| 04 | [IoT Malware and Botnets](04-iot-malware-and-botnets.md) | Mirai-family botnets, IZ1H9 case study, KmsdBot, and a rundown of current IoT malware families |
| 05 | [IoT Hacking Methodology and Tools](05-iot-hacking-methodology-and-tools.md) | The 5-phase methodology — information gathering (Shodan/Censys/FOFA/FCC ID), vulnerability scanning, launching attacks (RF/SDR, hardware bus hacking — UART/JTAG/I2C/SPI, NAND glitching), gaining remote access, maintaining access via firmware |
| 06 | [IoT Countermeasures and Security](06-iot-countermeasures-and-security.md) | Defense checklists, manufacturer guidelines, OWASP Top 10 solutions, hardware security best practices, device-management platforms, security tooling |

### OT / ICS Hacking

| # | Topic | What's inside |
|---|-------|----------------|
| 07 | [OT/ICS Concepts and Architecture](07-ot-ics-concepts-and-architecture.md) | What OT is, ICS components (SCADA/DCS/PLC/HMI/RTU/IED/BPCS/SIS), IT/OT convergence, the Purdue Model, protocols mapped to every Purdue level |
| 08 | [OT Attacks and Threats](08-ot-attacks-and-threats.md) | Challenges & vulnerabilities of OT, MITRE ATT&CK for ICS (all 12 tactics), the 14 OT threat categories, HMI-based attacks, PLC rootkits, the Evil PLC attack, RF remote-controller attacks, supply-chain attacks |
| 09 | [OT Malware Case Studies](09-ot-malware-case-studies.md) | Fuxnet and COSMICENERGY (PIEHOP/LIGHTWORK) deep dives, plus Pipedream, INDUSTROYER.V2, and other ICS-targeting malware |
| 10 | [OT Hacking Methodology and Tools](10-ot-hacking-methodology-and-tools.md) | Information gathering (Shodan/CIRT.net/Kamerka-GUI), Nmap NSE scripts for every major ICS protocol, Nessus/Skybox scanning, protocol fuzzing (Fuzzowski), Modbus/PLC exploitation (Metasploit, modbus-cli, mbtget), ICS hardware hacking |
| 11 | [OT Countermeasures and Security](11-ot-countermeasures-and-security.md) | Purdue-model security controls, Zero-Trust for ICS/SCADA, international OT security bodies, honeypots/decoys, commercial OT security platforms |

### Quick Reference

| File | Purpose |
|------|---------|
| [CHEATSHEET-commands.md](CHEATSHEET-commands.md) | Every command in this repo in one place — copy/paste ready, grouped by tool |
| [CHEATSHEET-tools-and-protocols.md](CHEATSHEET-tools-and-protocols.md) | Every tool, port number, and protocol in one set of lookup tables |

---

## 🗺️ How IoT and OT Hacking Fit Together

```
                    ┌──────────────────────────────────────┐
                    │        Module 18: IoT & OT Hacking     │
                    └──────────────────────────────────────┘
                                    │
              ┌─────────────────────┴─────────────────────┐
              ▼                                             ▼
      ┌───────────────┐                             ┌───────────────┐
      │   IoT Hacking  │                             │   OT Hacking   │
      │ (consumer/     │                             │ (industrial/   │
      │  enterprise     │                             │  critical      │
      │  smart devices) │                             │  infrastructure)│
      └───────┬────────┘                             └───────┬────────┘
              │                                              │
   ┌──────────┼──────────┐                        ┌──────────┼──────────┐
   ▼          ▼          ▼                        ▼          ▼          ▼
Concepts   Attacks    Methodology              Concepts   Attacks    Methodology
& Attack   & Threats  & Tools &                & ICS      & Threats  & Tools &
Surface    & Malware  Countermeasures          Arch.      & Malware  Countermeasures
```

Both halves follow the **same five-phase attacker methodology**:

1. **Information Gathering** — Shodan, Censys, FOFA, FCC ID lookups, sniffing
2. **Vulnerability Scanning** — Nmap NSE, Nessus, IoTSeeker, Genzai, Skybox
3. **Launch Attacks** — protocol abuse, RF/SDR attacks, hardware bus attacks, fuzzing
4. **Gain Remote Access** — Telnet/default creds, DNP3, Modbus write access
5. **Maintain Access** — firmware modification, backdoors, rootkits

---

## 🧰 Lab Setup Recommendations

To practice everything documented in this repo safely:

- **IoT lab**: A Raspberry Pi or ESP32 dev board, a cheap IP camera / smart plug bought specifically for testing, an SDR dongle (RTL-SDR or HackRF One), a Bus Pirate/Attify Badge/Saleae for UART/JTAG/I2C work.
- **OT lab**: A virtual SCADA/PLC sandbox such as **GRFICS** (Graphical Realism Framework for Industrial Control Simulations) or **CONPOT** (honeypot, doubles as a practice Modbus/S7 target), a Siemens LOGO!/S7-1200 PLC or an open-source PLC simulator (e.g., **OpenPLC**), Wireshark with the industrial protocol dissectors enabled.
- **Network isolation**: Run all of this on an isolated VLAN or a dedicated virtual network — never on your home/production LAN, and never against a device or system you don't own or have written authorization to test.

---

## 📖 Source

Built from: **CEH v13 – Module 18: IoT and OT Hacking** (EC-Council official courseware, 258 pages).
Extra depth, tool documentation, and lab guidance added from public vendor/tool documentation (linked inline throughout each file) and general ICS/IoT security practice.

---

## 📂 Repo Structure

```
CEHv13-Module18-IoT-OT-Hacking/
├── README.md                                   ← you are here
├── 01-iot-concepts-and-architecture.md
├── 02-iot-attack-surface-and-vulnerabilities.md
├── 03-iot-attacks-and-threats.md
├── 04-iot-malware-and-botnets.md
├── 05-iot-hacking-methodology-and-tools.md
├── 06-iot-countermeasures-and-security.md
├── 07-ot-ics-concepts-and-architecture.md
├── 08-ot-attacks-and-threats.md
├── 09-ot-malware-case-studies.md
├── 10-ot-hacking-methodology-and-tools.md
├── 11-ot-countermeasures-and-security.md
├── CHEATSHEET-commands.md
└── CHEATSHEET-tools-and-protocols.md
```
