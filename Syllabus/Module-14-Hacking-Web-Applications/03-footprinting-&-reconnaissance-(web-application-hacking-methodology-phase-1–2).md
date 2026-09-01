# 03 — Footprinting & Reconnaissance (Web Application Hacking Methodology, Phase 1–2)

> Every real engagement starts here. Before you can attack anything, you need to know what's actually running, where it's hosted, what technology built it, and what's exposed. This file covers the first two phases of the CEH web-app-hacking methodology: **Footprint Web Infrastructure** and **Analyze Web Applications**.
>
> ⚠️ **Authorization note:** every command below assumes you have written authorization to test the target (a pentest engagement letter, a bug-bounty program's in-scope asset, or your own lab). Running these against systems you don't have permission to test is illegal in virtually every jurisdiction.

## Table of Contents
- [The Full Methodology at a Glance](#the-full-methodology-at-a-glance)
- [Server & Service Discovery](#server--service-discovery)
- [Banner Grabbing](#banner-grabbing)
- [Detecting Firewalls, WAFs, and Load Balancers](#detecting-firewalls-wafs-and-load-balancers)
- [Hidden Content & Directory Discovery](#hidden-content--directory-discovery)
- [Detecting Web Application Technologies](#detecting-web-application-technologies)
- [Website Mirroring](#website-mirroring)
- [Identifying Entry Points for User Input](#identifying-entry-points-for-user-input)
- [Extracting Metadata from Public Documents](#extracting-metadata-from-public-documents)
- [Gathering a Target-Specific Wordlist](#gathering-a-target-specific-wordlist)
- [Monitoring Web Pages for Updates and Changes](#monitoring-web-pages-for-updates-and-changes)
- [Using AI to Accelerate Recon](#using-ai-to-accelerate-recon)

---

## The Full Methodology at a Glance

```
1.  Footprint Web Infrastructure
2.  Analyze Web Applications (attack surface mapping)
3.  Bypass Client-Side Controls
4.  Attack Authentication Mechanism
5.  Attack Authorization Schemes
6.  Attack Access Controls
7.  Attack Session Management Mechanism
8.  Perform Injection / Input-Validation Attacks
9.  Attack Application Logic Flaws
10. Attack Shared Environments
11. Attack Database Connectivity
12. Attack the Web Application Client
13. Attack Web Services
```
Steps 1–2 are covered here. Steps 3–13 are covered across [05](./05-xss-csrf-and-client-side-attacks.md), [06](./06-session-authentication-and-authorization-attacks.md), [04](./04-injection-attacks.md), [08](./08-other-web-app-attacks.md), and [07](./07-web-services-api-and-webhook-attacks.md).

## Server & Service Discovery

**Goal:** figure out what's actually listening, on which host, on which ports.

```bash
# Basic host resolution and organizational info
whois target.com
nslookup target.com
dig target.com ANY
dig target.com MX
dig target.com NS

# Zone transfer attempt (works only if the DNS server is misconfigured)
dig axfr target.com @ns1.target.com

# Full TCP/UDP port + service/version scan
nmap -sS -sV -p- -T4 target.com
nmap -sU --top-ports 50 target.com

# Fast, high-confidence web-focused scan
nmap -sV -p 80,443,8080,8443 --script=http-enum,http-title,http-headers target.com
```

**DNS interrogation** — enumerating subdomains widens the attack surface enormously (dev/staging subdomains are frequently far less hardened than production):
```bash
# Brute-force subdomains with a wordlist
gobuster dns -d target.com -w subdomains.txt

# Passive subdomain enumeration (no direct traffic to the target)
amass enum -passive -d target.com
subfinder -d target.com -silent
```

## Banner Grabbing

Banners leak the exact software and version in use — the single most useful piece of information for matching against a public exploit database.

**HTTP banner grabbing with `telnet` or `curl`:**
```bash
telnet target.com 80
GET / HTTP/1.0
[press Enter twice]

# Equivalent with curl (safer, scriptable)
curl -I http://target.com
```
Typical output reveals the web server and framework:
```
HTTP/1.1 200 OK
Server: Microsoft-IIS/10.0
X-Powered-By: ASP.NET
```

**Banner grabbing over SSL/TLS with OpenSSL** (telnet/netcat can't do this over an encrypted channel):
```bash
openssl s_client -connect target.com:443
# then issue a raw request once connected:
GET / HTTP/1.1
Host: target.com
```

**Netcat equivalent:**
```bash
nc -v target.com 80
HEAD / HTTP/1.1
Host: target.com
[press Enter twice]
```

**ID Serve / httprecon** — Windows GUI tools that fingerprint web server type even when the `Server` header has been deliberately obscured, by analyzing subtle protocol-implementation differences (header ordering, response to malformed requests, etc.).

## Detecting Firewalls, WAFs, and Load Balancers

**WAF detection with `wafw00f`:**
```bash
wafw00f https://target.com
```
This sends a series of probes designed to trigger a WAF's blocking behavior, then fingerprints the WAF vendor from the resulting response signature (block page, status code, headers like `X-Sucuri-ID` or `cf-ray`).

**Manual WAF fingerprinting:**
```bash
curl -s -A "() { :; }; echo VULNERABLE" https://target.com/   # Shellshock-style probe
curl -s "https://target.com/?id=1' OR '1'='1"                  # look for a generic block page
```

**Load balancer detection:**
```bash
# Multiple distinct IPs on repeated resolution can indicate round-robin DNS load balancing
dig target.com +short
dig target.com +short
dig target.com +short

# lbd (Load Balancing Detector) — checks both DNS- and HTTP-based load balancing
lbd target.com

# TTL/response-time anomalies across repeated requests to the same URL can also reveal
# multiple backend servers behind a single virtual IP
for i in {1..5}; do curl -s -o /dev/null -w "%{time_total}\n" https://target.com; done
```

## Hidden Content & Directory Discovery

**Goal:** find files, directories, and endpoints that aren't linked from the visible UI (backup files, admin panels, forgotten debug endpoints, API routes).

**Gobuster** (Go-based, very fast):
```bash
gobuster dir -u https://target.com -w common.txt
gobuster dir -u https://target.com -w common.txt -s 200,301,302   # filter by status code
gobuster dir -u https://target.com -w common.txt -x php,bak,zip,old -t 50
```

**dirb:**
```bash
dirb https://target.com
dirb https://target.com /usr/share/wordlists/dirb/big.txt -X .php,.bak
```

**ffuf** (fast, flexible, good for parameter and vhost fuzzing too):
```bash
ffuf -u https://target.com/FUZZ -w common.txt
ffuf -u https://target.com/FUZZ -w common.txt -mc 200,301,302,403 -t 100
# Virtual host fuzzing:
ffuf -u https://target.com -H "Host: FUZZ.target.com" -w subdomains.txt -fs <size-of-default-response>
```

**wfuzz** (older but flexible for parameter discovery):
```bash
wfuzz -c -z file,common.txt --hc 404 https://target.com/FUZZ
```

**Snispet — `robots.txt` and `sitemap.xml` are free intel:**
```bash
curl https://target.com/robots.txt
curl https://target.com/sitemap.xml
```

## Detecting Web Application Technologies

Knowing exactly which CMS, framework, JS libraries, analytics tags, and server software power a site tells you which known vulnerabilities and default paths to try first.

```bash
whatweb https://target.com                 # CLI fingerprinting: CMS, JS libs, server, cookies
whatweb -v https://target.com               # verbose, shows plugin-by-plugin match confidence
```
**Wappalyzer** — browser extension and CLI/API version that reads page markup, headers, and JS globals to identify hundreds of technologies (analytics, CDN, CMS, e-commerce platform, JS framework).

**BuiltWith** — web-based technology profiler (https://builtwith.com) useful when you'd rather not send extra traffic to the target yet.

```bash
# Nmap's HTTP NSE scripts are also excellent technology fingerprinting tools:
nmap -p80,443 --script=http-generator,http-wordpress-enum,http-drupal-enum target.com
```

**WebSocket enumeration** — modern apps increasingly use WebSockets for real-time features; tools like **STMS** and **Burp Suite's WebSocket history panel** let you observe and replay WebSocket frames.

## Website Mirroring

Downloading a full local copy of the target lets you search offline, at leisure, for comments, hard-coded secrets, and hidden links without generating further traffic against the live target.

```bash
# HTTrack — full offline website copier
httrack https://target.com -O ./mirror

# wget — recursive mirror
wget --mirror --convert-links --adjust-extension --page-requisites --no-parent https://target.com
```
After mirroring, grep the local copy for interesting strings:
```bash
grep -r -i "api_key\|password\|secret\|TODO\|FIXME" ./mirror
```

## Identifying Entry Points for User Input

Every place a web application accepts input is a candidate attack surface: URL parameters, form fields, HTTP headers (`User-Agent`, `Referer`, `X-Forwarded-For`), cookies, file uploads, and JSON/XML request bodies.

**Workflow with Burp Suite (or OWASP ZAP) as an intercepting proxy:**
1. Configure the browser to route traffic through the proxy (`127.0.0.1:8080` for Burp by default).
2. Browse the entire application manually, clicking every link and submitting every form, so the proxy's site map captures every endpoint.
3. Review **Target → Site map** for every parameter, header, and cookie the app reads.
4. Send interesting requests to **Repeater** for manual parameter manipulation, or to **Intruder** for automated fuzzing.

## Extracting Metadata from Public Documents

Publicly-hosted documents (PDF, DOCX, XLSX, PPTX) frequently retain metadata that reveals usernames, internal software versions, and file-system paths.

```bash
# Metagoofil — harvests public documents from a domain via search engines, then extracts metadata
metagoofil -d target.com -t pdf,doc,xls,ppt -l 100 -n 20 -o results -f results.html

# exiftool on a single already-downloaded document
exiftool report.pdf
```
**FOCA** (Windows GUI) automates the same workflow: search-engine discovery → download → metadata extraction → username/software-version correlation.

## Gathering a Target-Specific Wordlist

Generic wordlists (`rockyou.txt`, SecLists) are a starting point, but a wordlist built from the target's *own* content finds hits generic lists miss (internal product names, jargon, employee names).

```bash
# CeWL — spiders a site and builds a wordlist from the words it finds
cewl https://target.com -d 3 -m 5 -w target_wordlist.txt

# Combine with a mangler (e.g., hashcat rules) to generate password-style permutations
```

## Monitoring Web Pages for Updates and Changes

Tracking when and how a target's pages change over time can reveal new features being rolled out, staging deployments going live briefly, or reverted security fixes.

- **WebSite-Watcher** — desktop tool that diffs pages on a schedule and alerts on changes.
- **Wget + cron + diff** — a free, scriptable equivalent:
```bash
wget -q -O snapshot_$(date +%F).html https://target.com/pricing
diff snapshot_2026-08-30.html snapshot_2026-08-31.html
```
- Checking **archive.org's Wayback Machine** for historical snapshots is a zero-traffic way to see how an application's structure evolved (and sometimes recover long-removed but still-functional endpoints).

## Using AI to Accelerate Recon

Modern practice increasingly uses LLM-driven automation to orchestrate the tools above. The pattern is: describe the goal in natural language, let an AI assistant translate that into tool invocations and parse the output.

Example prompts used against an AI coding/ops assistant during recon:
```
"Perform a vulnerability scan on the target url www.target.com"
"Perform a vulnerability scan on the target url www.target.com using nmap"
"Install Sn1per and scan the target url www.target.com for web vulnerabilities, save results to scan.txt"
```
AI-assisted vulnerability scanners such as **Sn1per** chain together dozens of the individual tools above (subdomain enumeration, port scanning, tech fingerprinting, screenshotting, vulnerability lookups) into a single automated workflow — useful for quickly triaging a large scope, but always validate automated findings manually before reporting them.

```bash
# Sn1per basic usage
sniper -t target.com -o                 # OSINT mode
sniper -t target.com -m stealth         # low-and-slow scan
sniper -t target.com -m normal          # full scan
```

---

**Previous:** [← 02 — OWASP Top 10 & Web Threats](./02-owasp-top-10-and-web-threats.md) · **Next:** [04 — Injection Attacks →](./04-injection-attacks.md)
