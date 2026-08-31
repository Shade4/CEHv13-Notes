# 03 — Attack Methodology: Reconnaissance & Footprinting

> Objective covered: **Explain Web Server Attack Methodology** (Phases 1–2)

A web server attack typically follows a **preplanned methodology** that an attacker follows to reach the goal of breaching the target web server's security. Attackers hack a web server in multiple stages.

## The 6-Phase Web Server Attack Methodology

| # | Phase | Purpose |
|---|---|---|
| 1 | **Information Gathering** | Collect as much information as possible about the target web server |
| 2 | **Web Server Footprinting** | Determine the server's remote access capabilities, its ports and services, and other aspects of its security |
| 3 | **Website Mirroring** | Copy a website and its content onto another server for offline browsing/detailed structural analysis |
| 4 | **Vulnerability Scanning** | Find vulnerabilities and misconfigurations of a web server with automated tools |
| 5 | **Session Hijacking** | Perform session hijacking after identifying the current session of the client, taking control over the user session |
| 6 | **Web Server Passwords Hacking** | Use password-cracking methods such as brute-force, hybrid, and dictionary attacks to crack the web server's password |

This file covers **Phases 1 & 2**. Phase 3 is in [04](04-directory-bruteforcing-and-mirroring.md), Phase 4 is in [05](05-vulnerability-scanning-and-exploitation.md), and Phases 5–6 are in [06](06-session-hijacking-and-password-cracking.md).

---

## Phase 1 — Information Gathering

Information gathering is the **first and one of the most important steps** toward targeting a web server. In this step, an attacker collects as much information as possible about the target using various tools and techniques. The information obtained from this step helps the attacker in assessing the security posture of the target organization. Attackers search newsgroups, bulletin boards, and so on for gathering information about the target organization. Attackers can also use tools such as **who.is** and **Whois Lookup** to extract information such as the target's domain name, IP address, and autonomous system number.

### `who.is`

- **Source:** https://who.is
- Designed to perform a variety of whois lookup functions. Lets the user perform a domain whois search, whois IP lookup, and whois database search for relevant information on domain registration and availability.

```bash
# Example CLI equivalent (Linux whois client)
whois certifiedhacker.com
```

### Additional Information-Gathering Tools

| Tool | Source |
|---|---|
| Whois Lookup | https://whois.domaintools.com |
| Whois | https://www.whois.com |
| Domain Dossier | https://centralops.net |
| Subdomain Finder | https://pentest-tools.com |

> 📖 **Cross-reference:** see **Module 02: Footprinting and Reconnaissance** for complete coverage of information-gathering techniques.

### Information Gathering from `robots.txt`

- A website owner creates a `robots.txt` file to **list the files/directories** a web crawler should (or should not) index for search purposes.
- **Poorly written `robots.txt` files can cause the complete indexing of website files and directories** — an attacker may easily obtain information such as passwords, email addresses, hidden links, and membership areas from a target's robots.txt file.
- If the owner writes `robots.txt` without allowing indexing of restricted pages, an attacker can still **view the robots.txt file itself** to discover restricted files and directory names.
- An attacker types `URL/robots.txt` in a browser's address bar to view the target website's `robots.txt` file.
- An attacker can also **download** the robots.txt file of a target website using the **Wget** tool.

```bash
# Fetch a target's robots.txt directly
curl https://target.com/robots.txt

# Or with wget
wget https://target.com/robots.txt -O robots.txt
```

Typical robots.txt content that leaks structure (e.g. a "hidden" admin path):
```
User-agent: Googlebot
Disallow: /
User-agent: googlebot-image
Disallow: /
User-agent: googlebot-mobile
Disallow: /
User-agent: MSNBot
Disallow: /
User-agent: Slurp
Disallow: /
User-agent: Teoma
Disallow: /
User-agent: Gigabot
Disallow: /
User-agent: ia_archiver
Disallow: /
User-agent: baiduspider
Disallow: /
User-agent: naverbot
Disallow: /
User-agent: Yeti
Disallow: /
User-agent: Yahoo-mmcrawler
Disallow: /
```

---

## Phase 2 — Web Server Footprinting / Banner Grabbing

By performing web server footprinting, an attacker can footprint valuable system-level data such as account details, operating system, software versions, server names, and database schema details. Footprinting tools such as **httprecon**, **Uniscan**, and **Netcraft** can extract this information from the target server.

### Netcat

- **Source:** https://netcat.sourceforge.net
- A networking utility that reads and writes data across network connections using the TCP/IP protocol. Also useful as a network debugging and exploration tool.

```bash
# Banner-grab www.moviescope.com on port 80
nc -vv www.moviescope.com 80
GET / HTTP/1.0
# (press Enter twice)
```

**Sample output (captured live):**
```
$nc -vv www.moviescope.com 80
DNS fwd/rev mismatch: www.moviescope.com != www.goodshopping.com
www.moviescope.com [10.10.1.19] 80 (http) open
GET / HTTP/1.0

HTTP/1.1 200 OK
Content-Type: text/html
Last-Modified: Wed, 15 Apr 2020 06:15:03 GMT
Accept-Ranges: bytes
ETag: "2a415933ed12d61:0"
Server: Microsoft-IIS/10.0
X-Powered-By: ASP.NET
Date: Thu, 14 Mar 2024 05:51:26 GMT
```
→ **Server identified as Microsoft-IIS/10.0**

### Telnet

- **Source:** https://learn.microsoft.com
- A client–server network protocol widely used on the internet/LANs. Provides login sessions for a user on the internet — a single terminal attached to another computer emulates the session using Telnet.

**Primary security issues with Telnet:**
- It does not encrypt data sent through the connection.
- It lacks an authentication scheme.

Telnet enables an attacker to perform a banner-grabbing attack — it probes HTTP servers to determine the `Server` field in the HTTP response header.

```bash
# Request Telnet to connect to a host on a specific port
telnet www.moviescope.com 80
# A blank screen appears. Then type and press Enter twice:
GET / HTTP/1.0
```
The HTTP server responds with the same kind of banner information shown above via Netcat.

### httprecon

- **Source:** https://www.computec.ch
- A tool for advanced web server fingerprinting: banner-grabbing attacks, status code enumeration, and header ordering analysis.

**Test cases httprecon performs on the target web server:**
- A legitimate GET request for an existing resource
- An exceedingly long GET request for an existing resource (a URI of >1024 bytes)
- A common GET request for a non-existing resource
- A common HEAD request for an existing resource
- Enumeration with OPTIONS, which is usually not permitted
- The HTTP method DELETE, which is usually not permitted
- The HTTP method TEST, which is not defined
- The protocol version HTTP/9.8, which does not exist
- A GET request including attack patterns (e.g. `:`, `../`, `%%`)

### Uniscan

- **Source:** https://sourceforge.net
- A versatile server fingerprinting tool that not only performs simple commands such as ping, traceroute, and nslookup, but also conducts static, dynamic, and stress checks on web servers. In addition, Uniscan performs automated Bing and Google searches for specific IPs. It compiles all this data into a comprehensive report file.

### Additional Footprinting Tools

| Tool | Source |
|---|---|
| Netcraft | https://www.netcraft.com |
| ID Serve | https://www.grc.com |
| Ghost Eye | https://github.com |
| Skipfish | https://code.google.com |

---

## AI-Assisted Web Server Footprinting

Attackers can leverage AI-powered technologies to enhance and automate hacking. With the aid of AI, attackers can effortlessly perform web server footprinting on target servers by using an appropriate natural-language prompt.

### Example 1 — Compound Nmap + WhatWeb + Nikto scan

**Prompt:** *"Perform webserver footprinting on target IP 10.10.1.22"*

**Resulting command:**
```bash
nmap -sV 10.10.1.22 && whatweb 10.10.1.22 && nikto -h 10.10.1.22
```

| Tool | Flags | What it does |
|---|---|---|
| **Nmap** | `-sV 10.10.1.22` | `-sV` enables version detection, attempting to determine the version of services running on open ports. Scans the target IP to detect open ports and service versions. |
| **WhatWeb** | `10.10.1.22` | A web scanner that identifies websites built with — by providing the target IP, WhatWeb will attempt to gather information about the web server and technologies used on the target website. |
| **Nikto** | `-h 10.10.1.22` | `-h` specifies the target host to scan. Nikto performs comprehensive tests on web servers for multiple items, including dangerous files/CGIs, outdated server software, and other potential security issues. |

**Real Nikto fragment captured against the lab target:**
```
+ Server: Microsoft-IIS/10.0
+ /: Retrieved x-powered-by header: ASP.NET.
+ /: The anti-clickjacking X-Frame-Options header is not present.
+ /: The X-Content-Type-Options header is not set.
+ /78dDfnqG.aspx: Retrieved x-aspnet-version header: 4.0.30319.
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ OPTIONS: Allowed HTTP Methods: OPTIONS, TRACE, GET, HEAD, POST .
+ 8226 requests: 0 error(s) and 6 item(s) reported on remote host
```

### Example 2 — Footprinting with Netcat via AI

**Prompt:** *"Perform webserver footprinting on target IP 10.10.1.22 with netcat"*

**Resulting command (a raw HTTP `HEAD` request built as a heredoc):**
```bash
nc -v 10.10.1.22 80 <<EOF
HEAD / HTTP/1.1
Host: 10.10.1.22

EOF
```

| Part | Meaning |
|---|---|
| `nc -v 10.10.1.22 80` | Initiates a connection to `10.10.1.22` on port 80. `-v` = verbose mode. |
| `HEAD / HTTP/1.1` | The HTTP request line — HEAD method, path `/`, protocol version HTTP/1.1. |
| `Host: 10.10.1.22` | Required `Host` header for the request. |
| `<<EOF ... EOF` | Bash heredoc syntax — everything between the two `EOF` markers is sent as the request body over the established `nc` connection. |

> 📝 **Note (added):** in the courseware's own worked example, the actual literal request line shown was `HEAD/HTTP/1.1` (missing the required space between the method and the path) — that's a typo in the source slide. The syntactically-correct line is `HEAD / HTTP/1.1` as written above; a missing space would cause most servers to return a `400 Bad Request` instead of the intended banner.

---

## Shodan Dorks for IIS Information Gathering

Gathering information on IIS servers via **Shodan** provides attackers with crucial details for planning and executing further attacks. By identifying the version of IIS used, attackers can match known vulnerabilities with server configurations, revealing weak points.

| Shodan Filter | Purpose |
|---|---|
| `http.title:"IIS"` | Search for any IIS server and get a list of instances |
| `ssl:"Company Inc." http.title:"IIS"` | Identify IIS servers with SSL certificates issued to a specific organization |
| `http.title:"IIS Windows Server" country:"US"` | Identify IIS servers in the US (geographically-targeted attacks) |
| `http.title:"IIS7" port:80` | Locate IIS7 servers running on port 80 |
| `http.title:"IIS7" net:"<IP_address>/24"` | Search for IIS7 servers within a specific IP range (network-specific info gathering) |
| `http.title:"IIS7"` | Identifies IIS servers running version 7 — useful for finding version-specific vulnerabilities |
| `http.title:"IIS Windows Server"` | Targets IIS servers on Windows, helpful for Windows-specific exploitation |
| `http.title:"Internet Information Services"` | Broad search for any IIS servers, useful for general information gathering |

Attackers review the search results to gather information such as IP addresses, open ports, running services, and version details. They can click on individual results for detailed server information (HTTP headers, SSL certificates, metadata), and use Shodan's export features to save data as CSV/JSON for further analysis.

---

## Abusing Apache `mod_userdir` to Enumerate User Accounts

Attackers can exploit Apache's **`mod_userdir`** module to enumerate user accounts on a web server. This module allows access to user directories using URIs formatted as `/~username/`. Using Nmap, attackers can identify valid usernames, which can aid in brute-forcing or targeted phishing.

**Perform Initial Scan to Enumerate Valid Users:**
```bash
nmap -p80 --script http-userdir-enum <target>
```
Scans port 80 using the `http-userdir-enum` script to list usernames matching the built-in default word list (`usernames.lst`, located at `/nselib/data/`).

**Perform Customized Scan:**
```bash
nmap -p80 --script http-userdir-enum --script-args userdir.users=<Wordlist>.txt <target>
```
Takes the `.txt` file as a source for usernames and tests each against the target.

**Bypass Detection with Custom User Agent:**
```bash
nmap -p80 --script http-brute --script-args http.useragent="<User_Agent>" <target>
```
Some security systems detect and block requests from Nmap because of its default user-agent string. This command changes the HTTP User-Agent string used by Nmap to a specified string, making the traffic appear to originate from a standard web browser rather than a scanning tool.

---

## Enumerating Web Server Information Using Nmap (Full NSE Arsenal)

**Source:** https://nmap.org

Nmap, along with the **Nmap Scripting Engine (NSE)**, can extract a large amount of valuable information from the target web server.

```bash
# Discover virtual domains with hostmap
nmap --script hostmap-bfk <host>

# Detect a vulnerable server that uses the TRACE method
nmap --script http-trace -p80 localhost

# Harvest email accounts with http-google-email
nmap --script http-google-email <host>

# Enumerate users with http-userdir-enum
nmap -p80 --script http-userdir-enum localhost

# Detect HTTP TRACE
nmap -p80 --script http-trace <host>

# Check if the web server is protected by a WAF or IPS
nmap -p80 --script http-waf-detect \
  --script-args="http-waf-detect.uri=/testphp.vulnweb.com/artists.php,http-waf-detect.detectBodyChanges" \
  www.modsecurity.org

# Fingerprint a WAF
nmap --script=http-waf-fingerprint -p80,443 <host>

# Enumerate common web applications
nmap --script http-enum -p80 <host>

# Obtain robots.txt
nmap -p80 --script http-robots.txt <host>
```

**Additional Nmap commands used to extract web server information:**
```bash
nmap -sV -O -p <target IP address>
nmap -sV --script http-enum <target IP address>
nmap <target IP address> -p 80 --script=http-frontpage-login
nmap --script http-passwd --script-args http-passwd.root=/ <target IP address>
```

**Real captured output — enumerating an unauthenticated IIS box:**
```
# sudo su
# nmap -sV --script=http-enum www.goodshopping.com
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-03-13 08:11 EDT
Nmap scan report for www.goodshopping.com (10.10.1.19)
Host is up (0.0012s latency).
Not shown: 990 filtered tcp ports (no-response)
PORT     STATE SERVICE      VERSION
25/tcp   open  smtp         Microsoft ESMTP 10.0.17763.1
80/tcp   open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
| http-server-header:
|   Microsoft-HTTPAPI/2.0
|_  Microsoft-IIS/10.0
| http-enum:
|_  /login.aspx: Possible admin folder
135/tcp  open  msrpc        Microsoft Windows RPC
139/tcp  open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds?
1801/tcp open  msmq?
2103/tcp open  msrpc        Microsoft Windows RPC
2105/tcp open  msrpc        Microsoft Windows RPC
2107/tcp open  msrpc        Microsoft Windows RPC
3389/tcp open  ms-wbt-server Microsoft Terminal Services
MAC Address: 02:15:5D:55:A2:80 (Unknown)
Service Info: Host: Server2019; OS: Windows; CPE: cpe:/o:microsoft:windows
```

### Finding Default Credentials of a Web Server

Administrators/security personnel use administrative interfaces to securely configure, manage, and monitor web application servers. Many of these interfaces are publicly accessible and remain set to default. Attackers attempt to identify the running administrative interface via port scanning, then apply these techniques:

- Consult the administrative interface documentation to identify default passwords
- Use **Metasploit's** built-in database to scan the server
- Use online resources such as **cirt.net** (https://cirt.net/passwords) and **FortyPoundHead.com** (https://www.fortypoundhead.com) to identify default passwords
- Attempt password-guessing and brute-forcing attacks

**Additional default-password resources:**
| Site |
|---|
| https://www.fortypoundhead.com |
| https://www.defaultpassword.com |
| https://default-password.info |
| https://www.routerpasswords.com |

### Finding Default Content of a Web Server

Most servers ship with default content and functionality that attackers target:

- **Administrator debug and test functionality** — used to debug, diagnose, and test web applications; often contain useful configuration information and the runtime state of both the server and its applications.
- **Sample functionality to demonstrate common tasks** — many servers contain sample scripts/pages to demonstrate application server functions and APIs. Sample scripts fail to secure these scripts from being exploited by attackers, or implement functionalities that allow attackers exploits.
- **Publicly accessible powerful functions** — some servers include powerful functionalities that are intended for administrative and restricted use. Attackers attempt to exploit such powerful functions to compromise the server and gain access. For example, some application servers allow web archives to be deployed over an HTTP interface used by the application; attackers can leverage common exploitation frameworks (such as Metasploit) to perform scanning, identify default passwords, upload backdoors, and gain command-shell access to the target server.
- **Server installation manuals** — an attacker who identifies server manuals may find configuration and installation information; this can help prepare an appropriate framework to exploit the installed server.

**Nikto2:**
- **Source:** https://cirt.net
- A vulnerability scanner used extensively to identify potential vulnerabilities in web applications and web servers, including default content, dangerous files/CGIs, and outdated server software.

```bash
nikto -h 10.10.1.19
```

**Real captured Nikto2 output fragment:**
```
- Nikto v2.5.0
+ Target IP:          10.10.1.19
+ Target Hostname:    www.moviescope.com
+ Target Port:        80
+ Start Time:         2024-03-13 07:33:14 (GMT-4)
+ Server: Microsoft-IIS/10.0
+ /: Retrieved x-powered-by header: ASP.NET.
+ The anti-clickjacking X-Frame-Options header is not present.
+ The X-Content-Type-Options header is not set.
+ OPTIONS: Allowed HTTP Methods: OPTIONS, TRACE, GET, HEAD, POST .
+ 8817 requests: 0 error(s) and 6 item(s) reported on remote host
+ End Time:           2024-03-13 07:41:57 (GMT-4) (2 minutes)
```

### Directory Brute Forcing

When a web server receives a request for a directory rather than a file, it responds in one of these ways:

- **Return default resource within the directory** (e.g. `index.html`)
- **Return an error** (e.g. HTTP status code 403, "not permitted")
- **Return a listing of directory content**

Attackers exploit poor server configuration to enumerate directory listings and mine them for sensitive files. This topic continues in [04 — Directory Brute-Forcing & Mirroring →](04-directory-bruteforcing-and-mirroring.md).

---

**Previous:** [← 02 — Web Server Attack Techniques](02-web-server-attack-techniques.md) · **Next:** [04 — Directory Brute-Forcing & Mirroring →](04-directory-bruteforcing-and-mirroring.md)
