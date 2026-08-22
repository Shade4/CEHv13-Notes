# Cheatsheet — Scanning Networks (Nmap / Hping3 Quick Reference)

One-page command reference. See the numbered files for full explanations of *why* each command works.

## Host Discovery (`nmap -sn ...`)

| Technique | Command |
|---|---|
| ARP ping scan | `nmap -sn -PR <target>` |
| UDP ping scan | `nmap -sn -PU <target>` |
| ICMP ECHO ping | `nmap -sn -PE <target>` |
| ICMP ECHO ping sweep | `nmap -sn -PE <IP range>` |
| ICMP timestamp ping | `nmap -sn -PP <target>` |
| ICMP address mask ping | `nmap -sn -PM <target>` |
| TCP SYN ping | `nmap -sn -PS <target>` (or `-PS22-25,80,113,1050,35000`) |
| TCP ACK ping | `nmap -sn -PA <target>` |
| IP protocol ping | `nmap -sn -PO <target>` |
| Disable Nmap's default ARP ping | `nmap --disable-arp-ping ...` |

## Port & Service Scanning

| Technique | Command |
|---|---|
| TCP Connect / full-open scan | `nmap -sT -v <target>` |
| Stealth / half-open (SYN) scan | `nmap -sS -v <target>` |
| Xmas scan (FIN+URG+PSH) | `nmap -sX -v <target>` |
| FIN scan | `nmap -sF -v <target>` |
| NULL scan (no flags) | `nmap -sN -v <target>` |
| TCP Maimon scan (FIN/ACK) | `nmap -sM -v <target>` |
| ACK flag probe scan | `nmap -sA -v <target>` |
| TTL-based ACK probe | `nmap --ttl [time] [target]` |
| Window-based ACK probe (Window scan) | `nmap -sW -v <target>` |
| IDLE / IPID header (zombie) scan | `nmap -Pn -p<port> -sI <zombie> <target>` |
| UDP scan | `nmap -sU -v <target>` |
| SCTP INIT scan | `nmap -sY <target>` |
| SCTP COOKIE ECHO scan | `nmap -sZ -v <target>` |
| List scan (no packets sent) | `nmap -sL -v <target>` |
| IPv6 scan | `nmap -6 <target/domain>` |
| Service/version detection | `nmap -sV <target>` |
| OS detection | `nmap -O <target>` |
| Full aggressive scan (all ports) | `nmap -p 1-65535 -T4 -A -v <target>` |
| Show reason for port state | `nmap -sV --reason -v -sT <target>` |

## IDS/Firewall Evasion

| Technique | Command |
|---|---|
| Packet fragmentation | `nmap -f <target>` (combine with `-sS -T4 -A -v`) |
| Source port manipulation | `nmap -g 80 <target>` or `--source-port 80` |
| Decoy scan (auto-generate) | `nmap -D RND:10 <target>` |
| Decoy scan (manual list) | `nmap -D decoy1,decoy2,ME,... <target>` |
| MAC spoof — full random | `nmap -sT -Pn --spoof-mac 0 <target>` |
| MAC spoof — by vendor | `nmap -sT -Pn --spoof-mac Dell <target>` |
| MAC spoof — exact address | `nmap -sT -Pn --spoof-mac 00:01:02:25:56:AE <target>` |
| Randomize host scan order | `nmap --randomize-hosts <target>` |
| Send bad checksums (test filtering) | `nmap --badsum <target>` |
| IP spoofing (Hping3) | `hping3 <target> -a <spoofed-ip>` |

## Hping3 Reference

| Purpose | Command |
|---|---|
| ICMP ping | `hping3 -1 <target>` |
| ACK scan on port 80 | `hping3 -A <target> -p 80` |
| UDP scan on port 80 | `hping3 -2 <target> -p 80` |
| Collect TCP sequence numbers | `hping3 <target> -Q -p <port>` |
| TCP timestamp / firewall test | `hping3 -S <target> -p 80 --tcp-timestamp` |
| SYN scan across a port range | `hping3 -8 50-60 -S <target> -V` |
| FIN+PUSH+URG scan | `hping3 -F -P -U <target> -p 80` |
| Ping-sweep a subnet | `hping3 -1 10.0.1.x --rand-dest -I eth0` |
| Passive HTTP sniff (listen mode) | `hping3 -9 HTTP -I eth0` |
| SYN flood (DoS — authorized testing only) | `hping3 -S <target> -a <spoofed-src> -p 22 --flood` |
| IP spoofing | `hping3 <target> -a <spoofed-ip>` |

## Nmap Scripting Engine (NSE)

| Purpose | Command |
|---|---|
| Run default script set | `nmap -sC <target>` |
| Run a specific script | `nmap --script <script-name>.nse <target>` |
| OS discovery via SMB | `nmap --script smb-os-discovery.nse <target>` |
| IPv6 fingerprinting | `nmap -6 -O <target>` |

## Metasploit Quick Reference

```
msf6 > search portscan
msf6 > use auxiliary/scanner/portscan/tcp
msf6 auxiliary(scanner/portscan/tcp) > set RHOSTS <target>
msf6 auxiliary(scanner/portscan/tcp) > run
```

One-liner (non-interactive):
```bash
msfconsole -q -x "use auxiliary/scanner/portscan/tcp; set RHOSTS <target>; run; exit"
```

## Chained Automation Pattern (Discover → Scan → Report)

```bash
#!/bin/bash
nmap -sn <CIDR> -oG - | awk '/Up$/{print $2}' > live_hosts.txt &&
nmap -iL live_hosts.txt -sV -oA scan_results &&
cat scan_results.nmap
```

## OS Fingerprint Signature Table (Passive)

| OS | TTL | TCP Window Size |
|---|---|---|
| Linux | 64 | 5,840 |
| FreeBSD | 64 | 65,535 |
| OpenBSD | 255 | 16,384 |
| Windows | 128 | 65,535 – 1 GB |
| Cisco Routers | 255 | 4,128 |
| Solaris | 255 | 8,760 |
| AIX | 255 | 16,384 |

## TCP Flags Quick Reference

| Flag | Meaning |
|---|---|
| SYN | Start connection / announce new sequence number |
| ACK | Acknowledge receipt |
| PSH | Push buffered data to the application now |
| URG | Process data urgently, ahead of the queue |
| FIN | Graceful connection close |
| RST | Abort connection / reject |

---

*Companion cheatsheet to the [`CEH-Module-03-Scanning-Networks`](README.md) study repo.*
