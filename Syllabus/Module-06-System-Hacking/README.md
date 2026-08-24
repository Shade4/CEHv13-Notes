# Module 06 — System Hacking

A structured, from-scratch study reference covering the **System Hacking** domain of the CEH v13 syllabus. This module sits at the center of the ethical hacking methodology: it's the point where everything gathered during footprinting, scanning, and enumeration gets turned into actual access, elevated privileges, persistence, and (for the attacker) a clean exit.

> **Note on sourcing:** This repo is an original set of study notes written to cover the same objectives, tools, and techniques taught in the official CEH v13 courseware — it is **not** a transcription or reproduction of any copyrighted textbook, slide deck, or PDF. Explanations, structure, and examples are written independently. Command syntax, tool names, and protocol names are reproduced exactly where accuracy matters, since those are technical facts rather than someone's creative expression. Where the source material matters (a tool's home page, a CVE, a research write-up), a link is given so you can go read the primary source yourself.

---

## Why System Hacking Matters

Every other CEH module (footprinting, scanning, enumeration, vulnerability analysis) exists to feed this one. Once an attacker has a foothold — a set of credentials, an exploitable service, a vulnerable application — System Hacking is the set of skills that turns that foothold into control: logging in, becoming admin, planting tools that keep the door open, and then making sure nobody notices any of it happened.

The CEH hacking methodology (CHM) breaks this into four stages, and this repo is organized around them:

| Stage | Attacker's Goal | What's Covered Here |
|---|---|---|
| **1. Gaining Access** | Turn recon into a working login or shell | Password cracking, authentication mechanics, buffer overflow exploitation |
| **2. Escalating Privileges** | Turn a low-privilege foothold into admin/root/SYSTEM | DLL hijacking, misconfiguration abuse, UAC bypass, AD privilege escalation |
| **3. Maintaining Access** | Keep control without being kicked out | Keyloggers, spyware, remote execution, rootkits, ADS, steganography, AD persistence |
| **4. Covering Tracks** | Make the intrusion invisible | Log manipulation, anti-forensics, artifact hiding, timestomping |

Every stage has a matching defensive playbook, and this repo tries to give equal weight to both sides — how the attack works, and what a defender should actually do about it. This is written for study, lab practice in an isolated environment you own, and CEH exam prep — **not** as an operational attack guide, and several of the more dangerous specifics (live exploit payload construction, functioning malware code) are deliberately described at a conceptual/procedural level rather than handed over as ready-to-run weapons.

---

## Repo Structure

```
Module-06-System-Hacking/
├── README.md                                          <- you are here
├── 01-Password-Cracking.md                            <- Objective 1, part A
├── 02-Exploiting-Vulnerabilities.md                    <- Objective 1, part B
├── 03-Privilege-Escalation.md                          <- Objective 2
├── 04-Executing-Applications-Keyloggers-Spyware.md      <- Objective 3, part A
├── 05-Hiding-Files-Rootkits-ADS-Steganography.md        <- Objective 3, part B
├── 06-Persistence-and-Domain-Dominance.md               <- Objective 3, part C
├── 07-Covering-Tracks.md                                <- Objective 4
└── CHEATSHEET.md                                        <- quick-reference commands
```

Each topic file follows the same internal shape: concept → how it actually works → tools → attacker walkthrough (command-level where relevant) → detection & defense. Defensive countermeasures are included in every file, not bolted on as an afterthought — in practice you can't understand one side without the other.

---

## Full Table of Contents

### [01 — Password Cracking](./01-Password-Cracking.md)
- How Windows stores credentials: SAM database, NTLM, Kerberos
- The four categories of password attack: non-electronic, active online, passive online, offline
- Dictionary, brute-force, rule-based, and mask attacks
- Hash injection / Pass-the-Hash
- LLMNR/NBT-NS poisoning
- Kerberos password attacks (AS-REP Roasting, Kerberoasting, Pass-the-Ticket, NTLM relay)
- Password guessing, default passwords, GPU-based cracking
- Wire sniffing, MITM/replay attacks
- Rainbow tables and Distributed Network Attacks
- Password cracking & recovery tool index
- Defenses: password policy, MFA, SMB signing, Kerberos hardening

### [02 — Exploiting Vulnerabilities (Buffer Overflows)](./02-Exploiting-Vulnerabilities.md)
- Vulnerability research resources (Exploit-DB, VulDB, OSV, MITRE CVE)
- Metasploit Framework architecture and module types
- Buffer overflow theory: the stack, EIP, memory layout
- The classic exploitation workflow: spiking → fuzzing → offset discovery → EIP control → bad-character analysis → module selection → shellcode
- Return-Oriented Programming (ROP)
- Bypassing ASLR/DEP: heap spraying, JIT spraying
- Buffer overflow detection tools and secure coding countermeasures

### [03 — Privilege Escalation](./03-Privilege-Escalation.md)
- Horizontal vs. vertical privilege escalation
- DLL hijacking and Dylib hijacking (macOS)
- Kernel exploits: Spectre and Meltdown
- Misconfigured services, misconfigured NFS
- Bypassing UAC (multiple techniques)
- Boot/logon initialization script abuse
- Domain policy manipulation and DCSync
- Abusing Active Directory Certificate Services (ADCS / ESC attacks)
- Active Directory enumeration (PowerView, Seatbelt/GhostPack)
- Privilege escalation tool index
- Defenses: least privilege, patching, UAC hardening, ACL auditing

### [04 — Executing Applications, Keyloggers & Spyware](./04-Executing-Applications-Keyloggers-Spyware.md)
- Remote code execution techniques (client exploitation, service execution, WMI, WinRM)
- Remote execution tool index
- Keyloggers: hardware vs. software, all sub-types, Metasploit keylogging
- Spyware: 11 categories, capabilities, propagation
- Anti-keylogger and anti-spyware countermeasures

### [05 — Hiding Files: Rootkits, NTFS ADS & Steganography](./05-Hiding-Files-Rootkits-ADS-Steganography.md)
- Rootkit types (kernel, hypervisor, bootkit, firmware, application, library, memory)
- How rootkits hook the OS (DKOM, function hooking)
- Rootkit detection methods and anti-rootkit tools
- NTFS Alternate Data Streams: creation, manipulation, detection
- Steganography: technical vs. linguistic, computer-based technique families
- Steganography by medium: image, audio, video, document, folder, whitespace, spam/email
- Steganalysis: attack types and detection tools

### [06 — Persistence and Domain Dominance](./06-Persistence-and-Domain-Dominance.md)
- Windows Sticky Keys persistence
- Boot/logon autostart abuse (registry run keys, startup folder)
- Domain dominance overview
- DCSync attack (stages, requirements, mechanics)
- Skeleton key, Golden Ticket, and Silver Ticket attacks
- AdminSDHolder / SDProp abuse
- Living-off-the-land command reference (WMIC, PsExec, Sysinternals, net)
- Defenses against domain persistence

### [07 — Covering Tracks](./07-Covering-Tracks.md)
- Why and how attackers manipulate logs (SECEVENT, SYSEVENT, APPEVENT)
- Disabling auditing (auditpol)
- Clearing logs: Meterpreter, PowerShell, wevtutil, manual clearing (Windows & Linux)
- Covering Bash shell history
- Covering tracks on the network (reverse HTTP shells, ICMP tunneling, DNS tunneling, TCP covert channels)
- Covering tracks on the OS: ADS, timestomping
- Disabling Windows forensic artifacts (last-access timestamps, hibernation, paging file, restore points, thumbnail cache, prefetch)
- Deleting activity history & incognito traces
- Hiding files, folders, and user accounts (Windows, Linux, macOS)
- Anti-forensics technique taxonomy
- Track-covering tools
- Defenses: centralized logging, SIEM, immutable logs, FIM

### [CHEATSHEET](./CHEATSHEET.md)
Every command referenced across the whole module, grouped by task, for fast lookup during labs or exam review.

---

## Master Tool Index

Grouped by function. Each entry links to the vendor/project's own site — always verify current legality and licensing terms before using any tool, and only ever run these against systems you own or are explicitly authorized to test.

### Password Cracking & Recovery
| Tool | Purpose | Link |
|---|---|---|
| John the Ripper | Offline hash cracking (dictionary/rule-based) | https://www.openwall.com/john/ |
| hashcat | GPU-accelerated hash cracking (dictionary/brute-force/mask) | https://hashcat.net |
| L0phtCrack | Windows password auditing | https://gitlab.com |
| THC-Hydra | Online brute-force across many protocols | https://github.com (thc-hydra) |
| RainbowCrack / rtgen | Rainbow-table generation and cracking | http://project-rainbowcrack.com |
| Cain & Abel | Legacy Windows password recovery/sniffing suite | — |
| Mimikatz | Credential/hash/ticket extraction | https://github.com (gentilkiwi/mimikatz) |
| DSInternals | AD credential/hash extraction (PowerShell) | https://github.com |
| pwdump7 | SAM hash extraction | — |
| Responder | LLMNR/NBT-NS/MDNS poisoning | https://github.com |
| Elcomsoft Distributed Password Recovery | Distributed password/key recovery | https://www.elcomsoft.com |
| Passware Kit Forensic | Password/encryption recovery | https://www.passware.com |
| Exterro PRTK | Distributed Network Attack toolkit | — |

### Exploitation
| Tool | Purpose | Link |
|---|---|---|
| Metasploit Framework | Exploit development & delivery platform | https://www.metasploit.com |
| Immunity Debugger | Windows exploit-dev debugger (buffer overflow work) | — |
| mona.py | Immunity Debugger plugin for exploit dev | https://github.com |
| Exploit-DB | Public exploit archive | https://www.exploit-db.com |
| VulDB | Vulnerability/exploit database | https://vuldb.com |
| OSV | Open-source vulnerability database | https://osv.dev |
| MITRE CVE | CVE database | https://www.cve.org |
| WES-NG | Windows patch-gap exploit suggester | https://github.com |

### Privilege Escalation
| Tool | Purpose | Link |
|---|---|---|
| Spartacus | Automated DLL hijacking discovery | https://github.com |
| PowerSploit | PowerShell post-exploitation/privesc toolkit | https://github.com |
| PEASS-ng (WinPEAS/LinPEAS) | Automated privesc enumeration | https://github.com |
| Seatbelt (GhostPack) | Host security/misconfiguration survey | https://github.com |
| BeRoot | Privilege escalation path checker | — |
| linWinPwn | AD enumeration/exploitation | — |
| PowerView | AD enumeration (PowerShell) | — |
| Traitor / FullPowers | Linux/Windows token & privilege abuse | https://github.com |
| PsExec | Remote process execution (Sysinternals) | https://www.microsoft.com |

### Executing Applications / Remote Access
| Tool | Purpose | Link |
|---|---|---|
| Dameware Remote Support | Remote Windows administration | https://www.solarwinds.com |
| Ninja / Pupy | Remote administration frameworks | https://github.com |
| PDQ Deploy / ManageEngine Endpoint Central | Enterprise remote deployment | vendor sites |

### Keyloggers & Anti-Keyloggers
| Tool | Purpose | Link |
|---|---|---|
| Spyrix Personal Monitor | Software keylogger/monitor | https://www.spyrix.com |
| REFOG, All In One Keylogger, Revealer Keylogger | Windows software keyloggers | vendor sites |
| KeyGrabber | Hardware USB/PS2 keylogger | https://www.keelog.com |
| Zemana AntiLogger | Anti-keylogger | https://zemana.com |
| GuardedID, KeyScrambler, SpyShelter | Anti-keylogger / keystroke encryption | vendor sites |

### Spyware & Anti-Spyware
| Tool | Purpose | Link |
|---|---|---|
| Spytech SpyAgent | Desktop monitoring spyware | https://www.spytech-web.com |
| mSpy, XNSPY, FlexiSPY | Mobile/cellphone spyware | vendor sites |
| SUPERAntiSpyware | Anti-spyware/anti-malware | https://www.superantispyware.com |
| Malwarebytes, Avast One | General anti-malware/anti-spyware | vendor sites |

### Rootkits & Anti-Rootkit
| Tool | Purpose | Link |
|---|---|---|
| GMER | Rootkit scanner | http://www.gmer.net |
| TDSSKiller | Rootkit removal | https://usa.kaspersky.com |
| Malwarebytes Anti-Rootkit | Rootkit removal | https://www.malwarebytes.com |
| Tripwire / AIDE | Integrity-based rootkit detection | — |

### NTFS ADS Detection
| Tool | Purpose | Link |
|---|---|---|
| Sysinternals Streams / LADS | Alternate Data Stream detection | https://learn.microsoft.com |
| StreamArmor | ADS discovery/cleanup | https://securityxploded.com |
| GMER, Stream Detector | ADS/rootkit detection | vendor sites |

### Steganography & Steganalysis
| Tool | Purpose | Link |
|---|---|---|
| OpenStego | Image steganography & watermarking | https://www.openstego.com |
| Snow | Whitespace steganography | https://darkside.com.au |
| StegoStick | Multi-format steganography | https://sourceforge.net |
| DeepSound | Audio steganography | https://jpinsoft.net |
| OmniHide PRO | Video/general steganography | https://omnihide.com |
| Spam Mimic | Spam/email steganography | https://www.spammimic.com |
| zsteg | PNG/BMP stego detection | https://github.com |
| StegoHunt MP | Enterprise steganalysis | https://www.wetstonetech.com |

### Covering Tracks / Anti-Forensics
| Tool | Purpose | Link |
|---|---|---|
| CCleaner | System/browser cleaner | https://www.ccleaner.com |
| BleachBit, DBAN, Privacy Eraser Free | Disk/file wiping | vendor sites |
| Cipher.exe | Built-in Windows secure-delete | — |
| Timestomp / Transmogrify | Timestamp manipulation | — |
| wevtutil / auditpol | Built-in Windows log/audit control | — |

---

## Suggested Study Order

1. Read **01** and **02** together — they are both "Gaining Access."
2. Read **03** — privilege escalation is the natural next step once you have any foothold.
3. Read **04**, **05**, and **06** as a block — they're all "Maintaining Access" in the CHM, just split by technique family.
4. Finish with **07** — covering tracks only makes sense once you understand what's been left behind in 01–06.
5. Keep **CHEATSHEET.md** open in a second tab while doing lab work.

## Lab & Ethics Reminder

Everything in this repo is written for authorized lab environments (your own VMs, CTF platforms, or environments you have explicit written permission to test) and for exam preparation. Running any of these techniques against systems you don't own or don't have permission to test is illegal in most jurisdictions, full stop.
