# CEH v13 — Module 16: Hacking Wireless Networks

A comprehensive, hands-on reference built from the **CEH v13 Module 16 (Hacking Wireless Networks)** courseware — 140 slides covering wireless concepts, encryption, threats, attack methodology, tool-by-tool procedures, and countermeasures. Every command in this repository is reproduced exactly as demonstrated in the source material (interface names, BSSIDs, and flags included) and supplemented with additional detail, context, and modern tooling notes for practical use in **authorized** penetration testing and CTF environments.

> ⚠️ **Legal & Ethical Use Only**
> Everything in this repository — every tool, command, and technique — is intended strictly for use against networks and devices **you own** or **have explicit, documented, written authorization** to test (e.g., a signed penetration testing engagement, a CTF/lab environment, or your own home lab). Unauthorized access to wireless networks is illegal in most jurisdictions under laws such as the U.S. Computer Fraud and Abuse Act (CFAA), the UK Computer Misuse Act, and India's IT Act, 2000 (Sections 43 & 66). Interfering with radio spectrum (jamming) is separately regulated by telecom authorities (FCC, TRAI, Ofcom, etc.) almost everywhere. Use this material to learn, defend, and test responsibly.

---

## 📚 What This Covers

This repo maps 1:1 onto the five learning objectives of the official module, then adds two consolidated cheat sheets for fast lookup during labs or exams.

| # | File | Objective Covered |
|---|------|--------------------|
| 01 | [`01-wireless-concepts.md`](01-wireless-concepts.md) | Wireless terminology, network types, SSID, Wi-Fi authentication process, Wi-Fi chalking |
| 02 | [`02-wireless-standards-topologies-antennas.md`](02-wireless-standards-topologies-antennas.md) | 802.11 standard family, Wi-Fi 6/6E/7, antenna types, choosing a Wi-Fi adapter |
| 03 | [`03-wireless-encryption-wep-wpa-wpa2-wpa3.md`](03-wireless-encryption-wep-wpa-wpa2-wpa3.md) | WEP, WPA, WPA2, WPA3 internals, 4-way handshake, SAE/Dragonfly, comparison tables, known issues |
| 04 | [`04-wireless-threats.md`](04-wireless-threats.md) | Full attack taxonomy — access-control, integrity, confidentiality, availability, authentication attacks |
| 05 | [`05-wifi-discovery-and-footprinting.md`](05-wifi-discovery-and-footprinting.md) | Passive/active footprinting, WarWalking/Chalking/Driving, discovery tools, WPS discovery |
| 06 | [`06-wireless-traffic-analysis.md`](06-wireless-traffic-analysis.md) | 802.11 frame types, monitor mode, Wireshark/CommView, spectrum analysis |
| 07 | [`07-wireless-attacks-dos-mitm-spoofing.md`](07-wireless-attacks-dos-mitm-spoofing.md) | Deauth/disassoc DoS, MITM with Aircrack-ng, MAC spoofing, ARP poisoning with Ettercap |
| 08 | [`08-rogue-ap-evil-twin-krack-advanced-attacks.md`](08-rogue-ap-evil-twin-krack-advanced-attacks.md) | Rogue APs, MANA Toolkit, Evil Twin, KRACK, jamming, aLTEr, Wi-Jacking, RFID cloning |
| 09 | [`09-wifi-encryption-cracking.md`](09-wifi-encryption-cracking.md) | WEP/WPA/WPA2/WPA3 cracking with Aircrack-ng + hashcat, WPS cracking with Reaver |
| 10 | [`10-wireless-countermeasures-and-wips.md`](10-wireless-countermeasures-and-wips.md) | Defenses per attack class, rogue-AP detection, WIPS architecture, auditing tools |
| — | [`cheatsheet-commands.md`](cheatsheet-commands.md) | Every command in the module, copy-pasteable, grouped by tool |
| — | [`cheatsheet-tools-and-defense.md`](cheatsheet-tools-and-defense.md) | Tool-purpose matrix + a one-page defensive checklist |

## 🗺️ How the Wireless Hacking Methodology Ties Together

```
 ┌─────────────────┐   ┌──────────────────┐   ┌───────────────────┐
 │  1. Wi-Fi        │→ │  2. Wireless      │→ │  3. Launch          │
 │     Discovery    │   │     Traffic       │   │     Wireless        │
 │  (05)            │   │     Analysis (06) │   │     Attacks (07-08) │
 └─────────────────┘   └──────────────────┘   └───────────┬─────────┘
                                                             │
                                    ┌────────────────────────┘
                                    ▼
                       ┌──────────────────────┐    ┌───────────────────────┐
                       │ 4. Wi-Fi Encryption    │→ │ 5. Compromise the      │
                       │    Cracking (09)       │   │    Wi-Fi Network       │
                       └──────────────────────┘    └───────────────────────┘
```

This is the exact five-step methodology EC-Council teaches: **discover → analyze → attack → crack → compromise**. Files 05–09 are ordered to follow it precisely.

## 🧰 Primary Toolset Referenced

| Category | Tools |
|---|---|
| Suite | **Aircrack-ng** (`airmon-ng`, `airodump-ng`, `aireplay-ng`, `airbase-ng`, `airdecap-ng`) |
| WPS | **Reaver**, **Wash** |
| Password cracking | **hashcat**, **Fern Wifi Cracker**, **cowpatty**, **John the Ripper** |
| Rogue AP / MITM | **MANA Toolkit**, **hostapd-wpe**, **Ettercap**, **bettercap** |
| DoS / injection | **mdk3/mdk4**, **aireplay-ng**, **AirJack** |
| Sniffing / analysis | **Wireshark**, **CommView for Wi-Fi**, **Kismet**, **RF Explorer** |
| Discovery | **inSSIDer**, **Sparrow-wifi**, **NetSurveyor**, **Acrylic Wi-Fi Heatmaps** |
| MAC spoofing | **Technitium MAC Address Changer**, `ifconfig`/`ip link` |
| RFID | **iCopy-X**, **RFIDler**, **Flipper Zero**, **Proxmark3** |
| Defense / WIPS | **Cisco Adaptive Wireless IPS**, **WatchGuard Wi-Fi Cloud**, **Arista WIPS**, **RFProtect** |

## 🖥️ Lab Environment Notes

The source material's screenshots use **Parrot OS** (a Debian-based security distro, functionally equivalent to Kali Linux) with a **Ralink Technology MT7601U** USB Wi-Fi adapter (`wlx00e02d886189` — the interface name is the adapter's own MAC address, a naming convention `udev`/`systemd` uses on modern Linux for USB NICs). All commands are cross-referenced against this convention. Where you see `wlan0`, `wlan0mon`, or `mon0` in this repo, substitute your own adapter's interface name (check with `iwconfig` or `ip link show`).

**Adapter requirement:** almost every attack here needs a wireless NIC that supports **monitor mode** and **packet injection** on the target's chipset. Popular choices: Alfa AWUS036ACH/ACHM (RTL8812AU), Alfa AWUS036NHA (Atheros AR9271), Panda PAU09 (RT5572). Built-in laptop Wi-Fi chipsets frequently do **not** support injection.

## 📁 Repository Structure

```
CEH-Module16-Wireless-Hacking/
├── README.md
├── 01-wireless-concepts.md
├── 02-wireless-standards-topologies-antennas.md
├── 03-wireless-encryption-wep-wpa-wpa2-wpa3.md
├── 04-wireless-threats.md
├── 05-wifi-discovery-and-footprinting.md
├── 06-wireless-traffic-analysis.md
├── 07-wireless-attacks-dos-mitm-spoofing.md
├── 08-rogue-ap-evil-twin-krack-advanced-attacks.md
├── 09-wifi-encryption-cracking.md
├── 10-wireless-countermeasures-and-wips.md
├── cheatsheet-commands.md
└── cheatsheet-tools-and-defense.md
```

## 📖 Source

Notes derived from **EC-Council CEH v13, Module 16 — Hacking Wireless Networks** (Exam 312-50), cross-referenced and expanded with publicly documented tool usage (official docs/GitHub repos for Aircrack-ng, Reaver, hashcat, Ettercap, MANA Toolkit, hostapd-wpe, and others). Figure numbers (e.g., *Figure 16.10*) are retained in the text so specific claims can be traced back to the original module.

## 🔗 Related Notes in This Library

- Module 6 — System Hacking
- Module 8 — Sniffing
- Module 9 — Social Engineering
- Module 10 — Denial-of-Service
- Module 11 — Session Hijacking
- Module 13 — Hacking Web Servers
- Module 14 — Hacking Web Applications
- Module 15 — SQL Injection

---
*Compiled for personal study and authorized security testing practice.*
