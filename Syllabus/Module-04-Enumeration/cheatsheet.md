# Cheatsheet — Enumeration (Module 04)

One-page command reference, grouped by service. See the numbered files for full explanations of *why* each command works.

## NetBIOS

| Purpose | Command |
|---|---|
| Get NetBIOS name table of a remote host | `nbtstat -a <remotename>` |
| Get NetBIOS name table by IP | `nbtstat -A <IPaddress>` |
| List the NetBIOS name cache | `nbtstat -c` |
| Enumerate NetBIOS via Nmap NSE | `nmap -sV -v --script nbstat.nse <target>` |
| Enumerate NetBIOS over raw port 137 | `nmap -sU -p 137 --script nbstat.nse <target>` |
| List shares on a remote computer | `net view \\<computername>` |
| List all shares (incl. hidden) | `net view \\<computername> /ALL` |
| List all shares in current domain | `net view /domain` |
| List shares on a specific domain | `net view /domain:<domain name>` |
| AI: quick NetBIOS scan | `nbtscan <target>` |
| AI: NetBIOS info + names | `nmblookup -A <target>` |

## SNMP

| Purpose | Command |
|---|---|
| Walk SNMPv1 tree | `snmpwalk -v1 -c public <target>` |
| Walk SNMPv2c tree | `snmpwalk -v2c -c public <target>` |
| Search installed software | `snmpwalk -v2c -c public <target> hrSWInstalledName` |
| Get RAM size | `snmpwalk -v2c -c public <target> hrMemorySize` |
| Set an OID value | `snmpwalk -v2c -c public <target> <OID> <New Value>` |
| Set sysContact | `snmpwalk -v2c -c public <target> sysContact <New Value>` |
| Enumerate SNMP processes (Nmap) | `nmap -sU -p 161 --script=snmp-processes <target>` |
| Get SNMP server/OS details | `nmap -sU -p 161 --script=snmp-sysdescr <target>` |
| List installed applications | `nmap -sU -p 161 --script=snmp-win32-software <target>` |
| Full system/user enumeration | `snmp-check <target>` |

## LDAP

| Purpose | Command |
|---|---|
| Install Python LDAP library | `pip3 install ldap3` |
| Simple bind (auth) | `ldapsearch -h <target> -x` |
| Get naming contexts | `ldapsearch -h <target> -x -s base namingcontexts` |
| Query primary domain | `ldapsearch -h <target> -x -b "DC=htb,DC=local"` |
| Query by object class | `ldapsearch -h <target> -x -b "DC=htb,DC=local" '(objectClass=Employee)'` |
| Query all objects | `ldapsearch -x -h <target> -b "DC=htb,DC=local" "objectclass=*"` |
| Brute-force LDAP auth (Nmap) | `nmap -p 389 --script ldap-brute --script-args ldap.base='"cn=users,dc=CEH,dc=com"' <target>` |

## NTP

| Purpose | Command |
|---|---|
| Collect time samples (debug) | `ntpdate -d <target>` |
| Trace NTP server chain | `ntptrace [-n] [-m maxhosts] <servername/IP>` |
| Query ntpd daemon state | `ntpdc [-c command] <hostname/IP>` |
| Monitor ntpd performance | `ntpq [-c command] <host/IP>` |
| Interactive ntpq version check | `ntpq> version` |

## NFS

| Purpose | Command |
|---|---|
| Scan for open NFS port/services | `rpcinfo -p <target>` |
| List shared directories | `showmount -e <target>` |
| RPC misconfiguration scan | `python3 rpc-scan.py <target> --rpc` |
| Baseline enum of open ports | `./superenum` (then supply IP list file) |

## SMTP

| Purpose | Command |
|---|---|
| Manual VRFY probe | `telnet <target> 25` then `VRFY <user>` |
| Manual EXPN probe | `telnet <target> 25` then `EXPN <user>` |
| Manual RCPT TO probe | `telnet <target> 25` then `MAIL FROM:<x>` / `RCPT TO:<user>` |
| List SMTP commands (Nmap) | `nmap -p 25,365,587 --script=smtp-commands <target>` |
| Identify open relays | `nmap -p 25 --script=smtp-open-relay <target>` |
| Enumerate mail users (Nmap) | `nmap -p 25 --script=smtp-enum-users <target>` |
| Metasploit SMTP enum (module) | `use auxiliary/scanner/smtp/smtp_enum` → `set RHOSTS <target>` → `run` |
| Metasploit SMTP enum (one-liner) | `msfconsole -q -x "use auxiliary/scanner/smtp/smtp_enum; set RHOSTS <target>; run; exit"` |
| smtp-user-enum (VRFY mode) | `smtp-user-enum -M VRFY -u <user> -t <target>` |

## DNS

| Purpose | Command |
|---|---|
| Get DNS name servers | `dig ns <target domain>` |
| Attempt zone transfer | `dig @<name server> <target domain> axfr` |
| Windows: set query type SOA | `nslookup` → `set querytype=soa` → `<target domain>` |
| Windows: attempt zone transfer | `ls -d <domain of name server>` |
| Zone transfer via DNSRecon | `dnsrecon -t axfr -d <target domain>` |
| Cache snoop — non-recursive | `dig @<DNS server IP> <target domain> A +norecurse` |
| Cache snoop — recursive | `dig @<DNS server IP> <target domain> A +recurse` |
| DNSSEC zone walk (LDNS) | `ldns-walk @<DNS server IP> <target domain>` |
| DNSSEC/NSEC zone walk (DNSRecon) | `dnsrecon -d <target domain> -z` |
| OWASP Amass full enum | `amass enum -d <target domain>` |
| Amass passive only | `amass enum -passive -d <target domain> -src` |
| Amass active brute-force | `amass enum -active -d <target domain> -brute -w /usr/share/wordlists/amass/all.txt` |
| Amass track last 2 scans | `amass track -config /root/amass/config.ini -dir amass4owasp -d <target domain> -last 2` |
| Amass list DB results | `amass db -dir amass4owasp -list` |
| Amass visual graph | `amass viz -d3 -dir amass4owasp` |
| List DNS services (Nmap) | `nmap --script=broadcast-dns-service-discovery <target domain>` |
| Brute-force subdomains (Nmap) | `nmap -T4 -p 53 --script dns-brute <target domain>` |
| Check DNS recursion enabled | `nmap -Pn -sU -p 53 --script=dns-recursion <target>` |
| DNSSEC NSEC enum (Nmap) | `nmap -sU -p 53 --script dns-nsec-enum --script-args dns-nsec-enum.domains=<domain> <target>` |

## IPsec

| Purpose | Command |
|---|---|
| Direct ISAKMP scan | `nmap -sU -p 500 <target>` |
| IKE host discovery/fingerprint | `ike-scan -M <target gateway IP>` |
| IKE version detection (Nmap) | `nmap -sU -p 500 --script=ike-version <target>` |

## VoIP

| Purpose | Command |
|---|---|
| Identify SIP devices/PBX servers | `svmap <target network range/IP>` |
| Metasploit SIP enumerator | `use auxiliary/scanner/sip/enumerator` → `use auxiliary/scanner/sip/options` → `set RHOSTS <range>` → `run` |

## RPC

| Purpose | Command |
|---|---|
| RPC service scan | `nmap -sR <target IP/network>` |
| Aggressive RPC/OS/version scan | `nmap -T4 -A <target IP/network>` |

## Unix/Linux Users

| Purpose | Command |
|---|---|
| List logged-in users (remote) | `/usr/bin/rusers [-a] [-l] [-u\|-h\|-i] [Host ...]` |
| List logged-in users (local net) | `rwho [-a]` |
| Show user info | `finger [-l] [-m] [-p] [-s] [user ...] [user@host ...]` |

## SMB

| Purpose | Command |
|---|---|
| Full SMB enum (OS/version/scripts) | `nmap -p 445 -A <target>` |
| Enumerate supported SMB protocols | `nmap -p 445 --script smb-protocols <target>` |
| Enumerate protocols via port 139 | `nmap -p 139 --script smb-protocols <target>` |
| Enumerate SMB shares | `nmap -p 445 --script smb-enum-shares <target>` |

## Chained Automation Pattern (Discover → Scan → Report)

```bash
#!/bin/bash
target_range="10.10.1.0/24"
sudo apt-get update && sudo apt-get install -y nmap
mkdir -p ~/enumeration_results
nmap -sn $target_range -oN ~/enumeration_results/ping_sweep.txt
nmap -T4 -F $target_range -oN ~/enumeration_results/quick_scan.txt
nmap -T4 -A $target_range -oN ~/enumeration_results/detailed_scan.txt
nmap -sV $target_range -oN ~/enumeration_results/version_detection.txt
```

## Key Ports Reference

| Port(s) | Service |
|---|---|
| TCP/UDP 53 | DNS |
| TCP/UDP 135 | MS RPC Endpoint Mapper |
| UDP 137 | NetBIOS Name Service |
| UDP 138 | NetBIOS Datagram Service |
| TCP 139 | NetBIOS Session Service |
| UDP 161 / 162 | SNMP (agent / trap) |
| TCP/UDP 389 | LDAP |
| TCP/UDP 445 | SMB (Direct Host) |
| UDP 500 | ISAKMP/IKE (IPsec) |
| TCP 20/21 | FTP |
| TCP 22 | SSH / SFTP |
| TCP 23 | Telnet |
| TCP 25 | SMTP |
| UDP 69 | TFTP |
| TCP 111 (+UDP) | RPC portmapper |
| TCP 123 (UDP) | NTP |
| TCP 179 | BGP |
| TCP 2049 | NFS |
| UDP/TCP 2000, 2001, 5060, 5061 | SIP / VoIP |
| TCP/UDP 3268 | Global Catalog |

---

*Companion cheatsheet to the [`CEH-Module-04-Enumeration`](README.md) study repo.*
