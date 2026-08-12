# Module 2: Footprinting and Reconnaissance
## Part B — Footprinting Through Search Engines

[← Back to Part A: Footprinting Concepts](01-footprinting-concepts.md) | [Next: Footprinting Through Internet Research Services →](03-footprinting-through-internet-research-services.md)

---

## Table of Contents

1. [Why Search Engines Matter for Footprinting](#why-search-engines-matter-for-footprinting)
2. [Advanced Google Hacking Techniques](#advanced-google-hacking-techniques)
3. [What an Attacker Can Do With Google Hacking](#what-an-attacker-can-do-with-google-hacking)
4. [AI-Assisted Google Hacking](#ai-assisted-google-hacking)
5. [The Google Hacking Database (GHDB)](#the-google-hacking-database-ghdb)
6. [Footprinting Through the Shodan Search Engine](#footprinting-through-the-shodan-search-engine)
7. [Other Search-Engine Footprinting Techniques](#other-search-engine-footprinting-techniques)
8. [Quick-Reference Summary](#quick-reference-summary)

---

## Why Search Engines Matter for Footprinting

Search engines are one of the richest sources of information about a target organization, precisely because of how they work: automated crawlers continuously scan active websites and index the results into a massive database. When a user (or an attacker) submits a query, the engine returns ranked Search Engine Results Pages (SERPs) — web pages, images, videos, and countless file types, all sorted by relevance.

For an attacker, this index can surface technology platforms in use, employee details, login pages, intranet portals, and contact information — all useful raw material for social engineering and more advanced system attacks. Major search engines used for this purpose include Google, Bing, Yahoo, Ask, AOL, Baidu, Yandex, WolframAlpha, and DuckDuckGo. Even a simple query like "top job portals" can surface further sources of information about a target's hiring patterns and internal structure.

As a defensive note: if an ethical hacker finds deleted pages or sensitive information about their own company still sitting in a search engine's cache, most engines provide a mechanism to request removal from that indexed cache.

---

## Advanced Google Hacking Techniques

**Google hacking** is the use of advanced search operators to build complex queries that surface sensitive or hidden information — the kind that helps an attacker locate vulnerable targets. (Note: don't put spaces between the operator and the query itself.)

| Operator | What It Does | Example |
|---|---|---|
| `site:` | Restricts results to a specific site or domain | `games site:www.certifiedhacker.com` |
| `allinurl:` | Only pages containing *all* the query terms in the URL | `allinurl: google career` |
| `inurl:` | Only pages containing the specified word in the URL | `inurl:copy site:www.google.com` |
| `intext:` | Pages containing the keyword within the page body | `intext:"vpn configuration"` |
| `allintitle:` | Only pages containing all query terms in the title | `malware detection intitle:help` |
| `inanchor:` | Pages where the anchor text of an inbound link contains the term | `Anti-virus inanchor:Norton` |
| `allinanchor:` | Pages where the anchor text of an inbound link contains *all* the terms | `allinanchor: best cloud service provider` |
| `cache:` | Shows Google's cached version of a page instead of the live one | `cache:www.eff.org` |
| `link:` | Finds pages linking to a specified page | `link:www.googleguide.com` |
| `filetype:` | Restricts results to a specific file extension | `jasmine:jpg` |
| `source:` | Pulls results from a specific source within Google News | `Malware news source:"Hacker News"` |
| `phonebook:` | Finds residential/business phone numbers for a person or org | `phonebook:Sundar Pichai` |
| `before:` | Content published before a specified date | `ransomware before:2020-06-29` |
| `after:` | Content published after a specified date | `site:wikipedia.org after:2023-01-01 artificial intelligence` |

A Google search built around these operators can surface things like security-team forum posts that inadvertently reveal which firewall or antivirus brand an organization runs — exactly the kind of detail that helps an attacker target known weaknesses in that specific product.

---

## What an Attacker Can Do With Google Hacking

By chaining these operators together, an attacker can filter enormous volumes of search results down to genuinely security-relevant information — not just finding vulnerable websites and servers, but locating private, sensitive data about the target directly. Once a vulnerable site turns up, the natural next step is attempting exploits like buffer overflow or SQL injection.

Categories of sensitive information attackers commonly extract from public servers using these techniques (formalized in the GHDB, below):

- Error messages that leak sensitive information
- Files containing passwords
- Sensitive directories
- Pages containing login portals
- Pages containing network/vulnerability data (IDS and firewall logs, configurations)
- Advisories and server vulnerabilities
- Software version information
- Web application source code

---

## AI-Assisted Google Hacking

Attackers are increasingly pairing AI tools with advanced Google hacking to automate the whole process. As an example of the pattern: a prompt to an AI shell assistant like **ShellGPT** — something like *"use filetype search operator to obtain pdf files on the target website eccouncil.org and store the result in the recon1.txt file"* — can get translated automatically into a working command-line pipeline (fetching search results via a text browser, filtering for URLs, and saving them to a file), skipping the manual work of building and running the query by hand.

The same pattern applies with general-purpose assistants like ChatGPT — for instance, a prompt asking it to *"use inurl search operator to obtain the Fortinet VPN login pages"* can produce a working search/filter pipeline for exactly that purpose. This mirrors what's covered in [Module 1's AI-Driven Ethical Hacking notes](../CEH-Module-01-Introduction-to-Ethical-Hacking/04-ai-driven-ethical-hacking.md) — AI acting as a force multiplier for reconnaissance tasks that used to require manually crafting each query.

---

## The Google Hacking Database (GHDB)

The **GHDB** is an authoritative, community-maintained source for Google dorks — search queries built around Google's advanced operators, specifically designed to surface sensitive information inadvertently exposed on the open web. It's technically a subset of the broader Exploit-DB project.

### GHDB Categories

- Footholds
- Files Containing Usernames
- Sensitive Directories
- Web Server Detection
- Vulnerable Files
- Vulnerable Servers
- Error Messages
- Files Containing Juicy Info
- Files Containing Passwords
- Sensitive Online Shopping Info
- Network or Vulnerability Data
- Pages Containing Login Portals
- Various Online Devices
- Advisories and Vulnerabilities

### How Attackers Use the GHDB

- **Reconnaissance** — gathering information about potential targets, including exposed files, directories, and devices that could be exploited.

### Example: Google Dorks for VPN Footprinting

| Search Query Pattern | Finds |
|---|---|
| `inurl:weblogin` + specific USG/ZyWALL model strings | Hosts with the Zyxel hardcoded-password vulnerability |
| `intext:"Please Login" SSL VPN inurl:remote/login intext:FortiClient` | Fortinet VPN login pages |
| `site:vpn.*.*/ intext:"login" intitle:"login"` | Various VPN login pages generally |
| `intitle:"index of" /etc/openvpn/` | Sensitive directories with juicy OpenVPN info |
| `"--BEGIN OpenVPN Static key V1--" ext:key` | Exposed OpenVPN static keys |
| `"index of" "vpn-config.*"` | Exposed vpn-config file details |
| `Index of / *.ovpn` | OpenVPN configuration files, certificates, and keys |
| `inurl:"/vpn/tmindex.html" vpn` | Netscaler and Citrix Gateway VPN login portals |
| `intitle:"SSL VPN Service" + intext:"...security conditions"` | Cisco ASA login web pages |

*(This table is illustrative of the GHDB's approach — real Google dorks change constantly as sites get patched or de-indexed, so treat specific query strings as examples of the pattern rather than reliable live queries.)*

---

## Footprinting Through the Shodan Search Engine

*Source: shodan.io*

**Shodan** is a search engine purpose-built for footprinting internet-connected devices and networks — specifically useful for finding devices and services with known vulnerabilities. A Shodan search targeting VoIP and VPN infrastructure, for instance, can surface detailed results about exposed devices in those categories. Shodan is also widely used to find exposed **IoT devices** (see below) and even **SCADA/industrial control systems**, both of which are frequently internet-facing without adequate access controls, giving attackers an entry point to establish a backdoor and pivot toward further attacks.

---

## Other Search-Engine Footprinting Techniques

### Reverse Image Search & Advanced Image Search
Search engines like Google support searching *by* an image (reverse image search) as well as heavily filtered image searches — both useful for tracing where else a photo of an employee, office, or badge has appeared online.

### Video Search Engines
Platforms and tools built around video content (this includes AI-assisted content tools) can surface footage related to a target — training videos, conference talks, leaked internal recordings — that reveal internal processes or personnel.

### Meta Search Engines
Meta search engines (e.g., StartPage) are a distinct category — rather than crawling the web themselves, they query *other* search engines and aggregate the combined results, which can surface information that a single engine's index alone would miss.

### FTP Search Engines
Many organizations — companies, universities, institutions — still run FTP servers to share large file archives internally. Though usually password-protected, plenty of FTP servers are left unsecured and directly browsable. Tools like **FileZilla** are used to connect to and browse these servers once located.

| Search Query Pattern | Finds |
|---|---|
| `site:.in \| .com \| .net intitle:"index of" ftp` | Files containing juicy information |
| `intitle:"Index of ftp passwords"` | Files containing passwords |
| `inurl:/ftp intitle:"office"` | Web server detection |
| `site:sftp.*.*/ intext:"login" intitle:"server login"` | Pages containing login portals |
| `intitle:"Index of ws_ftp.ini"` | The `ws_ftp.ini` file — often contains FTP usernames and passwords directly |
| `inurl:ftp -inurl:(http\|https) intext:"@gmail.com"...` | Archived email conversations — sometimes revealing full card numbers or private company emails |
| `allintitle:"CrushFTP WebInterface"` | CrushFTP login/password-reset pages |
| `"index of" /ftp/logs` | Potential log files |
| `intitle:"index of" inurl:ftp intext:admin` | Admin folders on FTP servers |

### IoT Search Engines
IoT-focused search engines (Shodan again being the prime example) crawl the internet specifically for publicly exposed IoT devices. Once located, an attacker can attempt to establish a backdoor into these devices as a foothold for further attacks — this is especially relevant for SCADA and industrial systems that were never designed with internet exposure in mind.

---

## Quick-Reference Summary

- **Search engines** index the open web via crawlers, turning up employee details, tech stacks, and login pages that feed directly into social engineering
- **14 Google operators** worth knowing: `site`, `allinurl`, `inurl`, `intext`, `allintitle`, `inanchor`, `allinanchor`, `cache`, `link`, `filetype`, `source`, `phonebook`, `before`, `after`
- **GHDB** = a structured, categorized library of "Google dorks" for surfacing exposed files, credentials, and vulnerable devices
- **Shodan** = the go-to search engine for internet-connected devices — VPNs, VoIP, IoT, and SCADA/ICS systems
- **AI tools** (ShellGPT, ChatGPT) increasingly automate the query-building and execution steps of this whole workflow
- Beyond Google: **reverse/advanced image search**, **video search engines**, **meta search engines**, **FTP search engines**, and **IoT search engines** all add distinct angles on the same target

---

*Part of the CEH Module 2 study series — continues in [Part C: Footprinting Through Internet Research Services](03-footprinting-through-internet-research-services.md).*
