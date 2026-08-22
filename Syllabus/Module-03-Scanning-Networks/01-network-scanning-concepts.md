# 01 — Network Scanning Concepts

## 1.1 What Is Network Scanning?

Network scanning is the process of actively probing a target network to build a picture of what's actually there: which hosts are alive, which ports are open on them, which services are running behind those ports, and what operating system each host is running.

Where footprinting is mostly passive (Whois, DNS records, job postings, social media), scanning is **active** — you're sending crafted packets directly at the target and drawing conclusions from the responses (or lack of them). It's still reconnaissance, just a louder, more detailed form of it.

```
        Attacker                          Target Network
           |                                    |
           | ---- sends TCP/IP probes -------->  |
           |                                    |
           | <----- gets network info back ---- |
           |                                    |
```

### Objectives of Network Scanning

A scan is typically run to achieve one or more of the following:

- Discover live hosts, their IP addresses, and their open ports
- Discover the OS and system architecture running on each host (a.k.a. **fingerprinting**) — this lets an attacker line up OS-specific exploits
- Discover which services/applications are listening on open ports, and their exact versions — version numbers point directly at known CVEs
- Identify vulnerabilities on any of the discovered systems
- Map out the network topology — devices, routers, switches, and how they interconnect

The more of this picture an attacker assembles, the more precisely they can target their next move.

## 1.2 Types of Scanning

The courseware draws a three-way distinction that's worth keeping straight, because "scanning" gets used loosely to mean all three:

| Type | What it finds | Analogy |
|---|---|---|
| **Network scanning** | Active hosts and their IP addresses on a network | Walking down a street and noting which houses have lights on |
| **Port scanning** | Open ports and the services listening behind them, by probing TCP/UDP ports | Checking which doors and windows on a house are unlocked |
| **Vulnerability scanning** | Known weaknesses in a system — a vulnerability scanner combines a scanning engine with a signature/exploit catalog (backup files, directory traversal patterns, outdated patches, etc.) | A locksmith testing whether each unlocked door/window can actually be forced open |

A useful mental picture from the source material: a burglar sizing up a house looks for doors and windows — the easily accessible points of entry. For computer systems, **ports are the doors and windows**. As a general (not absolute) rule, more open ports = more attack surface. But this isn't universal — a machine with very few open ports can still be catastrophically vulnerable if one of those ports is running something exploitable.

## 1.3 TCP/IP Communication Basics

Because almost every scanning technique in this module works by manipulating TCP flags and observing how a target reacts, you need the handshake mechanics down cold before any of the scan types (Xmas, NULL, FIN, ACK-probe, IDLE, etc.) will make sense.

### The TCP Header & Its Flags

The TCP header carries six 1-bit control flags. Four of them (`SYN`, `ACK`, `FIN`, `RST`) govern connection setup/teardown; the other two (`PSH`, `URG`) give the receiving stack processing instructions. A flag is "on" when its bit is set to `1`.

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Source Port         |       Destination Port       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                        Sequence Number                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Acknowledgment Number                     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Offset| Res |  TCP Flags  |            Window                 |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          TCP Checksum         |         Urgent Pointer       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                            Options                           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

| Flag | Name | What it does |
|---|---|---|
| **SYN** | Synchronize | Announces a new sequence number; starts the 3-way handshake |
| **ACK** | Acknowledgment | Confirms receipt of a transmission and states the next expected sequence number |
| **PSH** | Push | Tells the receiver to hand buffered data up to the application immediately, rather than waiting to fill a buffer — used at the start/end of a data transfer to avoid buffer deadlocks |
| **URG** | Urgent | Tells the system to process the packet's data immediately, ahead of everything else in the queue |
| **FIN** | Finish | Announces "no more data coming" — starts graceful connection teardown |
| **RST** | Reset | Aborts a connection in response to an error. **Attackers repurpose this flag heavily for scanning and enumeration**, since a RST response reveals a port is closed |

> Almost every stealth/inverse-flag scanning technique in `04-port-and-service-discovery.md` is really just creative use of SYN, ACK, and RST to extract "open/closed" information without completing a full, log-visible connection.

### The Three-Way Handshake (Session Establishment)

TCP is connection-oriented — before any data flows, the two ends negotiate ("shake hands on") the connection:

```
   Client (Bill)                              Server (Sheela)
   10.0.0.2:21                                 10.0.0.3:21

        |------------ SYN, SEQ#10 -------------------->|
        |         "I'd like to talk on port 21"         |
        |                                                |
        |<------- SYN+ACK, ACK#11, SEQ#142 -------------|
        |         "OK, I'm open on port 21"              |
        |                                                |
        |------------ ACK, ACK#143, SEQ#11 ------------->|
        |         "OK, thanks"                            |
        |                                                |
        |============ OPEN CONNECTION ==================|
```

1. **SYN** — client sends a SYN packet to the destination, proposing a connection.
2. **SYN/ACK** — server acknowledges with its own SYN, plus an ACK of the client's SYN.
3. **ACK** — client acknowledges the server's SYN/ACK.

Once all three packets have landed, the connection is "OPEN" and data can flow in both directions until one side sends `FIN` or `RST`.

### Session Termination

```
   Client (Bill)                              Server (Sheela)

        |------------ FIN, SEQ#50 ---------------------->|
        |        "I'm done sending data"                  |
        |                                                 |
        |<----------- ACK, ACK#51, SEQ#170 --------------|
        |        "Got your termination request"           |
        |                                                 |
        |<----------- FIN, SEQ#171 -----------------------|
        |        "I've sent everything too"                |
        |                                                 |
        |------------ ACK, ACK#172, SEQ#51 -------------->|
        |        "Thanks, closing"                         |
```

Termination is essentially two mini-handshakes stacked back to back — each side sends `FIN`, and the other `ACK`s it.

**Why this matters for scanning:** every scan type in this module is really a variation on "which of these packets does the target send back, and what does that response prove?" A full TCP Connect scan completes the whole handshake (loud, logged). A SYN/stealth scan stops after step 2 and sends `RST` instead of `ACK` (quieter, often unlogged at the application layer). Inverse-flag scans (FIN/NULL/Xmas) skip the handshake model entirely and rely on how the target's TCP/IP stack is supposed to behave per RFC 793 when it receives an out-of-context flag combination.

---

**Next:** [`02-scanning-tools.md`](02-scanning-tools.md) — the tools that actually generate these probes.
