# 06 — Evasion and Bypass Techniques

[⬅ Back to main index](../README.md)

This section covers every technique an attacker uses to bypass or evade network security controls. It is split into three focused sub-files to keep each one readable:

| Sub-section | Topics |
|---|---|
| [06a — Firewall Evasion](./06a-firewall-evasion/README.md) | Port scanning, firewalking, banner grabbing, IP spoofing, source routing, tiny fragments, IP-based bypass, anonymizers, proxy bypass, ICMP tunneling, ACK tunneling, HTTP tunneling (HTTPort/HTTHost), SSH tunneling (OpenSSH + Bitvise), DNS tunneling (iodine/dnscat2), external systems bypass, MITM/DNS poisoning, malicious content delivery, XSS/WAF bypass, HTML smuggling, Windows BITS evasion |
| [06b — IDS Evasion](./06b-ids-evasion/README.md) | Insertion attack, evasion, DoS against IDS, obfuscating, false positive generation, session splicing, unicode evasion, fragmentation attacks, TTL attacks, urgency flag, invalid RST packets, polymorphic shellcode, ASCII shellcode, application-layer attacks, desynchronization (pre/post SYN), domain generation algorithms (DGA), encryption, flooding |
| [06c — NAC and Endpoint Security Evasion](./06c-nac-and-endpoint-evasion/README.md) | VLAN hopping (VLANPWN), pre-authenticated device bypass (nac_bypass_setup.sh, FENRIR), ghostwriting, DLL hijacking/application whitelisting, dechaining macros (all VBScript techniques), clearing memory hooks (x64dbg), process injection (Windows API), LoLBins, CPL sideloading, ChatGPT-assisted malware, Metasploit template modification, Windows AMSI bypass, and 10+ advanced EDR evasion techniques |

> Educational purpose only. This content mirrors the EC-Council CEH v13 curriculum for Module 12. Understanding these techniques is essential for defenders to recognize and counter them. Never apply these techniques against systems or networks you do not own or have explicit written authorization to test.

---

[⬅ Back to main index](../README.md) · [➡ 06a: Firewall Evasion](./06a-firewall-evasion/README.md)
