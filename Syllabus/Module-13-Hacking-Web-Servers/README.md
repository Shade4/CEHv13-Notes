# CEH v13 — Module 13: Hacking Web Servers

A complete, GitHub-flavored-Markdown reference built from the **EC-Council CEH v13, Module 13 ("Hacking Web Servers")** official courseware (130-page PDF, Exam 312-50). Every attack, tool, and command shown in the source deck has been transcribed and verified against the original screenshots, then expanded with additional real-world context, extra commands, and corrected/annotated explanations where the courseware's own wording was imprecise.

> **Scope note:** This module deliberately overlaps with several other CEH modules (System Hacking, DoS/DDoS, Session Hijacking, Social Engineering, Hacking Web Applications). Where the source material says "refer to Module X," this repo keeps the pointer but still explains the concept in-line so each file is self-contained.

## ⚠️ Legal & Ethical Use

Everything in this repository is for **authorized security testing, CEH exam preparation, and defensive learning only**. Only run any command here against systems you own or have **explicit written permission** to test (e.g., a personal lab, HackTheBox/TryHackMe, or a signed pentest engagement). Unauthorized access to computer systems is illegal in virtually every jurisdiction (e.g., the Computer Fraud and Abuse Act in the US, the IT Act 2000 in India). IP addresses like `10.10.1.x` used throughout are private RFC 1918 lab addresses taken directly from the courseware's practice range — replace them with your own lab targets.

## 📚 Table of Contents

| # | File | Covers |
|---|------|--------|
| 01 | [Web Server Concepts & Architecture](01-web-server-concepts-and-architecture.md) | Web server operations, document/server root, virtual hosting, Apache/IIS/Nginx architecture & CVE-style vulnerability tables |
| 02 | [Web Server Attack Techniques](02-web-server-attack-techniques.md) | DNS hijacking, DNS amplification, directory traversal, defacement, misconfiguration, HTTP response-splitting, cache poisoning, SSH/FTP brute force, HTTP/2 continuation flood, frontjacking |
| 03 | [Attack Methodology — Recon & Footprinting](03-attack-methodology-recon-and-footprinting.md) | The 6-phase attack methodology, information gathering, banner grabbing, Shodan dorks, the full Nmap NSE script arsenal, default creds/content |
| 04 | [Directory Brute-Forcing & Mirroring](04-directory-bruteforcing-and-mirroring.md) | Dirhunt, Gobuster, AI-assisted brute forcing, + bonus HTTrack/Wget mirroring |
| 05 | [Vulnerability Scanning & Exploitation](05-vulnerability-scanning-and-exploitation.md) | Acunetix, Nginxpwner, Exploit-DB workflow, AI + searchsploit-nmap, Nginx alias path traversal (Kyubi) |
| 06 | [Session Hijacking & Password Cracking](06-session-hijacking-and-password-cracking.md) | Burp Suite Sequencer, JHijack, Ettercap, Hashcat, THC-Hydra, Ncrack |
| 07 | [Web Server Attack Tools](07-web-server-attack-tools.md) | Immunity CANVAS, OpenVAS, HULK, MPack |
| 08 | [Countermeasures & Hardening](08-countermeasures-and-hardening.md) | Network segmentation, patch/protocol/account/file hardening, detecting hacking attempts, defending each attack class |
| 09 | [Security Scanning & Monitoring Tools](09-security-scanning-and-monitoring-tools.md) | Web app scanners, web server scanners, malware monitoring, pen-testing platforms |
| 10 | [Patch Management](10-patch-management.md) | Patch/hotfix lifecycle, installation methods, best practices, enterprise patch tools |
| — | [Cheatsheet: Command Quick Reference](cheatsheets/01-command-quick-reference.md) | Every command in this module, copy-paste ready, grouped by task |
| — | [Cheatsheet: Attack ↔ Defense Methodology Map](cheatsheets/02-attack-defense-methodology-map.md) | Methodology flow diagram, attack→tool→detection→defense matrix, pentest checklist |

## 🎯 Learning Objectives (from the courseware)

By the end of this module you should be able to:
1. Summarize web server concepts
2. Demonstrate different web server attacks
3. Explain the web server attack methodology
4. Explain web server attack countermeasures

## 🧭 How This Repo Is Organized

Each numbered file corresponds to a stage of a real web server penetration test, roughly following the courseware's own attack methodology:

```
Information Gathering → Footprinting → (Mirroring) → Vulnerability Scanning
        → Session Hijacking → Password Cracking → Exploitation → Reporting
```

Countermeasure files (08–10) are written so a **blue-teamer** can use them standalone as a hardening checklist, independent of the attack files.

## 🗒️ Module Summary (from the source deck)

> In this module, we discussed in detail the general concepts related to web servers; various web server threats and attacks; the web server attack methodology in detail, including information gathering, web server footprinting, vulnerability scanning, and web server password hacking; and various web server hacking tools. Additionally, we discussed various countermeasures that can be employed to prevent web server hacking attempts. We conclude the discussion with a detailed look at how to secure web servers using various security tools.
>
> In the next module (Module 14), the courseware discusses how attackers, as well as ethical hackers and pen testers, hack web applications.

## 📖 Source

- **EC-Council CEH v13, Module 13 — Hacking Web Servers**, Exam 312-50 (Certified Ethical Hacker), 130 pages.
- Every external tool/site URL (nmap.org, exploit-db.com, cirt.net, etc.) is cited as given in the original courseware.
- Corrections/clarifications added by this repo's author are explicitly marked with a **📝 Note** callout so the original courseware content and the added analysis are never blurred together.
