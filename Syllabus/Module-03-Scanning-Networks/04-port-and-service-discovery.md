# 04 — Port and Service Discovery

## 4.1 Overview

Once you know a host is alive (file `03`), the next question is: **which ports are open, and what's listening on them?** This is the step administrators use to audit their own exposure and attackers use to find a way in. Sometimes users unknowingly leave unnecessary ports open — an attacker takes advantage of exactly that carelessness.

## 4.2 Common Ports and Services (Reference Table)

The reserved/well-known ports referenced throughout the module and its labs:

| Port/Protocol | Name | Description |
|---|---|---|
| 7/tcp,udp | echo | |
| 9/tcp,udp | discard | sink null |
| 11/tcp | systat | Users |
| 13/tcp,udp | daytime | |
| 15/tcp,udp | netstat | |
| 17/tcp,udp | qotd | Quote of the day |
| 19/tcp,udp | chargen | ttytst source |
| 20/tcp | ftp-data | FTP data transfer |
| 21/tcp | ftp | FTP command |
| 22/tcp | ssh | Secure Shell |
| 23/tcp | telnet | |
| 25/tcp | SMTP | Email server |
| 37/tcp,udp | time | Timeserver |
| 39/tcp,udp | rlp | Resource location |
| 53/tcp,udp | domain | Domain name server |
| 66/tcp,udp | sql*net | Oracle SQL*net |
| 67/udp | bootps | Bootp server |
| 68/udp | bootpc | Bootp client |
| 69/udp | tftp | Trivial File Transfer |
| 70/tcp | gopher | Gopher server |
| 79/tcp | finger | Finger |
| 80/tcp,udp | www-http | WWW |
| 88/tcp,udp | kerberos | Kerberos |
| 109/tcp | pop2 | PostOffice v.2 |
| 110/tcp | pop3 | PostOffice v.3 |
| 111/tcp,udp | sunrpc | RPC 4.0 portmapper |
| 113/tcp,udp | auth/ident | Authentication Service |
| 114/tcp,udp | audionews | Audio News Multicast |
| 119/tcp | nntp | Usenet News Transfer |
| 123/udp | ntp | Network Time Protocol |
| 137/tcp,udp | netbios-ns | NetBIOS Name Service |
| 138/tcp,udp | netbios-dgm | NetBIOS Datagram Service |
| 139/tcp,udp | netbios-ssn | NetBIOS Session Service |
| 143/tcp,udp | imap | Internet Message Access Protocol |
| 150/tcp,udp | sql-net | SQL-NET |
| 156/tcp,udp | sqlsrv | SQL Service |
| 161/tcp,udp | snmp | SNMP |
| 162/tcp,udp | snmp-trap | |
| 163/tcp,udp | cmip-man | CMIP/TCP Manager |
| 164/tcp,udp | cmip-agent | CMIP/TCP Agent |
| 194/tcp,udp | irc | Internet Relay Chat |
| 201–208/tcp,udp | at-* | AppleTalk (routing, name binding, echo, zone info, etc.) |
| 213/tcp,udp | ipx | Novell |
| 220/tcp,udp | imap3 | Interactive Mail Access Protocol v3 |
| 387/tcp,udp | aurp | AppleTalk Update-Based Routing |
| 396/tcp,udp | netware-ip | Novell Netware over IP |
| 411/tcp,udp | rmt | Remote mt |
| 445/tcp,udp | kerberos-ds | Microsoft DS |
| 500/udp | isakmp | ISAKMP/IKE |
| 510/tcp | fcp | First Class Server |
| 512/tcp | exec | BSD rexecd(8) |
| 512/udp | comsat/biff | Mail-notification |
| 513/tcp | login | BSD rlogind(8) |
| 513/udp | who | whod BSD rwhod(8) |
| 514/tcp | shell | cmd BSD rshd(8) |
| 514/udp | syslog | BSD syslogd(8) |
| 515/tcp,udp | printer | spooler BSD lpd(8) |
| 517/tcp,udp | talk | BSD talkd(8) |
| 518/udp | ntalk | SunOS talkd(8) |
| 532/tcp,udp | netnews | Readnews |
| 540/tcp,udp | uucp | uucpd BSD uucpd(8) |
| 543/tcp,udp | klogin | Kerberos Login |
| 544/tcp,udp | kshell | Kerberos Shell |
| 545/tcp | ekshell | Kerberos encrypted remote shell — kfall |
| 600/tcp | pcserver | ECD Integrated PC board srvr |
| 635/udp | mount | NFS Mount Service |
| 640/udp | pcnfs | PC-NFS DOS Authentication |
| 650/udp | bwnfs | BW-NFS DOS Authentication |
| 744/tcp,udp | flexlm | Flexible License Manager |
| 749/tcp,udp | kerberos-adm | Kerberos Administration |
| 750/tcp,udp | kerberos | kdc Kerberos authentication |
| 751/tcp,udp | kerberos_master | Kerberos authentication |
| 754/tcp | krb_prop | Kerberos slave propagation |
| 999/udp | applix | Applixware |
| 1080/tcp,udp | socks | SOCKS Proxy |
| 1109/tcp | kpop | Pop with Kerberos |
| 1433/tcp,udp | ms-sql-s | Microsoft SQL Server |
| 1434/tcp,udp | ms-sql-m | Microsoft SQL Monitor |
| 1723/tcp,udp | pptp | Pptp |
| 2049/tcp,udp | nfs | Network File System |
| 2105/tcp | eklogin | Kerberos encrypted rlogin |
| 2108/tcp | rkinit | Kerberos remote kinit |
| 2111/tcp | kx | X over Kerberos |
| 2120/tcp | kauth | Remote kauth |
| 4894/tcp | lyskom | LysKOM (conference system) |
| 5060/tcp,udp | sip | Session Initiation Protocol |
| 6000–6063/tcp,udp | x11 | X Window System |
| 6667/tcp | irc | Internet Relay Chat |

## 4.3 Port Scanning Techniques — The Full Taxonomy

Port scanning techniques are categorized by the transport protocol used for communication:

```
Port and Service Discovery Techniques
│
├── TCP Scanning
│   ├── Open TCP Scanning Methods
│   │   └── TCP Connect / Full-Open Scan     nmap -sT -v <Target IP>
│   ├── Stealth TCP Scanning Methods
│   │   ├── Half-Open Scan                   nmap -sS -v <Target IP>
│   │   ├── Inverse TCP Flag Scan
│   │   │   ├── Xmas Scan                    nmap -sX -v <Target IP>
│   │   │   ├── FIN Scan                     nmap -sF -v <Target IP>
│   │   │   ├── NULL Scan                    nmap -sN -v <Target IP>
│   │   │   └── Maimon Scan                  nmap -sM -v <Target IP>
│   │   └── ACK Flag Probe Scan
│   │       ├── TTL-Based Scan               nmap -sA --ttl 100 -v <Target IP>
│   │       └── Window-Based Scan            nmap -sW -v <Target IP>
│   └── Third-Party and Spoofed TCP Scanning Methods
│       └── IDLE / IPID Header Scan          nmap -Pn -p<port> --si <Zombie> <Target>
├── UDP Scanning                             nmap -sU -v <Target IP>
├── SCTP Scanning
│   ├── SCTP INIT Scanning                   nmap -sY <Target IP>
│   └── SCTP COOKIE/ECHO Scanning            nmap -sZ -v <Target IP>
├── SSDP and List Scanning
└── IPv6 Scanning                            nmap -6 <Target IP/Domain>
```

### 4.3.1 TCP Connect / Full-Open Scan

**Syntax:** `nmap -sT -v <Target IP>`

The most reliable form of TCP scanning: it uses the OS's own `connect()` system call to actually open a connection to every port of interest. A successful connection means the port is listening; an error means it isn't reachable.

```
   Attacker -- SYN Packet + Port(n) -->  Target
   Attacker <--- SYN + ACK Packet -----  Target
   Attacker -------- ACK -------------->  Target      → PORT OPEN
   Attacker <-------- RST --------------  Target       (scanner tears it down)
```
```
   Attacker -- SYN Packet + Port(n) -->  Target
   Attacker <----------- RST -----------  Target       → PORT CLOSED
```

Because a full three-way handshake completes, this scan is **easily detectable and filterable** — the connection shows up in the target's own connection logs just like a legitimate client. It doesn't require superuser/raw-socket privileges (unlike most of the scans below), which is its main practical advantage. To make many sequential `connect()` calls fast, the attacker parallelizes with many sockets and short, non-blocking timeouts rather than looping one port at a time.

### 4.3.2 Stealth Scan / Half-Open Scan (SYN scan)

**Syntax:** `nmap -sS -v <Target IP>`

Also called a "SYN scan" because it only ever sends the SYN packet. The handshake is deliberately reset before completion:

```
Client sends a single SYN → port open  ⇒ server replies SYN/ACK  ⇒ client sends RST (never ACK)
Client sends a single SYN → port closed ⇒ server replies RST directly
```

Because the connection never fully opens, many logging mechanisms that only trigger on completed connections **never see it** — hence "stealth." It still implements handshake logic on paper, but bails out before the final step. This is the default and most popular Nmap scan type for a reason: it's fast, avoids the most naive connection logging, and works reliably against standards-compliant stacks.

### 4.3.3 Inverse TCP Flag Scan

Rather than SYN, these send probe packets with an unusual TCP flag configuration (or *no* flags at all) and interpret the target's (non-)response:

- **Open port:** no response at all
- **Closed port:** an RST comes back

```
   Attacker -- Probe (FIN / URG / PSH / NULL) -->  Target      (open: no response)
   Attacker <--------------- RST/ACK -------------  Target      (closed)
```

This works because RFC 793 says a closed port must respond to an unexpected segment with RST — but an **open** port is allowed to just silently drop packets that don't have SYN or ACK set. **Windows TCP/IP stacks famously ignore RFC 793 on this point and don't reliably send the expected RST for closed ports**, so these techniques mostly only work cleanly against UNIX/BSD-derived stacks.

| Variant | Flags set | Syntax |
|---|---|---|
| **FIN scan** | FIN only | `nmap -sF -v <Target IP>` |
| **Xmas scan** | FIN + URG + PSH ("lit up like a Christmas tree") | `nmap -sX -v <Target IP>` |
| **NULL scan** | none | `nmap -sN -v <Target IP>` |
| **SYN/ACK probe** | (used in ACK-probe scans below, not strictly "inverse") | — |

**Xmas scan** in detail:
```
   Attacker -- FIN+URG+PSH -->  Server:23  (open)   → no response
   Attacker -- FIN+URG+PSH -->  Server:23  (closed) → RST
```
The name comes from all three flags being "lit" at once. It's good for scanning large networks quickly and figuring out which hosts respond to which flag sets, but relies entirely on RFC 793-compliant behavior — **it does not work against any current version of Microsoft Windows**, since Windows shows all ports as "open" regardless of actual state under this technique. This is purely BSD-networking-code behavior and never supported Windows NT or later.

**Advantages of inverse-flag scans generally:** avoids many IDS/logging systems; highly stealthy.
**Disadvantages:** needs raw socket access (superuser privileges); mostly only effective against BSD-derived TCP/IP stacks.

**TCP Maimon scan:**

**Syntax:** `nmap -sM -v <Target IP>`

Very similar to NULL/FIN/Xmas, but the probe used is **FIN/ACK**. Normally a target should respond with RST regardless of port state, but on many BSD systems the packet is simply dropped when the port is open:

- **Open (or filtered):** no response even after retransmissions → Nmap reports `open|filtered`
- **Closed:** RST packet
- **Filtered:** ICMP unreachable error (type 3, code 1, 2, 3, 9, 10, or 13)

```
Attacker -- FIN/ACK Probe -->  Target   (open: no response)
Attacker -- FIN/ACK Probe -->  Target   (closed: RST packet)
Attacker -- FIN/ACK Probe -->  Target   (filtered: ICMP unreachable error)
```

### 4.3.4 ACK Flag Probe Scan

**Syntax (generic):** `nmap -sA -v <Target IP>`

Sends TCP probe packets with the ACK flag set and analyzes the RST response's header fields (TTL, WINDOW) to infer port state — exploiting quirks specific to BSD-derived TCP/IP stacks. Two sub-variants:

**TTL-Based ACK Flag Probe**

Send thousands of ACK probes across different ports, then compare the **TTL field** of each RST reply.
```bash
nmap --ttl [time] [target]
```
```
1: host 10.2.2.11 port 20: F:RST -> ttl: 80 win: 0
2: host 10.2.2.11 port 21: F:RST -> ttl: 80 win: 0
3: host 10.2.2.11 port 22: F:RST -> ttl: 50 win: 0   <-- anomaly = OPEN
4: host 10.2.2.11 port 23: F:RST -> ttl: 80 win: 0
```
Port 22 returned a noticeably lower TTL (50) than the boundary/majority value (80, > 64) — that's the tell for an open port.

**Window-Based ACK Flag Probe**

**Syntax:** `nmap -sW -v <Target IP>`

Same idea, but examine the **WINDOW field** of the RST replies instead — useful when all replies happen to share the same TTL (so TTL-based analysis can't distinguish anything).
```
1: host 10.2.2.12 port 20: F:RST -> ttl: 64 win: 0
2: host 10.2.2.12 port 21: F:RST -> ttl: 64 win: 0
3: host 10.2.2.12 port 22: F:RST -> ttl: 64 win: 512   <-- non-zero = OPEN
4: host 10.2.2.12 port 23: F:RST -> ttl: 64 win: 0
```
A **non-zero** window value on the RST indicates an open port; a **zero** window value indicates closed. If there's no response after many retransmissions and an ICMP unreachable (type 3, code 1/2/3/9/10/13) comes back instead, the port is inferred **filtered**.

**Advantage:** can evade many IDS in typical configurations.
**Disadvantage:** slow, and only reliably exploits older BSD-derived TCP/IP stacks — not universally applicable.

**Checking firewall filtering with ACK probes:** send an ACK probe with a random sequence number:
- **No response** → a stateful firewall is present (it's dropping unsolicited ACKs)
- **RST response** → no firewall filtering that packet

### 4.3.5 IDLE / IPID Header Scan

**Syntax:** `nmap -Pn -p<port> -sI <Zombie IP> <Target IP>` (Zenmap uses `-sI`)

The most indirect scan in the whole module — a fully blind scan that never sends a single packet from the attacker's real IP to the target. It relies on impersonating a third, largely idle host (the "**zombie**") via IP spoofing, and reading the **IPID** (IP Identification) field — a value every OS increments by one for each packet it sends — to infer what happened on the wire.

**Choosing a zombie:** you want a host that (a) is mostly idle (so its IPID increments predictably, driven only by your probes) and (b) assigns IPIDs incrementally/globally. Shorter round-trip time between attacker↔zombie and zombie↔target means a faster scan.

**Step 1 — baseline the zombie's IPID:**
```
Attacker -- SYN+ACK probe -->  Zombie
Attacker <-- RST (IPID=31337) -  Zombie      (unsolicited SYN/ACK ⇒ zombie sends RST)
```
The zombie wasn't expecting a SYN/ACK, so it denies the phantom connection with an RST — and that RST carries the zombie's current IPID, which we record as **X = 31337**.

**Step 2 — send a spoofed SYN to the real target, using the zombie's IP as source:**

*If the target port is open:*
```
Attacker -- SYN (spoofed as Zombie) -->  Target:80
Target -- SYN+ACK -->  Zombie                     (Zombie didn't ask for this either)
Zombie -- RST (IPID = 31338) -->  Target          (zombie's IPID bumps by 1: X+1)
```
*If the target port is closed:* the target replies to the spoofed SYN with a plain RST straight back to the zombie, and the zombie — having no reason to respond to an unsolicited RST — stays silent. Its IPID doesn't move.

**Step 3 — re-probe the zombie's IPID, exactly like step 1:**
```
Attacker -- SYN+ACK probe -->  Zombie
Attacker <-- RST (IPID=31339) -  Zombie
```
- If the target port was **open**, the zombie sent one extra packet in step 2, so the IPID has now advanced by **2** total (X → X+2) since the original baseline.
- If the target port was **closed**, the zombie sent nothing extra, so the IPID only advanced by **1** (the increment from this very probe).

By comparing final IPID against the original baseline, the attacker learns the target's port state **without the target ever seeing the attacker's real IP** — every packet the target receives appears to come from the zombie.

**Why it matters:** this is complete blind/third-party scanning — extremely hard to attribute, since the logs at the target only implicate the innocent zombie machine.

### 4.3.6 UDP Scan

**Syntax:** `nmap -sU -v <Target IP>`

UDP has no handshake, so there's nothing to "half-complete" — the logic here is inverted relative to TCP scans:

```
Attacker -- "Are you open on UDP Port 29?" -->  Server
   → No response                                  = OPEN (or filtered — ambiguous)
   → ICMP Port Unreachable message                = CLOSED
```

**Why UDP scanning is inherently harder and slower than TCP scanning:**
- Open ports usually send nothing back at all — "no response" is used as a positive signal, which is inherently ambiguous with packet loss or filtering.
- Closed ports return `ICMP_PORT_UNREACH`. Because ICMP error generation is rate-limited by most stacks (per RFC 1812 §4.3.2.8), scanning speed is capped: the tool has to throttle its own probes or it'll blow past the target's ICMP rate limit and start mis-reading dropped-for-rate-limit as open.
- Retransmission is required for any probe/response the scanner suspects was simply lost in transit rather than deliberately filtered.
- Root access is required to read raw ICMP unreachable messages directly; non-root users can sometimes infer state indirectly via a second `write()` call to a closed port failing, or via non-blocking `recvfrom()` calls returning `EAGAIN`/`ECONNREFUSED` (tools like Netcat and Pluvial's `pscan.c` use this "UDP recvfrom()/write() scanning" trick).

**Advantage:** No TCP-handshake overhead, and Windows-based hosts in particular tend not to implement aggressive ICMP rate limiting, so UDP scans often run efficiently against them.
**Disadvantage:** port info only — pair with `-sV` (version scan) or `-O` (OS fingerprint) for anything beyond open/closed. Most networks carry vastly more TCP than UDP traffic, which further limits how much useful signal a UDP scan turns up — but the ports it does find (spyware, trojans, and other malware love unfiltered UDP) are disproportionately valuable to a security review.

### 4.3.7 SCTP Scanning

**Stream Control Transmission Protocol (SCTP)** is a reliable, message-oriented transport-layer protocol — an alternative to TCP/UDP, purpose-built for multi-homing and multi-streaming. Common SCTP use cases: VoIP, IP telephony, SS7/SIGTRAN signaling services. Its association setup is a **four-way handshake**:

```
   Client (Bob)                          Server (Clara)
      |-------------- INIT --------------->|
      |<------------ INIT-ACK -------------|
      |------------ COOKIE-ECHO ---------->|
      |<------------ COOKIE-ACK -----------|
```

**SCTP INIT Scan**

**Syntax:** `nmap -sY <Target IP>`

Analogous to a TCP SYN scan — fast (thousands of ports/sec on an unobstructed link) and stealthy, since it never completes a full SCTP association.

```
Attacker -- INIT chunk -->  Target   (listening/open: INIT+ACK chunk returned)
Attacker -- INIT chunk -->  Target   (not listening/closed: ABORT chunk returned)
```
No response after retransmissions, or an ICMP unreachable (type 3, code 0/1/2/3/9/10/13), means **filtered**.

**Advantage:** clearly differentiates open, closed, and filtered states.

**SCTP COOKIE ECHO Scan**

**Syntax:** `nmap -sZ -v <Target IP>`

A more advanced/stealthier variant. Instead of an INIT chunk, it sends a COOKIE ECHO chunk directly:
```
Attacker -- COOKIE ECHO chunk -->  Target   (port open: packet silently dropped, no response)
Attacker -- COOKIE ECHO chunk -->  Target   (port closed: ABORT chunk returned)
```
Because non-stateful firewall rule sets designed around blocking INIT chunks don't touch COOKIE ECHO, this evades the exact defenses that catch an INIT scan — only an advanced/stateful IDS can detect it.

**Advantage:** less conspicuous than an INIT scan.
**Disadvantage:** cannot cleanly distinguish open from filtered — both report as `open|filtered`.

### 4.3.8 SSDP and List Scan

**SSDP Scan**

Simple Service Discovery Protocol communicates with machines over routable IPv4/IPv6 multicast addresses, controlling Universal Plug and Play (UPnP) discovery. It generally works even through firewalls, since it's designed to "just work" for consumer devices. Attackers scan for SSDP/UPnP endpoints specifically to hunt for exploitable buffer-overflow or DoS conditions in UPnP implementations — e.g., via a Metasploit module like `auxiliary/scanner/upnp/ssdp_msearch`, configuring `RHOSTS`/`RPORT`/`THREADS` and running against a target.

**List Scan**

**Syntax:** `nmap -sL -v <Target IP>`

Doesn't ping or scan anything at all — it's purely a "sanity check" that generates and prints a list of the IPs/names Nmap *would* target, performing reverse-DNS resolution on each by default. Every listed address is reported as "not scanned" (0 hosts up).

**Advantages:** confirms your target list/CIDR range is what you think it is before running an actual (and possibly loud/slow) scan; catches malformed IP ranges early.

### 4.3.9 IPv6 Scan

**Syntax:** `nmap -6 <Target IP/Domain>`

IPv6 expands the address space from 32 bits to 128 bits, which makes traditional brute-force scanning across a subnet computationally infeasible — a /64 subnet alone offers 2⁶⁴ possible addresses. At one probe per second, an exhaustive scan of that space would take roughly **5 billion years**. Many scanning tools also simply don't support ping sweeps over IPv6 at all.

Because of this, attackers pivot to harvesting real IPv6 addresses from other sources instead of guessing: sniffed network traffic, log files, "Received from" headers in archived email/Usenet posts, or DNS records — then port-scanning those specific known-good addresses. If an attacker compromises one host on a subnet, they can also probe the "all-nodes" link-local multicast address or any predictable/sequential addressing scheme in use.

```bash
nmap -6 scanme.nmap.org
```
```
Nmap scan report for scanme.nmap.org (2600:3c01::f03c:91ff:fe18:bb2f)
PORT      STATE  SERVICE
22/tcp    open   ssh
80/tcp    open   http
31337/tcp open   Elite
```

## 4.4 Port Scanning with AI

The same "translate intent → command" pattern from file `02` applies to port scanning: prompts like *"Use Nmap to find open ports on target IP 10.10.1.11"*, *"Perform stealth scan on target IP 10.10.1.11 and display the results"*, and *"Perform an XMAS scan on target IP 10.10.1.11"* get turned into `nmap -sn 10.10.1.11`-style commands and executed via a shell-driving AI wrapper, with output parsed and summarized back to the user.

A more advanced chained example — scan a list of IPs, then extract just port/service/version info to a new file:
```bash
nmap -sV -iL scan1.txt --open | awk '/Nmap scan report for/{ip=$NF}/^[0-9]+\/tcp/{print ip " : " $0}' > scan3.txt
```
- `-sV -iL scan1.txt` — version-scan every host listed in `scan1.txt`
- `--open` — only show open ports
- the `awk` pipeline tracks the current host's IP from the "Nmap scan report for" line and prefixes each subsequent open-port line with it
- output redirected to `scan3.txt` for later analysis

This same pattern also drives Metasploit from natural language:
```bash
msfconsole -q -x "use auxiliary/scanner/portscan/tcp; set RHOSTS 10.10.1.22; run; exit"
```

## 4.5 Service Version Discovery

**Syntax:** `nmap -sV <Target IP>`

Every open port is generally tied to one specific service, and every service has its own version. Weak/outdated versions of common protocols are exactly what lets an attacker map a discovered port straight to a known CVE. Version detection works by examining responses from the **`nmap-service-probes`** database — a set of queries and matching expressions Nmap sends to each open port, comparing the response against known service signatures.

Combined example — scan open ports, MAC info, and service versions with the reason for each state:
```bash
nmap -sV --reason -v -sT 10.10.1.11
```
- `-sV` — version detection
- `--reason` — show *why* Nmap thinks a port is in a given state (e.g., `syn-ack`)
- `-sT` — TCP connect scan
- `-v` — verbose

## 4.6 Nmap Scan Time Reduction Techniques

Because Nmap treats both performance and accuracy as high priorities, a slow scan is almost always a symptom of one of these being fixable:

- **Omit non-critical tests** — skip an intense/full scan if you only need minimal info; limit the port range scanned; skip `-sn` if you already know hosts are up; avoid stacking `-sC`, `-sV`, `-O`, `--traceroute`, and `-A` unless you actually need all of them; only enable DNS resolution when necessary.
- **Optimize timing parameters** — the `-T` option ranges from high-aggressiveness to low-aggressiveness timing templates; useful for tuning against heavily filtered/rate-limited networks.
- **Separate and optimize UDP scans** — UDP has fundamentally different performance/timing characteristics (see 4.3.6) and is more affected by ICMP rate limiting than TCP, so scan it as its own pass rather than bundling it in with TCP scanning.
- **Upgrade Nmap** — newer releases bring bug fixes, algorithmic improvements, and performance features (e.g., faster local ARP scanning).
- **Execute concurrent Nmap instances** — running one Nmap process against an entire large network tends to be slower and less efficient than dividing the target list into smaller groups and running several instances in parallel.
- **Scan from a favorable network location** — running from inside the target's local network (when legitimately authorized, e.g., an internal pentest) is faster and offers defense-in-depth insight; external scanning is mandatory when specifically testing firewall behavior or evaluating exposure from an outside attacker's perspective.
- **Increase available bandwidth and CPU time** — a new data line, freed-up CPU (close unrelated running applications), and Nmap's own congestion-control algorithms (which prevent network flooding and thereby improve result accuracy) all reduce total scan time; you can gauge current bandwidth usage by running Nmap in verbose mode (`-v`).

---

**Next:** [`05-os-discovery-banner-grabbing.md`](05-os-discovery-banner-grabbing.md) — once you know the open ports, figure out what OS is behind them.
