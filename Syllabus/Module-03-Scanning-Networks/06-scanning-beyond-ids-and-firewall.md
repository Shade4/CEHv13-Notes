# 06 — Scanning Beyond IDS and Firewall

## 6.1 Overview

Intrusion detection systems (IDS) and firewalls exist specifically to stop unauthorized traffic from reaching a network — but they have edges and blind spots, and attackers design their scans specifically to walk along those edges. This file covers the ten evasion techniques the module groups together:

```
Packet Fragmentation │ Source Routing │ Source Port Manipulation │ IP Address Decoy
IP Address Spoofing  │ MAC Address Spoofing │ Creating Custom Packets
Randomizing Host Order & Sending Bad Checksums │ Proxy Servers │ Anonymizers
```

## 6.2 Packet Fragmentation

Splitting a single probe packet into several smaller fragments before sending it. When these fragments reach the target, the IDS/firewall behind it generally has to queue and reassemble *all* of them before it can process any single one — a heavier CPU/memory cost than inspecting one whole packet. Because this reassembly overhead is expensive, many IDS configurations are set to simply skip inspecting fragmented traffic outright, which is exactly the gap fragmentation exploits. Once the fragments reach the actual destination host, its own TCP/IP stack reassembles them back into the original packet.

### SYN/FIN Scanning Using IP Fragments

Not a new scan type — it's a *modification* applied on top of existing scans (see file `04`). Instead of sending one intact TCP header, the header is split across several packets, each containing only 8 octets (64 bits): just enough to carry the source and destination port for the initial fragment. The next fragment's flags allow the remote host to reassemble the pieces correctly, using the field-equivalent values of source, destination, protocol, and identification to recognize which fragments belong together.

```
   Attacker -- SYN/FIN (small IP fragments) + Port(n) -->  Target
   Attacker <--------------- RST (if port closed) --------  Target
```

**Caveats:**
- Some hosts fail to parse/reassemble fragmented packets correctly, which can cause crashes, reboots, or unexpected monitoring-device behavior on the target side — an unintended side effect worth knowing about even in authorized testing.
- Some firewalls have rule sets that explicitly block fragment queues at the kernel level (e.g., `CONFIG_IP_ALWAYS_DEFRAG` on Linux) — though this isn't widely deployed because of its performance cost.
- Because so many IDS rely on **signature-based** detection of scan attempts at the IP/TCP header level, fragmentation frequently slips past that signature matching entirely, causing filtering/detection failures on the target network.

**Nmap syntax:** the `-f` flag enables fragmentation, generally paired with a stealth scan type:
```bash
nmap -sS -T4 -A -f -v 10.10.1.11
```

## 6.3 Source Routing

Every IP datagram carries an **IP options** field, which can store a list of IP addresses defining the exact route a packet must hop through to reach its destination. Normally, each router along the path independently examines the destination IP and picks the next hop itself. **Source routing flips this** — the *originator* (attacker) dictates some or all of that path, deliberately choosing hops that avoid any firewall- or IDS-configured routers, so the packet reaches the destination via an attacker-defined route instead of the "correct" one a defender would expect.

```
        A (Sender)  --X-->  [Firewall]        E
         |                                    |
         v                                    v
         B  ------>  C  ------>  D  -------->  F (Destination)
```
The originator dictates the eventual route of the traffic — bypassing the firewall/IDS-configured router entirely by routing through B → C → D → E instead.

## 6.4 Source Port Manipulation

Rather than manipulating the *path* the packet takes, this manipulates a field the firewall trusts blindly: the **source port number**. Many firewall misconfigurations arise because administrators configure rules that automatically allow traffic claiming to originate from well-known ports (HTTP, DNS, FTP, etc.), assuming that traffic must be legitimate. An attacker simply relabels their actual (arbitrary) source port as one of these trusted values, and the firewall waves it through without further scrutiny.

```
   Attacker (actual port: 242)
        --> manipulated to port: 80 -->  [Firewall]  --allowed--> Victim
   Attacker (actual port: 242, unmanipulated)  -->  [Firewall]  --blocked--
```

**Nmap syntax:** `-g` or `--source-port`
```bash
nmap -g 80 10.10.1.11
```

Even application-level proxies and protocol-parsing firewall elements (which are more resistant to this than simple stateless packet filters) can sometimes still be tricked, depending on configuration — this is fundamentally a misconfiguration/trust problem, not a protocol flaw.

## 6.5 IP Address Decoy

**Nmap syntax:**
```bash
nmap -D RND:10 [target]                              # auto-generate 10 random decoys
nmap -D decoy1,decoy2,decoy3,...,ME,... [target]      # manually specify decoy IPs
```

Nmap's decoy scan cloaks a real scan inside a crowd of fake ones: it generates (or lets you specify) additional spoofed source IP addresses, all of which *appear* to be scanning the target simultaneously. From the target's point of view, its IDS/firewall might log scanning activity from 5–10 different IPs, but it can't tell which of them is the real attacker and which are innocuous decoys.

**Auto-generated decoys:**
```bash
nmap -D RND:10 10.10.10.10
```
Nmap generates a random number of decoy IPs and places the real IP at a random position among them.

**Manually specified decoys**, with optional `ME` keyword to control your real IP's position in the list:
```bash
nmap -D 192.168.0.1,172.120.2.8,192.168.2.8,10.10.1.19,10.10.1.5 10.10.1.11
```
If `ME` is placed 4th in the decoy list, your real IP is positioned 4th in the actual packets sent; omit `ME` and Nmap places your real IP at a random position for you.

Decoys can be layered into both the initial ping scan (ICMP, SYN, ACK, etc.) and the actual port-scanning phase.

**Limitations:** decoy scanning fails against defenders using active countermeasures like router path tracing or selectively dropping suspicious responses — and using too many decoys can slow the scan considerably and reduce its accuracy.

## 6.6 IP Address Spoofing

Most firewalls filter based on source IP, trusting packets from addresses they consider legitimate and blocking ones from illegitimate sources. IP spoofing directly attacks that trust model: the attacker alters packet headers to make traffic *appear* to originate from a different (often trusted) machine, while concealing their real IP.

```
Attacker (sends spoofed packet, claiming address 7.7.7.7)  -->  actually is 7.7.7.7's real machine
Victim IP address 5.5.5.5 receives the spoofed traffic
```

**Critical caveat:** any reply the target sends goes back to the **spoofed** address, not to the attacker — so **a real three-way handshake and a genuine bidirectional TCP session cannot be completed with a spoofed source**. This makes IP spoofing most useful for one-way attacks (like flooding/DoS) rather than anything requiring an actual response.

**When the attacker spoofs a nonexistent address entirely**, the target's reply goes nowhere and the target machine simply hangs waiting on a session that will never respond, until it times out — quietly burning the target's own resources (a mechanism attackers can exploit deliberately for denial-of-service purposes).

**Hping3 syntax:**
```bash
hping3 www.certifiedhacker.com -a 7.7.7.7
```
`-a` sets the spoofed source address for arbitrary crafted TCP/IP packets sent to the target.

## 6.7 MAC Address Spoofing

Network firewalls can also filter based on the source **MAC address**, allowing traffic only from specific known-legitimate hardware addresses. To get around MAC-based ACLs, attackers fake a legitimate MAC address and masquerade as an already-trusted device on the network — Nmap's `--spoof-mac` option handles this directly.

| Command | Effect |
|---|---|
| `nmap -sT -Pn --spoof-mac 0 [Target IP]` | `0` triggers full randomization — Nmap generates a random MAC and attaches it to every packet during the scan |
| `nmap -sT -Pn --spoof-mac [Vendor] [Target IP]` | Spoofs a MAC that matches a specific vendor's OUI prefix (e.g., `Dell`), so the packets look like they came from a legitimate device of that brand — the original MAC never appears in firewall logs |
| `nmap -sT -Pn --spoof-mac [new MAC] [Target IP]` | Manually sets an exact, attacker-chosen MAC address for every packet in the scan |

Example output snippet (vendor-based spoofing):
```
Spoofing MAC address 00:00:97:A2:AE:71 (Dell EMC)
```

This lets an attacker scan in a semi-hidden mode, since the real hardware MAC never shows up in the target's logs.

## 6.8 Creating Custom Packets

### Packet Crafting Tools

Attackers hand-build custom TCP packets to route around firewall inspection entirely, using dedicated packet crafting tools:

- **Colasoft Packet Builder** (https://www.colasoft.com)
- **NetScanTools Pro** (https://www.netscantools.com)

**Colasoft Packet Builder** provides three linked views:
- **Packet List** — every constructed packet; selecting one syncs the Decode Editor and Hex Editor below it.
- **Hex Editor** — raw hex bytes of the packet, with non-printable characters shown as `.` in the ASCII pane; you can edit either the hex or the ASCII side directly.
- **Decode Editor** — a friendlier, field-by-field view (source/destination address, protocol type, hardware/protocol size, sender/target addresses, etc.) that lets you edit a value without needing to know its exact byte offset or length.

New packets are built via `Add`/`Insert` in the Edit menu or Toolbar. Once built, packets can be sent to the wire directly, with the attacker controlling send interval, loop count, and delay between loops. Beyond legitimate network auditing use, this same capability lets an attacker deliberately craft fragmented packets to bypass firewalls/IDS, or flood a victim with a very large volume of custom packets as a DoS technique.

## 6.9 Randomizing Host Order and Sending Bad Checksums

### Randomizing Host Order

**Nmap option:** `--randomize-hosts`

Rather than scanning a target range sequentially (which is an obvious, easy-to-spot pattern for a monitoring system), Nmap shuffles each group of 16,384 hosts before scanning — especially effective when paired with slower timing options, since the scan then reads as noise rather than a clean sweep. For larger randomized groups, `PING_GROUP_SZ` needs to be increased in `nmap.h` and Nmap recompiled. Alternatively: generate the full target list with a list scan (`-sL -n -oN <filename>`), randomize it externally (e.g., a Perl script), and feed the shuffled list back in with `-iL`.

```bash
nmap --randomize-hosts 10.10.1.11
```

### Sending Bad Checksums

**Nmap option:** `--badsum`

TCP/UDP checksums exist to guarantee data integrity — a receiving stack is supposed to silently discard any packet whose checksum doesn't validate. Sending deliberately invalid checksums is a clever probe: **any** response at all tells you the responding system (an IDS or firewall) never actually verified the checksum in the first place — a signature of an improperly configured or naive security device, since a correctly-implemented stack would drop the packet and stay silent.

```bash
nmap --badsum 10.10.1.11
```

## 6.10 Proxy Servers

A **proxy server** is an intermediary application that sits between a client and the destination it's trying to reach, mediating the request/response cycle on the client's behalf.

```
   Attacker  <--->  Proxy Server  <--->  Target Organization
```

Legitimate uses of a proxy: acting as a firewall/local-network shield, IP multiplexing (NAT/PAT — letting many machines share one public IP), light web-surfing anonymization, ad/"unsuitable content" filtering, general hacking-attack protection, and bandwidth savings.

### Why Attackers Use Proxy Servers

- To **hide the actual source** of a scan and evade certain IDS/firewall restrictions
- To hide their source IP so they can operate without immediate legal exposure
- To **mask the actual source** of an attack by impersonating the proxy's own address
- To **remotely access intranets** and other website resources normally off-limits
- To **interrupt all requests** sent by a user, redirecting them to a third destination — so a victim can only ever identify the proxy's address, never the attacker's
- To **chain multiple proxy servers** together to make detection/attribution even harder

Because so many free proxy servers are just a Google search away ("free proxy servers" returns thousands of listings), this technique carries an extremely low barrier to entry.

### Proxy Chaining

Chaining multiplies the anonymity effect: the more proxies in the chain, the harder attribution becomes for a defender trying to trace the traffic back.

```
User -> [Proxy 20.10.10.2:8012] -> [Proxy 10.10.20.5:8023] -> [Proxy 20.10.15.4:8030]
     -> [Proxy 20.15.15.3:8054] -> [Proxy 15.20.15.2:8045] -> [Proxy 10.10.20.8:8028] -> Web Server
```

Each proxy in the chain strips the previous hop's identification info before passing the request to the next proxy; only the final, unencrypted request lands at the web server, which sees only the last proxy in the chain.

### Proxy Tools

| Tool | Source | Notes |
|---|---|---|
| **Proxy Switcher** | https://www.proxyswitcher.com | Lets an attacker surf anonymously via a chain of SOCKS/HTTP/HTTPS proxies without disclosing their real IP; also used to bypass site-level access restrictions |
| **CyberGhost VPN** | https://www.cyberghostvpn.com | Hides the real IP behind a selected replacement, encrypts the connection, and doesn't retain logs |
| Burp Suite | https://www.portswigger.net | |
| Tor | https://www.torproject.org | |
| Hotspot Shield | https://www.hotspotshield.com | |
| Proxifier | https://www.proxifier.com | |
| IPRoyal Residential Proxy | https://iproyal.com | |

## 6.11 Anonymizers

An **anonymizer** is an intermediate server that fetches a website on the user's behalf, making browsing activity untraceable and stripping identifying information (source IP) from all outbound requests. Most anonymizers can handle HTTP, FTP, and Gopher traffic.

**How it's used:** either visit the anonymizer directly and enter the target site's address into an anonymization field, or point the browser's home page permanently at the anonymizer to blanket-anonymize all subsequent browsing. Attackers can also configure an anonymizer as a permanent proxy in an application's HTTP/FTP/Gopher configuration menu — silently cloaking every request the application makes going forward.

### Why Use an Anonymizer?

- **Ensuring privacy** — untraceable navigation, as long as no identifying personal info is manually submitted through forms
- **Accessing government-restricted content** — a citizen can still reach a site blocked domestically by routing through an anonymizer located outside that country
- **Protection against online attacks** — an anonymizer can route customer traffic through its own protected DNS, defending against pharming-style attacks
- **Bypassing IDS and firewall rules** — organizational firewalls only ever see a connection to the anonymizer's own address, never to the actual destination site the user is really browsing to

Anonymizers can equally be used offensively: attacking a website while remaining untraceable.

### Types of Anonymizers

| Type | Mechanism | Advantage | Disadvantage |
|---|---|---|---|
| **Networked** | Routes info through a *chain* of Internet-connected computers before it reaches the destination | Complicates traffic analysis for anyone trying to trace it back | Multi-node communication means confidentiality could be compromised at any single node along the chain |
| **Single-point** | Routes info through *one* intermediary website before it reaches the destination, and passes the response back the same way | Simple, arm's-length communication that hides the IP and identifying info | Offers much weaker resistance to sophisticated traffic analysis than a networked chain |

### Anonymizer / Censorship-Circumvention Tools

| Tool | Source |
|---|---|
| **Whonix** | https://www.whonix.org — a full desktop OS built for advanced security/privacy; routes everything through Tor via a heavily reconfigured Debian base run inside multiple VMs, providing strong protection from malware and IP leaks |
| **AstrillVPN** | https://www.astrill.com — bypasses censorship, accesses geo-blocked content, encrypts traffic, and avoids logging DNS queries/traffic |
| **Tails** | https://tails.net — a live OS run from a USB stick/SD card; uses cryptographic tools to encrypt files, email, and IM, leaves no trace on the host computer |
| Psiphon | https://psiphon.ca |
| TunnelBear | https://www.tunnelbear.com |
| Invisible Internet Project (I2P) | https://geti2p.net |
| Bright Data Proxy API | https://brightdata.com |

---

**Next:** [`07-network-scanning-countermeasures.md`](07-network-scanning-countermeasures.md) — the defensive side of everything covered so far.
