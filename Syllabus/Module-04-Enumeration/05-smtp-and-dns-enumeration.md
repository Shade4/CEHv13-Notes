# 05 — SMTP and DNS Enumeration

## Part A: SMTP Enumeration

### 5.1 Why SMTP Is Enumerable

Mail systems commonly pair **SMTP** with POP3 and IMAP — SMTP handles outbound delivery while POP3/IMAP let users save and download messages from the server mailbox. SMTP uses mail exchange (MX) records via DNS to route mail and runs on TCP port **25** (also commonly 2525 or 587).

SMTP ships with three built-in commands that respond differently for valid vs. invalid users — and that difference is exactly what enumeration exploits:

| Command | Purpose |
|---|---|
| **VRFY** | Validates whether a user exists |
| **EXPN** | Shows the actual delivery addresses of aliases and mailing lists |
| **RCPT TO** | Defines the recipient(s) of a message |

Because SMTP servers respond differently to `VRFY`, `EXPN`, and `RCPT TO` depending on whether the target user is valid, an attacker can directly interact with SMTP through a raw Telnet session and collect a list of valid users on the server, no special tooling required.

### 5.2 Manual Enumeration via Telnet

**Using VRFY:**
```
$ telnet 192.168.168.1 25
Trying 192.168.168.1...
Connected to 192.168.168.1.
Escape character is '^]'.
220 NYmailserver ESMTP Sendmail 8.9.3
HELO
501 HELO requires domain address
HELO x
250 NYmailserver Hello [10.0.0.86], pleased to meet you
VRFY Jonathan
250 Super-User <Jonathan@NYmailserver>
VRFY Smith
550 Smith... User unknown
```

**Using EXPN:**
```
$ telnet 192.168.168.1 25
...
EXPN Jonathan
250 Super-User <Jonathan@NYmailserver>
EXPN Smith
550 Smith... User unknown
```

**Using RCPT TO:**
```
$ telnet 192.168.168.1 25
...
MAIL FROM:Jonathan
250 Jonathan... Sender ok
RCPT TO:Ryder
250 Ryder... Recipient ok
RCPT TO: Smith
550 Smith... User unknown
```

In every case, a real account returns a `2xx`-style success and a fake one returns `550 ... User unknown` — a clean binary signal an attacker can automate against a whole wordlist of candidate names.

Admins and pen testers can perform SMTP enumeration using command-line utilities like Telnet and netcat, or with dedicated tools — Metasploit, Nmap, NetScanTools Pro, and smtp-user-enum — to collect valid users, delivery addresses, message recipients, and more.

### 5.3 SMTP Enumeration Using Nmap

**Source:** https://nmap.org

Attackers enumerate the target SMTP server using various SMTP-focused Nmap Scripting Engine (NSE) scripts.

```bash
# List all SMTP commands available in the Nmap directory
nmap -p 25,365,587 --script=smtp-commands <Target IP Address>

# Identify SMTP open relays
nmap -p 25 --script=smtp-open-relay <Target IP Address>

# Enumerate all mail users on the SMTP server
nmap -p 25 --script=smtp-enum-users <Target IP Address>
```

Example output of the last command:
```
PORT   STATE SERVICE
25/tcp open  smtp
| smtp-enum-users:
|   root
|   admin
|   administrator
|   webadmin
|   sysadmin
|   netadmin
|   guest
|   user
|   web
|_  test
```

### 5.4 SMTP Enumeration Using Metasploit

Metasploit ships an SMTP enumeration module that connects to the target SMTP server and enumerates usernames against a predefined wordlist. The SMTP server's own `VRFY` method validates each candidate username against the wordlist, and Metasploit surfaces the matched list of real accounts.

**Steps to enumerate SMTP users with Metasploit:**

1. **Launch and select the module:**
   ```
   msf > use auxiliary/scanner/smtp/smtp_enum
   msf auxiliary(smtp_enum) >
   ```

2. **Inspect available options:**
   ```
   show options
   ```
   Key options: `RHOSTS` (target host(s)), `RPORT` (default 25), `THREADS` (default 1, max one per host), `UNIXONLY` (skip Microsoft-banner servers when testing Unix users — default true), `USER_FILE` (default `/usr/share/metasploit-framework/data/wordlists/unix_users.txt`).

   You can also run `show evasion` to view options for evading security solutions.

3. **Set the target:**
   ```
   set RHOSTS 10.10.1.19
   ```

4. **(Optional) Use a custom wordlist:**
   ```
   set USER_FILE <location of wordlist file>
   ```

5. **(Optional) See advanced options:**
   ```
   show advanced
   ```
   Includes `CHOST`/`CPORT` (local client address/port), `ConnectTimeout` (default 10s), `Proxies`, `SSL`/`SSLCipher`/`SSLVersion`/`SSLVerifyMode`, and `ShowProgress`.

6. **Run the scan:**
   ```
   run
   ```
   Example output:
   ```
   [*] 220 metasploitable.localdomain ESMTP Postfix (Ubuntu)
   [*] Domain Name: localdomain
   [+] 192.168.1.56:25 - Found user: ROOT
   [+] 192.168.1.56:25 - Found user: backup
   [+] 192.168.1.56:25 - Found user: bin
   [+] 192.168.1.56:25 - Found user: daemon
   [+] 192.168.1.56:25 - Found user: distccd
   [+] 192.168.1.56:25 - Found user: ftp
   [+] 192.168.1.56:25 - Found user: games
   [+] 192.168.1.56:25 - Found user: gnats
   [+] 192.168.1.56:25 - Found user: irc
   [+] 192.168.1.56:25 - Found user: libuuid
   [+] 192.168.1.56:25 - Found user: list
   [+] 192.168.1.56:25 - Found user: lp
   [+] 192.168.1.56:25 - Found user: mail
   ```

### 5.5 SMTP Enumeration Tools

**NetScanTools Pro** — https://www.netscantools.com
Its SMTP Email Generator tool tests the process of sending an email through an SMTP server. Attackers use it for SMTP enumeration and to extract all email header parameters, including confirm/urgent flags. Sessions can be logged to a file and reviewed later — showing the full communication between NetScanTools Pro and the SMTP server, including relay-test results (e.g., `RCPT TO:<securitytest@yourdomain.com>` → `550 5.7.1 Unable to relay`).

**smtp-user-enum** — https://pentestmonkey.net
A tool specifically for enumerating OS-level user accounts on Solaris via SMTP (sendmail), by inspecting responses to `VRFY`, `EXPN`, and `RCPT TO`.

```
smtp-user-enum.pl [options] (-u username|-U file-of-usernames) (-t host|-T file-of-targets)
```

| Option | Function |
|---|---|
| `-m n` | Maximum number of processes (default: 5) |
| `-M mode` | SMTP command to use for username guessing — `EXPN`, `VRFY`, or `RCPT TO` (default: `VRFY`) |
| `-u user` | Check whether a specific user exists on the remote system |
| `-f addr` | From-address to use for `RCPT TO` guessing (default: `user@example.com`) |
| `-D dom` | Domain to append to a supplied user list to build email addresses (default: none) |
| `-U file` | File of usernames to check via SMTP |
| `-t host` | Target host running the SMTP service |
| `-T file` | File of hostnames running the SMTP service |
| `-p port` | TCP port the SMTP service runs on (default: 25) |
| `-d` | Debugging output |
| `-t n` | Max wait time (seconds) for the reply (default: 5) |
| `-v` | Verbose |
| `-h` | Help message |

Example:
```bash
smtp-user-enum -M VRFY -u administrator -t 10.10.1.19
```
```
Starting smtp-user-enum v1.2 ( http://pentestmonkey.net/tools/smtp-user-enum )

-------------------------- Scan Information --------------------------

Mode ..................... VRFY
Worker Processes .......... 5
Target count .............. 1
Username count ............ 1
Target TCP port ........... 25
Query timeout .............. 5 secs
Target domain ..............

######## Scan started at Tue Mar 12 01:13:20 2024 ########
10.10.1.19: administrator exists
######## Scan completed at Tue Mar 12 01:13:20 2024 ########
1 results.

1 queries in 1 seconds (1.0 queries / sec)
```

### 5.6 SMTP Enumeration Using AI

**Prompt:** *"Perform SMTP enumeration on target IP 10.10.1.19."*
```bash
nmap -p25 --script smtp-enum-users --script-args smtp-enum-users.methods={VRFY,EXPN,RCPT} 10.10.1.19 -oN ~/enumeration_results/smtp_enum_10.10.1.19.txt
```
Runs `smtp-enum-users` against port 25 of the target, trying all three enumeration methods, and saves results to a timestamped file.

**Prompt:** *"Perform SMTP enumeration on target IP 10.10.1.19 with Metasploit."*
```bash
msfconsole -q -x "use auxiliary/scanner/smtp/smtp_enum; set RHOSTS 10.10.1.19; run; exit"
```
Runs Metasploit in quiet mode, loads the `smtp_enum` auxiliary module, sets the target, and executes.

---

## Part B: DNS Enumeration

### 5.7 DNS Enumeration Using Zone Transfer

**DNS zone transfer** is the process of copying a DNS zone file from a primary DNS server to a secondary one. In most setups, the secondary server holds a full backup of everything on the primary, purely for redundancy — and the DNS server uses zone transfer specifically to push changes made on the main server out to the secondary(s).

An attacker performs DNS zone transfer enumeration to locate the DNS server and access its records. **If the target's DNS server allows zone transfers**, an attacker can retrieve DNS server names, hostnames, machine names, usernames, IP addresses, aliases, and more — all assigned within that domain, in one shot.

To pull off a zone transfer, the attacker sends a zone-transfer request to the DNS server while pretending to be a legitimate client; the server then hands back a chunk of its database as a "zone." That zone can carry a huge amount of information about the DNS zone network. Common tools: `nslookup`, `dig`, and DNSRecon. If zone transfer is enabled on the target name server, it provides the DNS info directly; otherwise it returns an error saying the transfer failed or was refused.

#### `dig` Command (Linux)

Query DNS name servers to retrieve target host addresses, name servers, mail exchanges, etc.

```bash
# Retrieve all DNS name servers for the target domain
dig ns <target domain>

# Test whether one of those name servers allows zone transfer
dig @<domain of name server> <target domain> axfr
```

Example:
```bash
dig ns www.certifiedhacker.com
```
```
;; ANSWER SECTION:
www.certifiedhacker.com. 14400 IN  CNAME  certifiedhacker.com.
certifiedhacker.com.      21600 IN  NS     ns2.bluehost.com.
certifiedhacker.com.      21600 IN  NS     ns1.bluehost.com.
```
```bash
dig @ns1.bluehost.com www.certifiedhacker.com axfr
```
```
(1 server found)
Transfer failed.
```
(In this case zone transfer was correctly refused — a well-configured server. A misconfigured server would instead dump its full zone file.)

#### `nslookup` Command (Windows)

**Source:** https://docs.microsoft.com

```
nslookup
set querytype=soa
<target domain>
```
Sets the query type to Start of Authority (SOA) to retrieve administrative info about the DNS zone. Then, to attempt the actual zone transfer against a specific name server:
```
/ls -d <domain of name server>
```

Example:
```
C:\Users\Admin> nslookup
Default Server: dns.google
Address: 8.8.8.8

> set querytype=soa
> certifiedhacker.com
Server: dns.google
Address: 8.8.8.8

Non-authoritative answer:
certifiedhacker.com
        primary name server = ns1.bluehost.com
        responsible mail addr = dnsadmin.box5331.bluehost.com
        serial  = 2024031000
        refresh = 86400 (1 day)
        retry   = 7200 (2 hours)
        expire  = 3600000 (41 days 16 hours)
        default TTL = 300 (5 mins)

> ls -d ns1.bluehost.com
[dns.google]
*** Can't list domain ns1.bluehost.com: Server failed
The DNS server refused to transfer the zone ns1.bluehost.com to your computer. If this
is incorrect, check the zone transfer security settings for ns1.bluehost.com on the DNS
server at IP address 8.8.8.8.
```

#### DNSRecon

**Source:** https://github.com

Checks every NS record of the target domain for zone-transfer weaknesses.

```bash
dnsrecon -t axfr -d <target domain>
```
`-t` specifies the enumeration type (`axfr` tests every NS server for a zone transfer), `-d` specifies the target domain.

Example:
```bash
dnsrecon -t axfr -d certifiedhacker.com
```
```
[*] Checking for Zone Transfer for certifiedhacker.com name servers
[*] Resolving SOA Record
[+]     SOA ns1.bluehost.com 162.159.24.80
[*] Resolving NS Records
[*] NS Servers found:
[+]     NS ns2.bluehost.com 162.159.25.175
[+]     NS ns1.bluehost.com 162.159.24.80
[*] Removing any duplicate NS server IP Addresses...
[*]
[*] Trying NS server 162.159.25.175
[+] 162.159.25.175 Has port 53 TCP Open
[-] Zone Transfer Failed (Zone transfer error: NOTIMP)
[*]
[*] Trying NS server 162.159.24.80
[+] 162.159.24.80 Has port 53 TCP Open
[-] Zone Transfer Failed (Zone transfer error: NOTIMP)
```

### 5.8 DNS Cache Snooping

**DNS cache snooping** is a DNS enumeration technique where an attacker queries the DNS server for a specific *cached* DNS record. Because the cache reflects sites recently visited by real users, an attacker can use this to figure out the sites recently visited by that user population — potentially revealing the DNS server owner's identity, their service provider, vendor names, and even banking details, which can feed into a social-engineering attack on the target user. Common tools: `dig`, DNSRecon.

There are two DNS cache snooping methods:

#### Non-Recursive Method

To snoop, the attacker sends a **non-recursive** query by setting the Recursion Desired (RD) bit in the query header to zero. The attacker queries the DNS cache for a specific record type (A, CNAME, PTR, CERT, SRV, MX). If the queried record is present in the cache, the DNS server responds with information confirming that *some* user on the system visited that domain. Otherwise, the DNS server responds pointing to another DNS server that could answer the query, or replies with the `root.hints` file listing all root DNS servers.

```bash
dig @<IP of DNS server> <Target domain> A +norecurse
```

The `+norecurse` option sets the query to non-recursive. A `status: NOERROR` in the response implies the query was accepted but **no answer was returned** — meaning nobody from the system had visited the queried site.

Example:
```bash
dig @162.159.25.175 certifiedhacker.com A +norecurse
```
```
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 37348
;; flags: qr aa; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1
;; ANSWER SECTION:
certifiedhacker.com.   14400   IN   A   162.241.216.11
```
(Here an answer *was* returned, and the note in the source material flags this response — "indicates that the query is accepted, but the site is not cached" — describing the raw NOERROR/no-cache-hit case as distinct from a genuinely cached result.)

#### Recursive Method

To snoop this way, the attacker sends a **recursive** query using `+recurse` instead of `+norecurse`. Again the attacker queries the DNS cache for a record type (A, CNAME, PTR, CERT, SRV, MX), but this time the key signal is the **TTL field**:

- Compare the TTL value returned against the TTL originally set on that record.
- If the returned TTL is **less than** the original TTL, the record **is cached** — meaning someone on the system has visited that site.
- If the record wasn't already cached, it gets added to the cache after this very query.

```bash
dig @<IP of DNS server> <Target domain> A +recurse
```

Example:
```bash
dig @162.159.25.175 certifiedhacker.com A +recurse
```
```
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 39363
;; flags: qr aa rd; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1
;; WARNING: recursion requested but not available
;; ANSWER SECTION:
certifiedhacker.com.   14400   IN   A   162.241.216.11
```
Here the TTL value returned (14400, the full/original TTL) is considered **high**, which strongly suggests the record was **not** in the cache at the time the query was issued.

### 5.9 DNS Cache Snooping Using AI

**Prompt:** *"Use dig command to perform DNS cache snooping on target domain www.certifiedhacker.com using recursive method. Use DNS server IP as 162.241.216.11."*
```bash
dig @162.241.216.11 www.certifiedhacker.com +recurse
```

**Prompt:** *"Use dig command to perform DNS cache snooping on the target domain www.certifiedhacker.com using non-recursive method. Use DNS server IP as 162.241.216.11."*
```bash
dig @162.241.216.11 www.certifiedhacker.com +norecurse
```

In both cases the AI translates the plain-English instruction directly into the correct `dig` invocation with the right recursion flag and target/server IPs substituted in.

### 5.10 DNSSEC Zone Walking

**DNSSEC zone walking** is a DNS enumeration technique where an attacker attempts to obtain internal DNS-server records when the zone isn't configured properly. The enumerated zone data helps the attacker build a host network map.

Organizations deploy **DNSSEC** to add security features to DNS data, protecting against known DNS threats — it uses digital signatures based on public-key cryptography to strengthen authentication, and those signatures are stored in the DNS name servers alongside common records (MX, A, AAAA, CNAME).

**The catch:** while DNSSEC secures the internet layer, it's itself vulnerable to a technique called **zone enumeration** or **zone walking**. By exploiting this, attackers can extract network information about a target domain and use it as the basis for internet-based attacks.

To close this gap, a newer DNSSEC variant uses **Next Secure version 3 (NSEC3)**. NSEC3 records provide the same functionality as NSEC records except they use cryptographically hashed record names, specifically designed to prevent the enumeration of record names present in the zone.

Common zone-enumeration tools: **LDNS**, **DNSRecon**, **nsec3map**, **nsec3walker**, and **DNSwalk**.

#### LDNS

**Source:** https://www.nlnetlabs.nl

`LDNS-walk` enumerates the DNSSEC zone and obtains results on the DNS record files.

```bash
ldns-walk @<IP of DNS Server> <Target domain>
```

Example (against `nlnetlabs.nl` using DNS server `8.8.8.8`):
```bash
ldns-walk @8.8.8.8 nlnetlabs.nl
```
Returns a full enumerated DNS record file — every subdomain and its associated record types (A, NS, SOA, MX, TXT, AAAA, NAPTR, RRSIG, NSEC, DNSKEY, TLSA, etc.), including things like ACME-challenge subdomains, DANE/TLSA records, DKIM domain-key records, GitHub-challenge verification records, PGP-key/OpenPGP fingerprint records, and OTR fingerprint records.

#### DNSRecon

**Source:** https://www.github.com

Assists in enumerating DNS records (A, AAAA, CNAME) and can also perform **NSEC zone enumeration** to pull the DNS record files of a target domain.

```bash
dnsrecon -d <target domain> -z
```

Example:
```bash
dnsrecon -d www.certifiedhacker.com -z
```
```
[*] std: Performing General Enumeration against: www.certifiedhacker.com...
[-] DNSSEC is not configured for www.certifiedhacker.com
[*]      SOA ns1.bluehost.com 162.159.24.80
[*]      NS ns1.bluehost.com 162.159.24.80
[*]      Bind Version for 162.159.24.80 "2024.2.2"
[*]      NS ns2.bluehost.com 162.159.25.175
[*]      Bind Version for 162.159.25.175 "2024.2.2"
[*]      MX mail.certifiedhacker.com 162.241.216.11
[*]      CNAME www.certifiedhacker.com certifiedhacker.com
[*]      A certifiedhacker.com 162.241.216.11
[*]      TXT www.certifiedhacker.com v=spf1 a mx ptr include:bluehost.com ?all
[*] Enumerating SRV Records
[+] 0 Records Found
[*] Performing NSEC Zone Walk for www.certifiedhacker.com
[*] Getting SOA record for www.certifiedhacker.com
[*] Name Server 162.159.24.80 will be used
[*]      CNAME www.certifiedhacker.com certifiedhacker.com
[*]      A certifiedhacker.com 162.241.216.11
[+] 2 records found
```

### 5.11 DNS Enumeration Using OWASP Amass

**Source:** https://github.com

**OWASP Amass** is a DNS enumeration tool that lets attackers map the target network and discover potential attack surfaces. It combines both **active and passive** reconnaissance techniques to gather DNS info, and it's built specifically to enumerate critical information without triggering security alerts inside the target's DNS environment.

```bash
amass enum -d <Target Domain>
```
Gathers all DNS details — subdomains, IP addresses, SSL/TLS, HTTP, APIs, certificates, web archives, and data-scraping results tied to the target domain.

**Other OWASP Amass commands:**
```bash
# Passive enumeration only
amass enum -passive -d <Target Domain> -src

# Active enumeration through brute-forcing with a specified wordlist
amass enum -active -d <Target Domain> -brute -w /usr/share/wordlists/amass/all.txt

# Track/compare the last two enumeration scans for a target domain
amass track -config /root/amass/config.ini -dir amass4owasp -d <Target Domain> -last 2

# Display results stored in the amass database
amass db -dir amass4owasp -list

# Create a d3-force HTML visual graph of the results
amass viz -d3 -dir amass4owasp
```

Example run (via Docker):
```bash
docker run caffix/amass enum -d certifiedhacker.com
```
```
certifiedhacker.com (FQDN) --> mx_record --> mail.certifiedhacker.com (FQDN)
certifiedhacker.com (FQDN) --> ns_record --> ns2.bluehost.com (FQDN)
certifiedhacker.com (FQDN) --> ns_record --> ns1.bluehost.com (FQDN)
www.certifiedhacker.com (FQDN) --> cname_record --> certifiedhacker.com (FQDN)
ns2.bluehost.com (FQDN) --> a_record --> 162.159.25.175 (IPAddress)
soc.certifiedhacker.com (FQDN) --> a_record --> 162.241.216.11 (IPAddress)
www.itf.certifiedhacker.com (FQDN) --> a_record --> 162.241.216.11 (IPAddress)
sftp.certifiedhacker.com (FQDN) --> a_record --> 162.241.216.11 (IPAddress)
162.241.216.0/24 (Netblock) --> contains --> 162.241.216.11 (IPAddress)
162.159.25.0/24 (Netblock) --> contains --> 162.159.25.175 (IPAddress)
26337 (ASN) --> managed_by --> OIS1 - Oso Grande IP Services, LLC (RIROrganization)
26337 (ASN) --> announces --> 162.241.216.0/24 (Netblock)
13335 (ASN) --> managed_by --> CLOUDFLARENET - Cloudflare, Inc. (RIROrganization)
13335 (ASN) --> announces --> 162.159.25.0/24 (Netblock)
```

### 5.12 DNS and DNSSEC Enumeration Using Nmap

**DNS Enumeration**

Attackers use Nmap to scan domains and obtain a list of subdomains, records, IP addresses, and other valuable information from the target host.

```bash
# List all available DNS-related services on the target host
nmap --script=broadcast-dns-service-discovery <Target Domain>
```

```bash
# Retrieve all subdomains associated with the target host
nmap -T4 -p 53 --script dns-brute <Target Domain>
```

Example:
```bash
nmap -T4 -p 53 --script dns-brute certifiedhacker.com
```
```
Host script results:
| dns-brute:
|   DNS Brute-force hostnames:
|     news.certifiedhacker.com - 162.241.216.11
|     mail.certifiedhacker.com - 162.241.216.11
|     blog.certifiedhacker.com - 162.241.216.11
|     www.certifiedhacker.com - 162.241.216.11
|     ftp.certifiedhacker.com - 162.241.216.11
|     smtp.certifiedhacker.com - 162.241.216.11
|_    demo.certifiedhacker.com - 162.241.216.11
```
Any wildcard entries in this list show as `*A*` for IPv4 or `*AAAA*` for IPv6.

```bash
# Check whether DNS recursion is enabled on the target server
nmap -Pn -sU -p 53 --script=dns-recursion 192.168.1.150
```

**DNSSEC Enumeration**

Attackers enumerate DNSSEC using the `dns-nsec-enum.nse` or `dns-nsec3-enum.nse` NSE scripts to obtain info about domains and their sub-domains.

```bash
# Retrieve the list of subdomains associated with the target domain
nmap -sU -p 53 --script dns-nsec-enum --script-args dns-nsec-enum.domains=eccouncil.org <target>
```

Example against a domain with no NSEC records configured:
```bash
nmap -sU -p 53 --script dns-nsec-enum --script-args dns-nsec-enum.domains=certifiedhacker.com 162.159.25.175
```
```
PORT    STATE SERVICE
53/udp  open  domain
| dns-nsec-enum:
|_  No NSEC records found
```

**Additional DNS enumeration tools:**
| Tool | Source |
|---|---|
| Knock | https://github.com |
| Raccoon | https://github.com |
| Subfinder | https://github.com |
| Turbolist3r | https://github.com |

### 5.13 DNS Enumeration with AI

**Prompt:** *"Use Nmap to perform DNS Enumeration on target domain www.certifiedhacker.com"*
```bash
nmap --script dns-brute --script-args dns-brute.domain=certifiedhacker.com -oN ~/enumeration_results/dns_brute_certifiedhacker.txt && nmap --script dns-zone-transfer -p 53 certifiedhacker.com -oN ~/enumeration_results/dns_zonetransfer_certifiedhacker.txt
```
This chains two Nmap scans together:
1. `dns-brute` against `certifiedhacker.com`, saving results to `dns_brute_certifiedhacker.txt`
2. `dns-zone-transfer` on port 53 against the same domain, saving results to `dns_zonetransfer_certifiedhacker.txt`

Both outputs land in `~/enumeration_results/` — a single AI prompt effectively automates the brute-force subdomain sweep and the zone-transfer attempt back to back.

---

**Next:** [`06-other-enumeration-techniques.md`](06-other-enumeration-techniques.md) — IPsec, VoIP, RPC, Unix/Linux user, and SMB enumeration.
