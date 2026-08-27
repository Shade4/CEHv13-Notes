# 06 — DoS/DDoS Attack Tools

> Exam objective: *Demonstrate different DoS/DDoS attack techniques* (tooling subset)

> ⚠️ The tools below are documented here **for recognition, detection, and defensive purposes
> only** — so you can identify their signatures in traffic captures and logs. Running any of them
> against a system you don't own or don't have signed authorization to test is illegal. If you
> want hands-on practice, do it against your own isolated lab VMs only (see
> [`10-dos-ddos-resilience-testing.md`](10-dos-ddos-resilience-testing.md) for a safe, authorized
> testing methodology).

## 6.1 ISB ("I'm So Bored")

- **Source:** https://sourceforge.net

A Windows GUI utility that lets an attacker perform **HTTP, UDP, TCP, and ICMP flood** attacks
against a target network. Beyond the flood modules themselves, ISB conveniently bundles one-click
access to common network reconnaissance commands — **WHOIS, netstat, traceroute, ping** — to help
an attacker profile the target before attacking. Its interface reports live stats (connected
sockets, packets sent, responses, failures) so the operator can watch the attack's effect in real
time.

## 6.2 UltraDDOS-v2

- **Source:** https://sourceforge.net

A minimal-effort DDoS tool with a simple GUI: the operator enters a target IP address/website,
port number, and the number of packets to transmit, then starts the flood. Its simplicity (one
dialog box, one "OK" button) is precisely what makes it dangerous in unskilled hands — no
networking knowledge is required to launch an attack.

## 6.3 High Orbit Ion Cannon (HOIC)

- **Source:** https://sourceforge.net

HOIC is one of the best-known **volunteer/hacktivist-style** DDoS tools (see the case study in
[`03-real-world-case-studies.md`](03-real-world-case-studies.md)). It performs HTTP flood attacks
and supports "booster scripts" that let multiple users coordinate simultaneous floods against a
shared target, amplifying the collective impact of a crowd of individually modest attackers.

## 6.4 Low Orbit Ion Cannon (LOIC)

- **Source:** https://sourceforge.net

LOIC is HOIC's older, simpler sibling — a stress-testing tool repurposed as a DDoS tool. It floods
a target with TCP, UDP, or HTTP requests with configurable thread counts and speed, and became
widely associated with hacktivist collectives due to its ease of use and "volunteer botnet" style
group attacks.

## 6.5 HULK (HTTP Unbearable Load King)

- **Source:** https://github.com

HULK is a Layer-7 stress tool that generates a high volume of **unique, obfuscated HTTP GET
requests** to a target web server — each request is deliberately crafted to look different (via
randomized headers, referrers, and user-agents) specifically to defeat caching layers and simple
signature-based detection, forcing the server to genuinely process every single request.

## 6.6 Slowloris (the tool)

- **Source:** https://github.com

The tool implementation of the Slowloris technique described in
[`05-application-layer-and-advanced-attacks.md`](05-application-layer-and-advanced-attacks.md) —
it opens many connections to the target and sends **partial HTTP headers**, trickling just enough
data periodically to keep each connection alive without ever completing it, exhausting the
server's connection pool using minimal attacker-side bandwidth.

## 6.7 UFONet

- **Source:** https://ufonet.03c8.net

UFONet is a toolkit that abuses **open redirects on third-party legitimate websites** to
indirectly generate a flood of traffic against a target — a form of the reflection/amplification
pattern covered in `04`–`05`, but built specifically around web-application redirect
vulnerabilities rather than network-protocol amplification (like NTP or DNS).

## 6.8 Packet Flooder Tool

- **Source:** https://www.netscantools.com

Part of the NetScanTools suite, this utility generates a configurable, high-rate stream of raw
packets against a chosen target — a general-purpose flood generator often used for basic network
stress-testing (again, **authorized targets only**).

---

## 🔍 Recognizing Flood Traffic in Wireshark

Regardless of which tool generated it, a flood/DoS attack in progress usually shows a very
recognizable signature in a packet capture: a huge volume of near-identical packets (same
destination, tight retransmission intervals, repeated `[TCP Retransmission]` or `[RST, ACK]`
flags) from one or a small number of source addresses hitting the same destination port
relentlessly.

```bash
# Live-capture and quickly eyeball volume per source IP (Linux, requires root)
sudo tcpdump -i eth0 -n | awk '{print $3}' | cut -d. -f1-4 | sort | uniq -c | sort -rn | head

# Wireshark display filter to isolate probable SYN-flood traffic
tcp.flags.syn == 1 && tcp.flags.ack == 0

# Wireshark display filter to isolate a suspected retransmission storm
tcp.analysis.retransmission
```

Cross-reference the source IP volume against **NetFlow/sFlow** statistics or your router's
interface counters — a sudden, sustained spike in packets-per-second or connections-per-second
from a wide (often spoofed) IP spread, concentrated on one destination, is the classic DoS/DDoS
signature discussed further in [`07-detection-techniques.md`](07-detection-techniques.md).

---

**Next:** [`07-detection-techniques.md`](07-detection-techniques.md) →