# 01 — Enumeration Concepts

## 1.1 What Is Enumeration?

Enumeration is the process of extracting usernames, machine names, network resources, shares, and services from a system or network. To do this, an attacker builds an **active connection** to the target and sends it **directed queries** — this is what separates enumeration from the more passive footprinting and scanning phases that come before it.

```
   Attacker  ---- active connection + directed queries ---->  Target System
   Attacker  <----------------- detailed info --------------  Target System
```

The attacker then uses everything pulled out during enumeration to:
- Identify specific attack points in the system
- Perform password attacks to gain unauthorized access to information-system resources

Enumeration techniques generally only work **in an intranet environment** — you need connectivity to the specific service, not just visibility of an open port from across the internet.

**Legal note:** the earlier modules (footprinting, scanning) mostly gather information without doing anything illegal. Enumeration is different — depending on an organization's policies and the laws in effect, actively querying a system like this can cross a legal line. An ethical hacker or pen tester should always have proper authorization before enumerating a target.

### Information Enumerated by Intruders

- Network resources
- Network shares
- Routing tables
- Audit and service settings
- SNMP and fully qualified domain name (FQDN) details
- Machine names
- Users and groups
- Applications and banners

**A specific trap worth knowing:** during enumeration, attackers may stumble onto a remote inter-process communication (IPC) share, such as **IPC$** on Windows. IPC$ is meant for interprocess communication, but attackers probe it further to connect to an administrative share — often by brute-forcing admin credentials — and once in, they can pull a complete listing of the file system that share represents.

## 1.2 Techniques for Enumeration

The following techniques are used to extract information about a target:

### Extract Usernames Using Email IDs
Every email address is really two pieces glued together: `username@domainname`. Harvest enough email addresses (e.g., from a company website, LinkedIn, or a data breach) and you effectively have a list of valid usernames for free.

### Extract Information Using Default Passwords
Plenty of online resources publish the default password lists assigned by manufacturers to their products. Users routinely ignore the "change the default password" recommendation that ships with hardware/software — which makes an attacker's job of enumerating and exploiting the target that much easier.

### Brute Force Active Directory
Microsoft Active Directory has a genuine design flaw around username enumeration during user-input verification: if a user has the **"logon hours"** feature enabled, every authentication attempt outside those hours returns a *different* error message than a wrong username would. Attackers use that inconsistency to enumerate valid usernames, then take the confirmed-valid list and run a brute-force attack to crack the corresponding passwords.

### Extract Information Using DNS Zone Transfer
A network administrator legitimately uses DNS zone transfer to replicate DNS data across multiple DNS servers or to back up DNS files — this requires executing a specific zone-transfer request against the name server. If the name server allows the transfer, it converts every DNS name and IP address it hosts into ASCII text and hands it over.

When administrators fail to configure the DNS server properly (i.e., leave zone transfer open to anyone), this becomes a goldmine for an attacker: a list of every named host, sub-zone, and associated IP address in the organization's network, in one request. Zone transfer can be performed with `nslookup` and `dig` (covered in detail in file `05`).

### Extract User Groups From Windows
To extract user groups from Windows, the attacker needs a registered ID as a user in Active Directory. From there, they can extract information about which groups that user belongs to, using either the Windows GUI or the command line.

### Extract Usernames Using SNMP
Attackers can easily guess read-only or read-write **community strings** via the SNMP application programming interface (API) to extract usernames directly.

### Extract Network Resources and Topology Using SNMP
Beyond usernames, attackers can methodically walk the SNMP tree to gather detailed information about network resources and topology as a whole — full details in file `03`.

## 1.3 Services and Ports to Enumerate

TCP and UDP are the two transport protocols that manage data communication between terminals on a network, and nearly every enumeration technique in this module hangs off one of these two.

**TCP** is connection-oriented and reliable — capable of carrying messages/emails across the internet with a full multi-process communication service. Its notable features:
- Acknowledgement via a sliding-window system
- Automatic retransmission of lost/unacknowledged data
- Addressing and multiplexing of data
- Connections that can be established, managed, and terminated
- Quality-of-service transmission
- Congestion management and flow control

**UDP** is connectionless and carries short messages with no delivery guarantee — "unreliable" in the formal networking sense, though it's exactly what you want for latency-sensitive traffic like:
- Audio streaming
- Video/teleconferencing

### Reference Table: Services and Ports Commonly Enumerated

| Port(s) | Service | What attackers get from it |
|---|---|---|
| **TCP/UDP 53** | DNS Zone Transfer | DNS clients send messages to a DNS server listening on UDP 53 by default; if a response would exceed UDP's 512-octet limit, the server flags the response as truncated and the client retries over **TCP** port 53 instead. TCP is the failover for lengthy queries. Malware such as the **ADM worm** and **Bonk Trojan** specifically abuse port 53 to exploit DNS server vulnerabilities. |
| **TCP/UDP 135** | Microsoft RPC Endpoint Mapper | RPC lets a client system request a service from a server; an *endpoint* is the protocol port the server listens on for RPC calls. The RPC Endpoint Mapper lets RPC clients discover the port currently assigned to a specific RPC service. A known flaw in how RPC exchanges messages over TCP/IP — incorrect handling of malformed messages — affects the Endpoint Mapper on port 135 and can be leveraged to launch a DoS attack. |
| **UDP 137** | NetBIOS Name Service (NBNS) | Also known as WINS. NBNS maintains a database matching NetBIOS names to IP addresses and is usually the first NetBIOS-related service attackers go after. Can technically use TCP 137 for a few operations too, though this is rarely seen in practice. |
| **TCP 139** | NetBIOS Session Service (SMB over NetBIOS) | Arguably the most well-known Windows port — used to transfer files over a network, for both null-session establishment and file/printer sharing. Restricting access to TCP 139 should be a top priority for any admin hardening a Windows box; a misconfigured 139 can let an intruder gain unauthorized access to critical files or the entire file system. |
| **TCP/UDP 445** | SMB over TCP (Direct Host) | Modern Windows hosts file/printer-sharing traffic directly over TCP port 445 rather than requiring the older NetBIOS-over-TCP (NBT) wrapper. |
| **UDP 161** | SNMP | Widely used to monitor network-attached devices (routers, switches, firewalls, printers, servers). SNMP has a manager/agent architecture: the agent listens for manager requests on port 161 and replies to the manager on port 162. |
| **TCP/UDP 389** | LDAP | Protocol for accessing and maintaining distributed directory information services over an IP network; uses TCP or UDP on port 389 by default. |
| **TCP 2049** | NFS | Mounts remote file systems so clients can interact with them as if they were local. NFS servers listen for clients on TCP 2049. A misconfigured NFS service can let attackers seize control of a remote system, escalate privileges, or plant backdoors/malware on the host. |
| **TCP 25** | SMTP | A TCP/IP mail delivery protocol running over TCP's connection-oriented service on the well-known port 25. See the command table below. |
| **TCP/UDP 162** | SNMP Trap | An agent uses this port to push unsolicited notifications (e.g., optional variable bindings, the `sysUpTime` value) to a manager. |
| **UDP 500** | ISAKMP/IKE | Internet Security Association and Key Management Protocol / Internet Key Exchange — part of the IPsec suite, used to establish, negotiate, modify, and delete Security Associations (SAs) and cryptographic keys in a VPN environment. |
| **TCP 22** | SSH / SFTP | SSH is a command-level protocol for securely managing networked devices remotely, generally used as the secure alternative to Telnet; the SSH server listens on TCP 22 by default. Attackers may brute-force SSH login credentials. SFTP also defaults to port 22, riding on SSH encryption — this single-port design is simpler and more secure than multi-port protocols like FTP/S. Attackers enumerate SFTP to learn about user accounts, file/directory permissions, and server configuration. |
| **TCP/UDP 3268** | Global Catalog Service | Microsoft's Global Catalog server — a domain controller storing *extra* information — listens on port 3268. Its database holds a row for every object in the *entire* organization (not just one domain), letting you locate objects from any domain without knowing the domain name up front. LDAP queries against the Global Catalog use port 3268; admins commonly connect to it via LDP for troubleshooting. |
| **TCP/UDP 5060, 5061** | SIP | Session Initiation Protocol — Internet-telephony signaling for voice/video calls. Port 5060 carries non-encrypted signaling traffic; 5061 carries TLS-encrypted signaling. |
| **TCP 20/21** | FTP | Connection-oriented file transfer; FTP control is on TCP 21, data transfer defaults to TCP 20 (or a dynamic port depending on server config). Once attackers confirm FTP ports are open, they enumerate the software version and any known vulnerabilities as a springboard to further exploitation — sniffing FTP traffic, brute-forcing FTP credentials, etc. |
| **TCP 23** | Telnet | An insecure protocol — login credentials travel in cleartext — so it's mostly confined to private networks today. The Telnet server listens on port 23. Attackers exploit Telnet for banner grabbing against other protocols (SSH, SMTP, etc.), credential brute-forcing, and port-forwarding attacks. |
| **UDP 69** | TFTP | A connectionless protocol built on UDP, so it offers no delivery guarantee. Primarily used to push firmware/software updates to remote networked devices, listening on UDP 69. Attackers can exploit TFTP to install malicious software or firmware on remote devices. |
| **TCP 179** | BGP | Border Gateway Protocol — heavily used by ISPs to maintain huge routing tables and process internet traffic efficiently; BGP routers establish sessions on TCP 179. Misconfigured BGP opens the door to dictionary attacks, resource-exhaustion attacks, flooding attacks, and hijacking attacks. |

### SMTP Command Reference

| Command | Syntax |
|---|---|
| Hello | `HELO <sending-host>` |
| From | `MAIL FROM:<from-address>` |
| Recipient | `RCPT TO:<to-address>` |
| Data | `DATA` |
| Reset | `RESET` |
| Verify | `VRFY<string>` |
| Expand | `EXPN<string>` |
| Help | `HELP[string]` |
| Quit | `QUIT` |

*(`VRFY`, `EXPN`, and `RCPT TO` are the three commands SMTP enumeration relies on most heavily — see file `05` for the full walkthrough.)*

---

**Next:** [`02-netbios-enumeration.md`](02-netbios-enumeration.md) — the first service the module tackles in depth, and usually the first one an attacker goes after too.
