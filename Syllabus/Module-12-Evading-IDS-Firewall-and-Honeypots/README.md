# 🛡️ Network Perimeter Security — IDS, IPS, Firewalls, Honeypots & Evasion

> Deep-dive study notes and reference documentation on network security technologies — how they work, how they're placed in a network, how they're classified, how to configure them, and crucially how attackers evade them (so defenders can detect and stop that evasion).
>
> Based on **CEH v13 — Module 12: Evading IDS, Firewalls, and Honeypots** (EC-Council courseware), expanded with extra explanations, Mermaid diagrams recreating every figure, comparison tables, hands-on commands, and practical lab setups.

---

## 📖 About this repo

Every diagram from the source slides has been:

1. **Explained in full prose** — what it shows, why it's designed that way, what each component does.
2. **Redrawn as a Mermaid diagram** — renders natively on GitHub without needing the original screenshot.
3. **Backed by practical commands** — real CLI commands / config snippets so concepts can be tried in a home lab.

> ⚠️ **Note:** Source material is derived from proprietary EC-Council CEH courseware for personal study. Keep this repo private if forking.

---

## 🎯 Learning Objectives

- [x] Describe IDS, IPS, and firewall concepts
- [x] Use different IDS, IPS, and firewall solutions (Snort, Suricata, Zeek, iptables, pfSense)
- [x] Explain different techniques to bypass IDS
- [x] Explain various techniques to bypass firewalls
- [x] Explain various techniques to bypass NAC and endpoint security
- [x] Use different tools to evade IDS/firewalls
- [x] Explain honeypot concepts and techniques to detect honeypots
- [x] Adopt countermeasures against IDS/firewall/endpoint evasion

---

## 🗂️ Repository Structure

```
.
├── README.md
├── CHANGELOG.md
├── 01-intrusion-detection-system/
│   └── README.md                           ← IDS concepts, placement (Fig 12.1–12.2), detection methods,
│                                               indicators, NIDS (Fig 12.4), HIDS (Fig 12.5), alert types,
│                                               Snort quick-start lab
├── 02-intrusion-prevention-system/
│   └── README.md                           ← IPS concepts, IDS vs IPS, placement (Fig 12.3),
│                                               classification, advantages, Suricata inline IPS setup
├── 03-firewalls/
│   └── README.md                           ← Firewall concepts (Fig 12.6), architecture (Fig 12.7–12.9),
│                                               DMZ (Fig 12.10), network/host-based (Fig 12.11–12.12),
│                                               OSI mapping (Table 12.1), all 7 firewall types
│                                               (Fig 12.13–12.14 + Application, Stateful, Proxy, NAT, VPN),
│                                               NGFWs, limitations, YARA rules, Snort rule reference,
│                                               iptables/firewalld/netsh/pfSense configs
├── 04-tools-commands-and-labs/
│   └── README.md                           ← Lab topology, Wireshark/tcpdump, Snort, Suricata, Zeek,
│                                               OSSEC/Wazuh, Security Onion, firewall command reference,
│                                               validation testing, hands-on exercises
├── 05-honeypots/
│   └── README.md                           ← What is a honeypot, low/medium/high/pure interaction,
│                                               production vs research, malware/spam/email/spider/DB/honeynet
│                                               types, tools (Cowrie, T-Pot, HoneyBOT etc.),
│                                               5 detection methods (fingerprinting, latency, MAC,
│                                               open ports, metadata), defeating specific honeypot types
│                                               (Honeyd, UML, VMware, tar pits, Snort_inline, Fake AP,
│                                               Bait-and-Switch), Send-Safe detection tool, lab setup
├── 06-evasion-and-bypass-techniques/
│   ├── README.md                           ← Index for all three sub-sections
│   ├── 06a-firewall-evasion/
│   │   └── README.md                       ← Port scanning, firewalking, banner grabbing, IP spoofing,
│   │                                           source routing, tiny fragments, IP bypass, anonymizers,
│   │                                           proxy bypass, ICMP tunnel, ACK tunnel, HTTP tunnel
│   │                                           (HTTPort/HTTHost + Chisel), SSH tunnel (OpenSSH + Bitvise
│   │                                           local/remote/dynamic), DNS tunnel (iodine + dnscat2),
│   │                                           external systems, MITM/DNS poisoning, malicious content,
│   │                                           XSS/WAF bypass (ASCII/hex/obfuscation/headers/fuzzing/SSL),
│   │                                           HTML smuggling, Windows BITS evasion
│   ├── 06b-ids-evasion/
│   │   └── README.md                       ← Insertion attack, evasion attack, DoS against IDS,
│   │                                           obfuscating, false positive generation, session splicing,
│   │                                           unicode evasion, fragmentation attack (2 scenarios),
│   │                                           TTL attack, urgency flag, invalid RST, polymorphic shellcode
│   │                                           (msfvenom), ASCII shellcode, application-layer attacks,
│   │                                           desynchronization (pre/post SYN), DGA (4 types),
│   │                                           encryption, flooding
│   └── 06c-nac-and-endpoint-evasion/
│       └── README.md                       ← VLAN hopping (VLANPWN), pre-auth bypass (nac_bypass_setup.sh,
│                                               FENRIR, NACkered, Silentbridge), ghostwriting, DLL hijacking,
│                                               dechaining macros (ShellCOM/XMLDOM/WMI/scheduled tasks/
│                                               registry/file drop/XMLHTTP download/msfvenom VBA),
│                                               clearing memory hooks (x64dbg), process injection
│                                               (VirtualAllocEx/WriteProcessMemory/CreateRemoteThread),
│                                               LoLBins (ConfigSecurityPolicy/CustomShellHost + full table),
│                                               CPL sideloading (CPLResourceRunner), ChatGPT-assisted
│                                               malware (Python ransomware examples), Metasploit template
│                                               modification (with VirusTotal testing workflow),
│                                               AMSI bypass (4 techniques: downgrade/obfuscation/
│                                               force-error/memory hijacking), 12 advanced EDR evasion
│                                               techniques (cloud phishing/Base64/fast flux/timing/
│                                               LoLBins/shellcode encryption/entropy/sandbox escape/
│                                               ETW disable/direct syscalls/call stack spoofing/
│                                               in-memory beacon encryption)
├── 07-evasion-tools/
│   └── README.md                           ← Traffic IQ Professional, Nmap (all evasion flags),
│                                               PingRAT, Green Tunnel, Metasploit (encoding/evasion),
│                                               KoviD rootkit, Hyperion PE encryptor,
│                                               Colasoft Packet Builder, NetScanTools Pro, CommView,
│                                               Ostinato (with Python API), WAN Killer, WireEdit,
│                                               full comparison table
└── 08-countermeasures/
    └── README.md                           ← IDS evasion defense (config/tuning/capacity/encryption),
                                                technique-by-technique countermeasure table, firewall
                                                hardening (default-deny/egress/anti-spoof/tunneling/
                                                ICMP/DNS/HTTP/SSH/BITS), WAF hardening, endpoint/AV
                                                defense (macro policy/ASR/PowerShell logging/CLM/
                                                Credential Guard/Memory Integrity/Sysmon/WDAC),
                                                NAC defense (DTP disable/802.1X/post-admission NAC),
                                                AV defense (AMSI/ML/cloud/signed scripts),
                                                architecture best practices (Defence in Depth/Zero Trust),
                                                audit cadence table, logging/monitoring checklist
```

---

## 🖼️ Figure Index

| Figure | Title | Location |
|---|---|---|
| Fig 12.1 | Placement of IDS | [01 — IDS](01-intrusion-detection-system.md#where-ids-resides-in-the-network) |
| Fig 12.2 | Working of IDS | [01 — IDS](./01-intrusion-detection-system/README.md#how-an-ids-works) |
| Fig 12.3 | IPS placement example | [02 — IPS](./02-intrusion-prevention-system/README.md#where-ips-sits-in-the-network) |
| Fig 12.4 | Network-based IDS (NIDS) | [01 — IDS](./01-intrusion-detection-system/README.md#network-based-intrusion-detection-systems-nids) |
| Fig 12.5 | Host-based IDS (HIDS) | [01 — IDS](./01-intrusion-detection-system/README.md#host-based-intrusion-detection-systems-hids) |
| Fig 12.6 | Example of a Firewall | [03 — Firewalls](./03-firewalls/README.md#what-is-a-firewall) |
| Fig 12.7 | Bastion Host Firewall | [03 — Firewalls](./03-firewalls/README.md#1-bastion-host) |
| Fig 12.8 | Screened Subnet Firewall | [03 — Firewalls](./03-firewalls/README.md#2-screened-subnet-dmz) |
| Fig 12.9 | Multi-homed Firewall | [03 — Firewalls](./03-firewalls/README.md#3-multi-homed-firewall) |
| Fig 12.10 | Demilitarized Zone (DMZ) | [03 — Firewalls](./03-firewalls/README.md#demilitarized-zone-dmz) |
| Fig 12.11 | Network-based Firewall | [03 — Firewalls](./03-firewalls/README.md#network-based-firewalls) |
| Fig 12.12 | Host-based Firewall | [03 — Firewalls](./03-firewalls/README.md#host-based-firewalls) |
| Table 12.1 | Firewall Technologies (OSI) | [03 — Firewalls](./03-firewalls/README.md#osi-layer--firewall-technology-mapping) |
| Fig 12.13 | Packet Filtering Firewall | [03 — Firewalls](./03-firewalls/README.md#1-packet-filtering-firewall) |
| Fig 12.14 | Circuit-Level Gateway | [03 — Firewalls](./03-firewalls/README.md#2-circuit-level-gateway-firewall) |
| Fig 12.22+ | Evasion tool examples | [06 — Evasion](./06-evasion-and-bypass-techniques/) |
| Fig 12.78+ | Honeypot diagrams | [05 — Honeypots](./05-honeypots/README.md) |

---

## 🚀 Using as a GitHub repo

```bash
cd network-perimeter-security-notes
git init
git add .
git commit -m "Complete CEH Module 12 notes: IDS/IPS/Firewalls/Honeypots/Evasion/Countermeasures"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

---

## 📚 Sources

- EC-Council **CEH v13**, Module 12: *Evading IDS, Firewalls, and Honeypots* — used here for personal study notes only.
