# 04 — NTP and NFS Enumeration

## Part A: NTP Enumeration

### 4.1 Why NTP Matters to an Attacker

**Network Time Protocol (NTP)** is designed to synchronize the clocks of networked computers, using **UDP port 123** as its primary communication channel. Under ideal conditions, NTP can keep time to within 10 ms of error over the public internet, and to within 200 μs or better on LANs.

It's also one of the most commonly overlooked services when administrators think about hardening a network — but queried properly, NTP hands an attacker a surprising amount of network intelligence:

- List of hosts connected to the NTP server
- Clients' IP addresses on the network, their system names, and OSes
- Internal IPs, if the NTP server happens to sit in the demilitarized zone (DMZ)

### 4.2 NTP Enumeration Commands

Four command-line utilities drive NTP enumeration: `ntpdate`, `ntptrace`, `ntpdc`, and `ntpq`.

#### `ntpdate`

Collects a number of time samples from several time sources.

```
ntpdate [-46bBdqsuv] [-a key] [-e authdelay] [-k keyfile] [-o version] [-p samples] [-t timeout] [-U user_name] server [...]
```

| Flag | Function |
|---|---|
| `-4` | Force DNS resolution of given host names to the IPv4 namespace |
| `-6` | Force DNS resolution of given host names to the IPv6 namespace |
| `-a key` | Enable the authentication function / specify the key identifier to use for authentication |
| `-B` | Force the time to always be slewed |
| `-b` | Force the time to be stepped |
| `-d` | Enable debugging mode |
| `-e authdelay` | Specify the processing delay to perform an authentication function |
| `-k keyfile` | Specify the path for the authentication key file as the string "keyfile"; default is `/etc/ntp/keys` |
| `-o version` | Specify the NTP version for outgoing packets, as an integer (1 or 2); default is 4 |
| `-p samples` | Specify the number of samples to acquire from each server, 1–8; default is 4 |
| `-q` | Query only; do not set the clock |
| `-s` | Divert logging output from standard output (default) to the system syslog facility |
| `-t timeout` | Specify the maximum wait time for a server response; default is 1 s |
| `-u` | Use an unprivileged port for outgoing packets |
| `-v` | Be verbose; logs `ntpdate`'s version identification string |

**Example:**
```bash
ntpdate -d 10.10.1.22
```
```
transmit(10.10.1.22)
receive(10.10.1.22)
server 10.10.1.22, port 123
stratum 5, precision -23, leap 00, trust 000
refid [86.77.84.80], root delay 0.000160, root dispersion 0.010117
reference time:    e99acb0.e67e53c2   Tue, Mar 12 2024  6:28:00.900
originate timestamp: e99acbc.165dbe21 Tue, Mar 12 2024  6:28:12.087
transmit timestamp:  e99acbc.137c4cc2 Tue, Mar 12 2024  6:28:12.076
filter delay:  0.02638  0.02625  0.02661  0.02725
filter offset: +0.010468 +0.010501 +0.010421 +0.010423
delay 0.02625, dispersion 0.00003, offset +0.010501

12 Mar 06:28:12 ntpdate[3280]: adjust time server 10.10.1.22 offset +0.010501 sec
```

#### `ntptrace`

Determines where an NTP server obtains its time, following the chain of NTP servers back to the primary time source. Attackers use this to trace the full list of NTP servers connected to a network.

```
ntptrace [-n] [-m maxhosts] [servername/IP_address]
```

| Flag | Function |
|---|---|
| `-n` | Print only IP addresses, no host names — useful when a name server is down |
| `-m maxhosts` | Set the maximum number of levels up the chain to follow |

**Example:**
```
# ntptrace
localhost: stratum 4, offset 0.0019529, synch distance 0.143235
10.10.0.1: stratum 2, offset 0.01142
73, synch distance 0.115554
10.10.1.1: stratum 1, offset 0.0017698, synch distance 0.011193
```

#### `ntpdc`

Queries the `ntpd` daemon about its current state and requests changes to that state. Attackers use it to pull the state and statistics of every NTP server connected to the target network.

```
ntpdc [-46dilnps] [-c command] [hostname/IP_address]
```

| Flag | Function |
|---|---|
| `-4` | Force DNS resolution of the given host name to the IPv4 namespace |
| `-6` | Force DNS resolution of the given host name to the IPv6 namespace |
| `-d` | Turn on debugging mode |
| `-c` | Interprets the following argument as an interactive-format command; multiple `-c` options can be given |
| `-i` | Force `ntpdc` to operate interactively |
| `-l` | List of peers known to the server(s); equivalent to `-c listpeers` |
| `-n` | Output all host addresses in dotted-quad numeric format instead of host names |
| `-p` | Print a list of peers plus a summary of their states; equivalent to `-c peers` |
| `-s` | Print a list of peers plus a summary of their states, in a slightly different format than `-p`; equivalent to `-c dmpeers` |

Interactively, `ntpdc` exposes a large command set once launched — `addpeer`, `addrefclock`, `addserver`, `addtrap`, `authinfo`, `broadcast`, `clkbug`, `clockstat`, `clrtrap`, `controlkey`, `ctlstats`, `debug`, `delrestrict`, `disable`, `dmpeers`, `enable`, `exit`, `fudge`, `help`, `host`, `hostnames`, `ifreload`, `ifstats`, `iostats`, `kerninfo`, `keyid`, `keytype`, `listpeers`, `loopinfo`, `memstats`, `monlist`, `passwd`, `peers`, `preset`, `pstats`, `quit`, `readkeys`, `requestkey`, `reset`, `reslist`, `restrict`, `showpeer`, `sysinfo`, `sysstats`, `timeout`, `timerstats`, `traps`, `trustedkey`, `unconfig`, `unrestrict`, `untrustedkey`, and `version`.

#### `ntpq`

Monitors the operations of the `ntpd` daemon and determines its performance.

```
ntpq [-46dinp] [-c command] [host/IP_address]
```

| Flag | Function |
|---|---|
| `-4` | Force DNS resolution of the given host name to the IPv4 namespace |
| `-6` | Force DNS resolution of the given host name to the IPv6 namespace |
| `-c` | Following argument is an interactive-format command; multiple `-c` options may be given |
| `-d` | Debugging mode |
| `-i` | Force `ntpq` to operate interactively |
| `-n` | Output all host addresses in dotted-quad numeric format instead of host names |
| `-p` | Print a list of peers plus a summary of their states |

**Example (interactive session):**
```
ntpq> version
ntpq 4.2.8p15@1.3728-o
ntpq> host
current host is localhost
```

Interactive `ntpq` command set: `:config`, `addvars`, `apeers`, `associations`, `authenticate`, `authinfo`, `cl`, `clearvars`, `clocklist`, `clockvar`, `config-from-file`, `cooked`, `cv`, `debug`, `delay`, `drefid`, `exit`, `help`, `host`, `hostnames`, `ifstats`, `iostats`, `kerninfo`, `keyid`, `keytype`, `lassociations`, `lopeers`, `lpassociations`, `lpeers`, `monstats`, `mreadlist`, `mreadvar`, `mrl`, `mrulist`, `mrv`, `ntpversion`, `opeers`, `passociations`, `passwd`, `peers`, `poll`, `pstats`, `quit`, `raw`, `readlist`, `readvar`, `reslist`, `rl`, `rv`, `savevariables`, `showvars`, `sysinfo`, `sysstats`, `timeout`, `timerstats`, `version`, `writelist`, `writevar`.

> **Note:** In many modern Linux distributions, the classic `ntpd` daemon has been effectively joined (or replaced) by **Chrony** (`chronyd`). Both daemons perform the same job — synchronizing the local system's time with a remote time server.

### 4.3 NTP Enumeration Tools

**PRTG Network Monitor** — https://www.paessler.com
Monitors every system, device, traffic flow, and application across an IT infrastructure using SNMP, WMI, and SSH. Attackers use it to retrieve SNTP server details — response time from the server, active sensors tied to that server, and synchronization time.

**Additional NTP enumeration tools:**
| Tool | Source |
|---|---|
| Nmap | https://nmap.org |
| Wireshark | https://www.wireshark.org |
| udp-proto-scanner | https://labs.portcullis.co.uk |
| NTP Server Scanner | http://www.bytefusion.com |

---

## Part B: NFS Enumeration

### 4.4 What NFS Enumeration Reveals

**NFS** (Network File System) is a file system that lets users access, view, store, and update files on a remote server, transparently — the client interacts with remote data exactly as if it were mounted locally. Depending on the privileges assigned, a client can be read-only or read/write.

NFS is generally deployed on networks where centralizing data for critical resources matters. Remote procedure calls (RPC) route and process the requests between clients and servers underneath NFS.

Sharing files/directories over the network happens via **exporting**; the client makes that exported data available locally via **mounting**. The `/etc/exports` file on the NFS server holds the list of clients allowed to share files with the server. Critically, the *only* credential NFS checks to allow access is **the client's IP address** — no password required. NFS versions before v4 all run on this same security model.

Enumerating NFS services lets an attacker identify:
- Exported directories
- The list of clients connected to the NFS server, along with their IP addresses
- The shared data tied to those IP addresses

Once an attacker has this picture, they can **spoof one of the allowed client IP addresses** to gain full access to the shared files on the server — since IP address alone is the trust mechanism.

### 4.5 Enumerating NFS with `rpcinfo` and `showmount`

**`rpcinfo`** scans a target IP for an open NFS port (2049) and the NFS services running on it:

```bash
rpcinfo -p <Target IP Address>
```

Example output:
```bash
rpcinfo -p 10.10.1.13
```
```
   program vers proto   port  service
    100000    4   tcp    111  portmapper
    100000    3   tcp    111  portmapper
    100000    2   tcp    111  portmapper
    100000    4   udp    111  portmapper
    100000    3   udp    111  portmapper
    100000    2   udp    111  portmapper
    100024    1   udp  50883  status
    100024    1   tcp  41813  status
    100005    1   udp  59085  mountd
    100005    1   tcp  38127  mountd
    100005    2   udp  48885  mountd
    100005    2   tcp  39347  mountd
    100005    3   udp  42995  mountd
    100005    3   tcp  48399  mountd
    100003    3   tcp   2049  nfs      <-- open NFS port + service
    100003    4   tcp   2049  nfs      <-- open NFS port + service
    100227    3   tcp   2049
    100021    1   udp  55478  nlockmgr
    100021    3   udp  55478  nlockmgr
    100021    4   udp  55478  nlockmgr
    100021    1   tcp  42867  nlockmgr
    100021    3   tcp  42867  nlockmgr
    100021    4   tcp  42867  nlockmgr
```

**`showmount`** views the list of shared files and directories:

```bash
showmount -e <Target IP Address>
```

Example:
```bash
showmount -e 10.10.1.9
```
```
Export list for 10.10.1.9:
/home *
```

Here `/home` is a shared folder, exported to `*` (any client). From this point, an attacker can use various follow-on commands and tools to gain access to the NFS server and even upload malicious files to launch further attacks.

### 4.6 NFS Enumeration Tools

NFS enumeration tools scan a network within a given IP range (or a single IP) to identify running NFS services — pulling a list of RPC services via the port mapper, a list of NFS shares, and a list of directories accessible through NFS. Some can also download a file shared through the NFS server directly.

**RPCScan** — https://github.com
Communicates with RPC services and checks for misconfigurations on NFS shares.

```bash
python3 rpc-scan.py <Target IP Address> --rpc
```

Example:
```bash
python3 rpc-scan.py 10.10.1.19 --rpc
```
```
rpc://10.10.1.19:111    Portmapper
RPC services for 10.10.1.19:
portmapper (100000)   2   udp   111
portmapper (100000)   3   udp   111
portmapper (100000)   4   udp   111
portmapper (100000)   2   tcp   111
portmapper (100000)   3   tcp   111
portmapper (100000)   4   tcp   111
nfs (100003)          2   tcp  2049
nfs (100003)          3   tcp  2049
nfs (100003)          2   udp  2049
nfs (100003)          4   tcp  2049
mount demon (100005)  1   tcp  2049
mount demon (100005)  2   tcp  2049
mount demon (100005)  3   tcp  2049
mount demon (100005)  1   udp  2049
mount demon (100005)  2   udp  2049
mount demon (100005)  3   udp  2049
```

**SuperEnum** — https://github.com
Includes a script that performs baseline enumeration on any open port. An attacker runs `./superenum`, then feeds it a text file (e.g., `Target.txt`) containing a target IP or list of IPs.

```bash
./superenum
Enter IP List filename with path
Target.txt
```
```
TCP Scan Started for IP: 10.10.1.19
```
After scanning, SuperEnum reports all open ports it found; when port 2049 comes back open, it explicitly flags the NFS service and cross-checks it with multiple tools (`nmap_nfs-ls`, `nmap_nfs-statfs`, `showmount`):
```
Testing for 10.10.1.19: 2049
Testing for 10.10.1.19: 2049, Tool: nmap_nfs-ls
Testing for 10.10.1.19: 2049, Tool: nmap_nfs-statfs   <-- Open NFS Port
Testing for 10.10.1.19: 2049, Tool: showmount
```

---

**Next:** [`05-smtp-and-dns-enumeration.md`](05-smtp-and-dns-enumeration.md) — two services almost every organization runs, and both leak substantial info if left unhardened.
