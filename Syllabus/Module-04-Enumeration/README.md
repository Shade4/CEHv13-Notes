# Module 04 — Enumeration

Personal study notes for **CEH v13 – Module 04: Enumeration**, rewritten and expanded from the official courseware (`CEHv13 - Module 04 - Enumeration`, pgs. 425–542) into a self-contained, repo-ready reference. Companion to the [Module 03 — Scanning Networks](../CEH-Module-03-Scanning-Networks) notes.

> **Scope note:** These are original study notes — concepts, commands, and explanations rewritten in my own words for revision and lab reference. They are not a copy of the EC-Council courseware; screenshots/figures referenced from the source slides are described rather than reproduced.

---

## Where Enumeration Fits

```
   FOOTPRINTING          SCANNING              ENUMERATION            (this module)
   (passive recon)  →   (Module 03)      →     "who exactly is
   "who/where"           "what's alive,          on this system,
                          what's open"            and what can
                                                   I do with it?"
```

Scanning tells you a port is open. Enumeration is what you do *with* that open port — you connect to it, talk to whatever service is listening, and pull out specific, actionable details: usernames, machine names, shares, groups, routing tables, SNMP community strings, DNS records, and more. It's the last stop before an attacker picks a specific account or vulnerability to go after.

**Key distinction from scanning:** enumeration requires an **active connection** to the target and **directed queries** — it's no longer just "is this port open," it's "let me log in / query / walk this service and see what falls out." Because of that active-connection requirement, enumeration techniques generally only work inside the target's own network/intranet, not from an arbitrary point on the internet.

**Legal note directly from the source material, worth keeping in mind:** unlike passive footprinting, enumeration activity can cross into illegal territory depending on an organization's policies and local law — always get proper authorization before doing this against a real target.

## Module Learning Objectives

1. Explain enumeration concepts
2. Demonstrate different techniques for NetBIOS enumeration
3. Demonstrate different techniques for SNMP enumeration and LDAP enumeration
4. Use different techniques for NTP and NFS enumeration
5. Demonstrate different techniques for SMTP and DNS enumeration
6. Demonstrate IPsec, VoIP, RPC, Unix/Linux, and SMB enumeration
7. Explain enumeration countermeasures

---

## Table of Contents

| # | File | Covers |
|---|------|--------|
| 01 | [`01-enumeration-concepts.md`](01-enumeration-concepts.md) | What enumeration is, what it extracts, extraction techniques, full services/ports-to-enumerate reference |
| 02 | [`02-netbios-enumeration.md`](02-netbios-enumeration.md) | NetBIOS name table, `nbtstat`, NetBIOS Enumerator, Nmap NSE, PsTools suite (PsExec–PsShutdown), `net view`, AI-assisted enumeration |
| 03 | [`03-snmp-and-ldap-enumeration.md`](03-snmp-and-ldap-enumeration.md) | SNMP architecture/MIB/OIDs, SnmpWalk, Nmap SNMP scripts, snmp-check & other tools, AI; LDAP/DSA sessions, manual Python enumeration, `ldapsearch`, `ldap-brute`, tools |
| 04 | [`04-ntp-and-nfs-enumeration.md`](04-ntp-and-nfs-enumeration.md) | `ntpdate`/`ntptrace`/`ntpdc`/`ntpq` full reference, NTP tools; `rpcinfo`/`showmount`, RPCScan, SuperEnum |
| 05 | [`05-smtp-and-dns-enumeration.md`](05-smtp-and-dns-enumeration.md) | SMTP VRFY/EXPN/RCPT TO, Nmap/Metasploit/smtp-user-enum, AI; DNS zone transfer (`dig`/`nslookup`/DNSRecon), DNS cache snooping, DNSSEC zone walking, OWASP Amass, Nmap DNS/DNSSEC scripts |
| 06 | [`06-other-enumeration-techniques.md`](06-other-enumeration-techniques.md) | IPsec (ISAKMP/ike-scan), VoIP (Svmap/Metasploit SIP), RPC (`rpcinfo`/Nmap/NetScanTools), Unix/Linux user enumeration (`rusers`/`rwho`/`finger`), SMB enumeration, AI-generated automation scripts |
| 07 | [`07-enumeration-countermeasures.md`](07-enumeration-countermeasures.md) | Defensive controls for every service above: SNMP, LDAP, NFS, SMTP, SMB, DNS |
| — | [`cheatsheet.md`](cheatsheet.md) | One-page quick reference: every enumeration command grouped by service |

---

## Quick Mental Model — What Gets Enumerated

| Service | Port(s) | What it typically leaks |
|---|---|---|
| NetBIOS | UDP 137, UDP 138, TCP 139 | Computer/domain names, shares, logged-in users, MAC address |
| SNMP | UDP 161 (agent), UDP 162 (trap) | Hosts, routers, ARP/routing tables, running processes, installed software, user accounts |
| LDAP | TCP/UDP 389 (636 for LDAPS) | Usernames, addresses, departmental details, org structure |
| NTP | UDP 123 | Connected hosts, client IPs/system names/OSes, internal IPs if server is in the DMZ |
| NFS | TCP 2049 (+ port mapper TCP/UDP 111) | Exported directories, connected clients + their IPs, shared data |
| SMTP | TCP 25 (also 587, 2525) | Valid usernames/mailboxes via VRFY/EXPN/RCPT TO |
| DNS | TCP/UDP 53 | Full zone data (zone transfer), cached-record snooping, subdomains (zone walking) |
| IPsec/ISAKMP | UDP 500 | VPN gateway presence, encryption/hash algorithms, key exchange details |
| VoIP/SIP | UDP/TCP 2000, 2001, 5060, 5061 | SIP devices, PBX servers, user-agent IPs, extensions |
| RPC | TCP/UDP 111 (portmapper) | Registered RPC services and the ports they listen on |
| SMB | TCP 445 (legacy: UDP 137/138, TCP 139) | OS/version banners, shares, users, security mode |

## Lab Environment Referenced in Source Material

- Attacker host: Parrot Security OS (terminal examples use `root@parrot` / `attacker@parrot`)
- Primary targets: `10.10.1.11` (WINDOWS11), `10.10.1.22` (SERVER2022 / domain CEH.com), `10.10.1.19` (www.goodshopping.com), `10.10.1.9` / `10.10.1.13` (Linux/Ubuntu hosts)
- Domains used in DNS examples: `certifiedhacker.com`, `www.certifiedhacker.com`
- Tooling: Nmap/Zenmap, Hping3-adjacent tools, Metasploit, Wireshark, PsTools, SoftPerfect Network Scanner, NetScanTools Pro, Softerra LDAP Administrator, DNSRecon, LDNS, OWASP Amass, ike-scan, Svmap

## Tools Index (all tools mentioned across this module)

| Category | Tools |
|---|---|
| NetBIOS | Nbtstat, NetBIOS Enumerator, Nmap (`nbstat.nse`), Global Network Inventory, Advanced IP Scanner, Hyena, Nsauditor, PsTools suite |
| SNMP | SnmpWalk, Nmap SNMP NSE scripts, snmp-check, SoftPerfect Network Scanner, Network Performance Monitor, OpUtils, PRTG Network Monitor, Engineer's Toolset |
| LDAP | Python `ldap3`, Nmap `ldap-brute`, `ldapsearch`, Softerra LDAP Administrator, AD Explorer, LDAP Admin Tool, LDAP Account Manager, LDAP Search |
| NTP | `ntpdate`, `ntptrace`, `ntpdc`, `ntpq`, PRTG Network Monitor, Nmap, Wireshark, udp-proto-scanner, NTP Server Scanner |
| NFS | `rpcinfo`, `showmount`, RPCScan, SuperEnum |
| SMTP | Telnet/netcat, Nmap SMTP NSE scripts, Metasploit `smtp_enum`, NetScanTools Pro, smtp-user-enum |
| DNS | `dig`, `nslookup`, DNSRecon, LDNS, OWASP Amass, Nmap DNS/DNSSEC NSE scripts, Knock, Raccoon, Subfinder, Turbolist3r |
| IPsec | Nmap, ike-scan |
| VoIP | Svmap, Metasploit SIP scanner modules |
| RPC | Nmap, NetScanTools Pro |
| Unix/Linux users | `rusers`, `rwho`, `finger` |
| SMB | Nmap, SMBMap, enum4linux, nullinux, SMBeagle, NetScanTools Pro |
| Detection/defense | Same enterprise monitoring stack as Module 03 (Snort, ExtraHop-class tooling), plus service-specific hardening covered in file `07` |

---

## How to Use This Repo

Read `01 → 07` in order the first time through — each file assumes the terminology from the ones before it. After that, `cheatsheet.md` is meant to be the one you keep open during labs/CTFs.

**Ethical/legal note:** All techniques described here are for use in authorized penetration testing, CTFs, and personal lab environments only. Enumerating systems you don't own or don't have written permission to test is illegal in most jurisdictions.
