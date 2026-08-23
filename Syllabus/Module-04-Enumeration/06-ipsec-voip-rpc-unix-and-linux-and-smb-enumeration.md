# 06 — IPsec, VoIP, RPC, Unix/Linux, and SMB Enumeration

This file rounds out the module's remaining enumeration targets: IPsec-based VPNs, VoIP/SIP infrastructure, RPC services, Unix/Linux logged-in users, and SMB — plus how attackers are increasingly stitching all of this together with AI-generated automation scripts.

## 6.1 IPsec Enumeration

**IPsec** is the most commonly implemented technology for both gateway-to-gateway (LAN-to-LAN) and host-to-gateway (remote access) enterprise VPN solutions. It secures communication between VPN endpoints using components such as Encapsulating Security Payload (ESP), Authentication Header (AH), and Internet Key Exchange (IKE).

Most IPsec-based VPNs use **ISAKMP** (Internet Security Association and Key Management Protocol), part of IKE, to establish, negotiate, modify, and delete Security Associations (SAs) and cryptographic keys in a VPN environment. Because ISAKMP runs on a fixed, well-known port, a simple scan is often enough to confirm a VPN gateway exists at all.

**Step 1 — direct scanning for ISAKMP:**
```bash
nmap -sU -p 500 <target IP address>
```
A response like `500/udp open|filtered isakmp` is a strong hint that a VPN gateway sits at that address.

**Step 2 — probe further with `ike-scan`:**

**Source:** https://github.com

`ike-scan` discovers IKE hosts and can fingerprint them via their retransmission backoff pattern. Specially crafted IKE packets carrying an ISAKMP header are sent to the target gateway, and the responses are recorded.

```bash
ike-scan -M <target gateway IP address>
```

Example:
```bash
ike-scan -M 202.170.130.17
```
```
Starting ike-scan 1.9.5 with 1 hosts (http://www.nta-monitor.com/tools/ike-scan/)
202.170.130.17	Notify message 14 (NO-PROPOSAL-CHOSEN)
	HDR=(CKY-R=f161f1d5ea32a456)

Ending ike-scan 1.9.5: 1 hosts scanned in 0.227 seconds (4.40 hosts/sec).  0 returned handshake; 1 returned notify
```

`ike-scan` can perform five distinct functions:

| Function | What it does |
|---|---|
| **Discovery** | Determine which hosts in a given IP range are running IKE, by showing which hosts respond to the IKE requests `ike-scan` sends |
| **Fingerprinting** | Determine the IKE implementation in use (and sometimes its software version) via **UDP backoff fingerprinting** (comparing the arrival-time pattern of IKE response retransmissions against known patterns) or **Vendor ID fingerprinting** (comparing Vendor ID payloads from the VPN server against known signatures) |
| **Transform enumeration** | Determine the transform attributes the VPN server supports for IKE phase 1 (encryption algorithm, hash algorithm) |
| **User enumeration** | For some VPN systems, discover valid VPN usernames |
| **Pre-shared key cracking** | Offline dictionary/brute-force cracking against IKE Aggressive Mode with pre-shared-key authentication — `ike-scan` obtains the hash and parameters, and `psk-crack` (also part of the ike-scan package) performs the actual cracking |

### IPsec Enumeration with AI

**Prompt:** *"Perform IPsec enumeration on target IP 10.10.1.22 with nmap."*
```bash
nmap -sU -p 500 --script=ike-version 10.10.1.22
```
- `nmap` — invoke Nmap
- `-sU` — UDP scan (no payload), typically used for services that don't respond to ICMP
- `-p 500` — the default IKE port used by IPsec VPNs
- `--script=ike-version` — detect the version of IKE running on the target

This one command performs a UDP scan on port 500 and runs the `ike-version` script against the target, providing insight into the IPsec configuration without needing a separate manual `ike-scan` pass.

## 6.2 VoIP Enumeration

VoIP has replaced the traditional public switched telephone network (PSTN) in both corporate and home settings — it uses internet infrastructure to establish voice calls, with the call data riding the same network as everything else. That shared-network design is exactly why VoIP is vulnerable to TCP/IP attack vectors.

**Session Initiation Protocol (SIP)** is one of the protocols VoIP uses for voice calls, video calls, and similar functions over an IP network. SIP service generally runs on UDP/TCP ports **2000, 2001, 5060, and 5061**.

Attackers use **Svmap** and **Metasploit** to perform VoIP enumeration, extracting sensitive info such as VoIP gateways/servers, IP-PBX systems, and User-Agent IP addresses/user extensions of client software (softphones) or VoIP phones. This info feeds directly into follow-on VoIP attacks: DoS, session hijacking, caller ID spoofing, eavesdropping, spam over internet telephony (SPIT), and VoIP phishing (vishing).

### Svmap

**Source:** https://github.com

Svmap is an open-source scanner that identifies SIP devices and PBX servers on a target network — genuinely useful for system administrators as a network-inventory tool, and just as useful to an attacker for the same reason.

Attackers use Svmap to:
- Identify SIP devices and PBX servers on default *and* non-default ports
- Scan large ranges of networks
- Scan one host across multiple ports for an SIP service (or multiple hosts across multiple ports)
- Ring every phone on a network simultaneously using the `INVITE` method

```bash
svmap <target network range/IP Address>
```

Example output:
```
+--------------------+------------------+
| SIP Device         | User Agent       |
+====================+==================+
| 151.50.106.225:5060 | DLink VoIP Stack |
+--------------------+------------------+
```

### SIP Enumeration Using Metasploit

Metasploit's **SIP Username Enumerator** module scans numeric usernames/extensions on VoIP phones.

```
use auxiliary/scanner/sip/enumerator
use auxiliary/scanner/sip/options
set RHOSTS 192.168.0.1/24
run
```

Example output:
```
[*] Sending SIP UDP OPTIONS requests to 192.168.0.0->192.168.0.255 (256 hosts)
[*] 192.168.0.54:5060  udp  SIP/2.0 200 OK: {"User-Agent"=>"Grandstream GXP1620
1.0.2.27", "Allow"=>"INVITE, ACK, OPTIONS, CANCEL, BYE, SUBSCRIBE, NOTIFY, INFO,
REFER, UPDATE, MESSAGE"}
[*] 192.168.0.87:5060  udp  SIP/2.0 200 OK: {"User-Agent"=>"Grandstream GXP1620
1.0.2.27", "Allow"=>"INVITE, ACK, OPTIONS, CANCEL, BYE, SUBSCRIBE, NOTIFY, INFO,
REFER, UPDATE, MESSAGE"}
...
[*] Scanned 256 of 256 hosts (100% complete)
[*] Auxiliary module execution completed
```

## 6.3 RPC Enumeration

**Remote Procedure Call (RPC)** is the technology behind distributed client/server programs. It's an inter-process communication mechanism that lets data flow between processes running on different machines. In general, RPC is built from a client, a server, an endpoint, an endpoint mapper, a client stub, a server stub, and assorted dependencies.

The **portmapper service** listens on **TCP and UDP port 111**, its job being to detect endpoints and present clients with details about listening RPC services. Enumerating RPC endpoints lets attackers identify any vulnerable services sitting on those ports. In networks protected by firewalls and other security controls, portmapper itself is often filtered — which is exactly why attackers fall back to scanning wide port ranges to find RPC services that are open to direct attack, rather than relying solely on the portmapper.

```bash
# Scan for RPC services
nmap -sR <target IP/network>

# Aggressive scan with OS/version/script detection
nmap -T4 -A <target IP/network>
```

Example (Zenmap):
```bash
nmap -T4 -A 10.10.1.0/24
```
```
Nmap scan report for 10.10.1.22
Host is up (0.0010s latency).
Not shown: 983 closed tcp ports (reset)
PORT    STATE SERVICE      VERSION
53/tcp  open  domain       Simple DNS Plus
80/tcp  open  http         Microsoft IIS httpd 10.0
88/tcp  open  kerberos-sec Microsoft Windows Kerberos (server time: 2024-03-12 12:33:20Z)
135/tcp open  msrpc        Microsoft Windows RPC
139/tcp open  netbios-ssn  Microsoft Windows netbios-ssn
389/tcp open  ldap         Microsoft Windows Active Directory LDAP (Domain: CEH.com0., Site: Default-First-Site-Name)
```

Attackers also use **NetScanTools Pro**'s `*nix RPC Info` tool to detect and access the portmapper service that typically runs on port 111 of Unix/Linux machines — querying the program number, version, protocol, and port for every registered RPC service on the target (e.g., `100000` portmapper on TCP/UDP 111, `100003` NFS and `100005` mount daemon both on port 2049).

## 6.4 Unix/Linux User Enumeration

Getting a list of logged-in users — along with usernames, host names, and session start times — is one of the important steps in enumerating a Unix/Linux target. Three command-line utilities cover this:

### `rusers`

Displays a list of users logged in to remote machines, or machines on the local network. Output is similar to the `who` command but scoped across every host/system on the local network.

```
/usr/bin/rusers [-a] [-l] [-u| -h| -i] [Host ...]
```

| Option | Function |
|---|---|
| `-a` | Report on a machine even if no users are logged in |
| `-h` | Sort alphabetically by host name |
| `-l` | Longer listing, similar to the `who` command |
| `-u` | Sort by the number of users |
| `-i` | Sort by idle time |

### `rwho`

Displays a list of users logged in to hosts on the local network. Output is similar to `who` and includes username, host name, and start date/time of each session, for every machine on the local network running the `rwho` daemon.

```
rwho [-a]
```
| Option | Function |
|---|---|
| `-a` | Include all users; without this flag, sessions idle for an hour or more are excluded from the report |

### `finger`

Displays info about system users: login name, real name, terminal name, idle time, login time, office location, and office phone numbers.

```
finger [-l] [-m] [-p] [-s] [user ...] [user@host ...]
```

| Option | Function |
|---|---|
| `-s` | Show login name, real name, terminal name, idle time, login time, office location, and office phone number |
| `-l` | Multi-line format showing everything `-s` shows, plus home directory, home phone number, login shell, mail status, and the contents of `.plan`, `.project`, `.pgpkey`, and `.forward` from the user's home directory |
| `-p` | Prevent `-l` from displaying the contents of `.plan`, `.project`, and `.pgpkey` |
| `-m` | Prevent username matching |

Example:
```bash
finger
```
```
Login    Name     Tty      Idle  Login Time   Office     Office Phone
ubuntu   Ubuntu   *:1            Mar 12 03:23 (:1)
```
```bash
finger ubuntu
```
```
Login: ubuntu                          Name: Ubuntu
Directory: /home/ubuntu                Shell: /bin/bash
On since Tue Mar 12 03:23 (EDT) on :1 from :1 (messages off)
No mail.
No Plan.
```

## 6.5 SMB Enumeration

**Server Message Block (SMB)** is a transport protocol Windows systems use to provide shared access to files, printers, and serial ports, along with remote access to Windows services. By default, SMB runs directly on **TCP port 445**, or via the older NetBIOS API on UDP ports 137/138 and TCP ports 137/139. Through SMB, users can access files and other data on a remote server — and SMB also allows read, write, and modify operations on those remote files. A network running this service is highly vulnerable to SMB enumeration, which provides a good amount of information about the target.

In SMB enumeration, attackers typically perform **banner grabbing** to pull OS details and running service versions — this info then feeds into SMB relay attacks and brute-force attacks. Common SMB enumeration tools: Nmap, SMBMap, enum4linux, nullinux, SMBeagle, and NetScanTool Pro.

```bash
nmap -p 445 -A <target IP>
```
`-p` specifies the port to scan (445 here); `-A` handles OS detection, version detection, script scanning, and traceroute info.

Example:
```bash
nmap -p 445 -A 10.10.1.19
```
```
PORT    STATE SERVICE     VERSION
445/tcp open  microsoft-ds?
MAC Address: 02:15:5D:64:A2:27 (Unknown)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running: Microsoft Windows 2019
OS details: Microsoft Windows Server 2019
Network Distance: 1 hop

Host script results:
| smb2-security-mode:
|   3:1:1:
|_    Message signing enabled but not required
|_clock-skew: -1s
|_nbstat: NetBIOS name: SERVER2019, NetBIOS user: <unknown>, NetBIOS MAC: 02:15:5d:64:a2:27 (unknown)
| smb2-time:
|   date: 2024-03-15T13:26:xx
|_  start_date: N/A

TRACEROUTE
```

**Enumerating the supported protocols/versions of the target SMB server:**
```bash
nmap -p 445 --script smb-protocols <Target IP>
nmap -p 139 --script smb-protocols <Target IP>
```

Example:
```bash
nmap -p 445 --script smb-protocols 10.10.1.19
```
```
PORT    STATE SERVICE
445/tcp open  microsoft-ds
Host script results:
| smb-protocols:
|   dialects:
|     2:0:2
|     2:1:0
|     3:0:0
|     3:0:2
|_    3:1:1
```

### SMB Enumeration with AI

**Prompt:** *"Scan the target IP 10.10.1.22 for the port using SMB with nmap"*
```bash
nmap -p 445 --script smb-enum-shares 10.10.1.22
```
- `-p 445` — SMB's TCP port
- `--script smb-enum-shares` — enumerates shares available on SMB servers
- `10.10.1.22` — target IP

Example output:
```
PORT    STATE SERVICE
445/tcp open  microsoft-ds

Host script results:
| smb-enum-shares:
|   note: ERROR: Enumerating shares failed, guessing at common ones (NT_STATUS_ACCESS_DENIED)
|   account_used: <blank>
|   \\10.10.1.22\ADMIN$:
|     warning: Couldn't get details for share: NT_STATUS_ACCESS_DENIED
|     Anonymous access: <none>
|   \\10.10.1.22\C$:
|     warning: Couldn't get details for share: NT_STATUS_ACCESS_DENIED
|     Anonymous access: <none>
|   \\10.10.1.22\IPC$:
|     warning: Couldn't get details for share: NT_STATUS_ACCESS_DENIED
|     Anonymous access: READ
|   \\10.10.1.22\NETLOGON:
```
Notice the mix of results: some shares reject even anonymous enumeration (`NT_STATUS_ACCESS_DENIED`), while `IPC$` still grants anonymous **READ** access — precisely the kind of partial exposure enumeration is designed to surface.

## 6.6 Create and Run Custom Scripts to Automate Network Enumeration Tasks with AI

Beyond running one enumeration command at a time, attackers increasingly prompt an AI shell-assistant to **generate an entire automation script** that chains multiple enumeration stages together — host discovery, quick scan, detailed scan, version detection — and saves every stage's output to its own file for later analysis.

**Prompt:** *"Develop and execute a script which will automate network enumeration tasks on target IP range 10.10.1.0/24"*

Generated script:
```bash
#!/bin/bash
target_range="10.10.1.0/24"

# Update system and install necessary tools
sudo apt-get update && sudo apt-get install -y nmap

# Create a directory for the enumeration outputs
mkdir -p ~/enumeration_results

# Perform a ping sweep to find live hosts
nmap -sn $target_range -oN ~/enumeration_results/ping_sweep.txt

# Perform a quick scan on discovered hosts
nmap -T4 -F $target_range -oN ~/enumeration_results/quick_scan.txt

# Perform a detailed scan on discovered hosts
nmap -T4 -A $target_range -oN ~/enumeration_results/detailed_scan.txt

# Perform a version detection scan on discovered hosts
nmap -sV $target_range -oN ~/enumeration_results/version_detection.txt

# Execute the script
chmod +x network_enumeration.sh && ./network_enumeration.sh
```

**What each stage does:**
- `#!/bin/bash` — shebang, run under Bash
- `target_range="10.10.1.0/24"` — the IP range variable used throughout
- `sudo apt-get update && sudo apt-get install -y nmap` — ensures Nmap is installed
- `mkdir -p ~/enumeration_results` — creates an output directory for every stage's results
- `nmap -sn $target_range -oN ~/enumeration_results/ping_sweep.txt` — ping sweep to find live hosts, saved to `ping_sweep.txt`
- `nmap -T4 -F $target_range -oN ~/enumeration_results/quick_scan.txt` — fast scan of the most common ports on discovered hosts, saved to `quick_scan.txt`
- `nmap -T4 -A $target_range -oN ~/enumeration_results/detailed_scan.txt` — full detailed scan (OS detection, version detection, scripts, traceroute), saved to `detailed_scan.txt`
- `nmap -sV $target_range -oN ~/enumeration_results/version_detection.txt` — dedicated service/version scan, saved to `version_detection.txt`
- `chmod +x network_enumeration.sh && ./network_enumeration.sh` — makes the script executable and runs it

**Result:** running this single generated script against a subnet produces a full battery of enumeration output — live host list, quick port summary, and rich per-host detail including SMB security mode, NetBIOS names, OS fingerprints (e.g., `OS: Windows 10 Enterprise 22000`, `OS CPE: cpe:/o:microsoft:windows_10::-`), domain/forest names, RDP NTLM info, SSL certificate validity windows, and even enumerated SMB users with their RIDs and account flags (e.g., `CEH\Guest (RID: 501)`, `CEH\Martin (RID: 1104)`, `CEH\Shiela (RID: 1105)`) — all without the attacker hand-typing a single Nmap flag beyond the original prompt.

---

**Next:** [`07-enumeration-countermeasures.md`](07-enumeration-countermeasures.md) — closing the loop with the defensive side of everything covered in files `02`–`06`.
