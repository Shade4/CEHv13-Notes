# Module 2: Footprinting and Reconnaissance
## Part H — Footprinting Tools and AI-Powered Automation

[← Back to Part G: Footprinting Through Social Engineering](07-footprinting-through-social-engineering.md) | [Next: Footprinting Countermeasures and Module Summary →](09-footprinting-countermeasures-and-summary.md)

---

## Table of Contents

1. [Dedicated Footprinting Tools](#dedicated-footprinting-tools)
2. [Additional Footprinting Tools](#additional-footprinting-tools)
3. [AI-Powered OSINT Tools](#ai-powered-osint-tools)
4. [Creating Custom Footprinting Scripts with AI](#creating-custom-footprinting-scripts-with-ai)
5. [Quick-Reference Summary](#quick-reference-summary)

---

## Dedicated Footprinting Tools

Beyond the individual techniques covered in earlier parts, a set of dedicated tools automate footprinting end to end — collecting a target's IP location, routing information, business information, address, phone number, social security number, details about the source of an email or file, DNS information, and domain information, all from a single interface.

### Maltego
*Source: maltego.com*

An automated tool for determining the **relationships and real-world links** between people, groups of people, organizations, websites, and internet infrastructure. Attackers use Maltego's different "entities" to pull email addresses, phone number lists, and a target's infrastructure details (domains, DNS names, netblocks, IP addresses). A common workflow: add a **Website entity**, rename it with the target's domain, and Maltego surfaces the email addresses and phone numbers associated with that target, along with entities tied to the domain's owner.

### Recon-ng
*Source: github.com*

A **web reconnaissance framework** with independent modules and database interaction, providing an environment for conducting open-source, web-based reconnaissance. As shown in a typical workflow, the `recon/domains-hosts/brute_hosts` module is loaded and run to harvest a list of hosts associated with the target URL/domain.

### FOCA (Fingerprinting Organizations with Collected Archives)
*Source: elevenpaths.com*

A tool mainly used to find **metadata and hidden information** in documents it scans — most commonly Microsoft Office, Open Office, or PDF files. Key features:

| Feature | What It Does |
|---|---|
| **Web Search** | Searches for hosts and domain names through URLs associated with the main domain, analyzing each link for host/domain info |
| **DNS Search** | Checks each domain's NS, MX, and SPF servers to discover new hosts and domain names |
| **IP Resolution** | Resolves each hostname by comparison with DNS, to obtain the IP address for that server name |
| **PTR Scanning** | Finds more servers in the same segment of a determined address via a PTR log scan |
| **Bing IP** | Searches for new domain names associated with a discovered IP address |
| **Common Names** | Performs dictionary attacks against the DNS |

Attackers use FOCA to search a target domain and pull the file information stored within it — extracted files can be viewed directly in a browser, and attackers can view additional information such as network domains, roles, vulnerabilities, and metadata of the target domain.

### subfinder
*Source: github.com*

A **subdomain discovery tool** that finds valid subdomains for websites using passive online sources — supporting multiple output formats (JSON, file, stdout).

### OSINT Framework
*Source: osintframework.com*

An open-source intelligence gathering framework focused on pulling information from free tools or resources, presented through a simple web interface as an **OSINT tree structure**. Tools in the tree are tagged with indicators:

- **(T)** — a link to a tool that must be installed and run locally
- **(D)** — a Google dork
- **(R)** — requires registration
- **(M)** — a URL containing the search term that must be edited manually

The tree spans categories like Username, Email Address, Domain Name, IP Address, Images/Videos/Docs, Social Networks, People Search Engines, Business Records, Geolocation Tools, Whois Records, Metadata, Dark Web, and more — each branching out to dozens of specific tools and services.

### Recon-Dog
*Source: github.com*

An all-in-one tool for basic information-gathering needs, using APIs to collect data about a target system.

| Feature | What It Does |
|---|---|
| **Censys** | Uses censys.io to gather a large amount of information about an IP address |
| **NS lookup** | Performs a name server lookup |
| **Port scan** | Scans the most common TCP ports |
| **Detect CMS** | Can detect 400+ content management systems |
| **Whois lookup** | Performs a Whois lookup |
| **Detect honeypot** | Uses shodan.io to check whether the target is a honeypot |
| **Find subdomains** | Uses findsubdomains.com to find subdomains |
| **Reverse IP lookup** | Finds domains associated with an IP address |
| **Detect technologies** | Uses wappalyzer.com to detect 1000+ technologies |
| **All** | Runs every utility against the target at once |

### BillCipher
*Source: github.com*

An information-gathering tool for a website or IP address, built to run on any OS supporting Python 2, Python 3, or Ruby. Offers a menu-driven interface with options including DNS Lookup, Whois Lookup, GeoIP Lookup, Subnet Lookup, Port Scanner, Page Links, Zone Transfer, HTTP Header, Host Finder, IP-Locator, Find Shared DNS Servers, Get Robots.txt, Host DNS Finder, Reverse IP Lookup, Subdomain listing, Find Admin login site, Check and Bypass CloudFlare, Website Copier, and Host Info Scanner.

---

## Additional Footprinting Tools

- **Sudomy** (github.com)
- **theHarvester** (edge-security.com)
- **whatweb** (github.com)
- **Raccoon** (github.com)
- **Orb** (github.com)
- **Web Check** (web-check.xyz)
- **OSINT.SH** (osint.sh)

---

## AI-Powered OSINT Tools

AI has meaningfully expanded what's possible in OSINT gathering — automating data collection, analysis, and even prediction, and extracting relevant insights faster than traditional manual methods allow.

### Key AI Use Cases in OSINT

- **Web Scraping** — pulling data from social media, blogs, forums, and deep-web databases; automating extraction of specific content like social media comments and replies over time
- **Pattern Recognition** — ML models identify entities (names, company details, addresses, emails, phone numbers) and the relationships between them across large datasets
- **Content Summarization** — NLP algorithms condense large volumes of data (e.g., extracting company names from hundreds of pages of PDFs)
- **Sentiment Analysis** — interpreting human emotion through text, useful for gauging public sentiment or predicting consumer behavior from social posts and reviews
- **Image Recognition** — computer vision assists with **face recognition** (identifying/tracking individuals across media), **metadata analysis** (extracting metadata from digital files), and enhanced **reverse image search** (including deepfake detection)
- **AI Detection** — identifying content generated by other AI tools, relevant to spotting AI-facilitated malicious activity

### Benefits of Integrating AI into OSINT

- **Improved Efficiency** — automates web scraping and data extraction, freeing investigators for higher-level analysis
- **Greater Scope** — expands OSINT coverage across the surface web, deep web, and dark web at once, surfacing patterns and relationships too large to find manually
- **Enhanced Visibility** — connects billions of seemingly unrelated data points into coherent, user-friendly graphical networks
- **Increased Investigator Safety** — enables anonymized, automated investigation, reducing the risk of exposing an investigator's identity in dangerous environments like the dark web

### Named AI-Powered OSINT Tools

| Tool | What It Does |
|---|---|
| **Taranis AI** (taranis.ai) | Uses NLP/AI to gather, enhance, and analyze unstructured news articles from multiple sources into structured, publishable intelligence reports (PDFs and more) |
| **OSS Insight** (ossinsight.io) | Analyzes 5+ billion GitHub events; offers GPT-powered natural-language querying, developer/repository analytics, and project comparison — useful for spotting emerging tech, vulnerable/low-engagement repos, and security landscape trends |
| **DorkGPT** (dorkgpt.com) | GPT-powered assistant for Google Dorking — generating and refining search queries to surface information not reachable through regular search |
| **DorkGenius** (dorkgenius.com) | Automates Google Dorking to generate advanced queries for finding hidden files, directories, and vulnerabilities |
| **Google Word Sniper** (googlewordsniper.eu) | Refines search queries with targeted keywords/phrases to surface hidden or niche content |
| **Cylect.io** (cylect.io) | Integrates multiple OSINT databases into one interface, simplifying and speeding up investigative search |
| **ChatPDF** (chatpdf.com) | Lets users upload and conversationally query PDF documents for specific data, summaries, and insights |
| **Bardeen.ai** (bardeen.ai) | Automates data collection and analysis workflows from various online sources |
| **DarkGPT** (github.com/luijait/DarkGPT) | Uses GPT-4-200K to query leaked databases, aiding targeted searches within compromised data sources |
| **PenLink Cobwebs** (cobwebs.com) | Gathers and analyzes data from various online sources, with visualization support for cybersecurity investigations |
| **Explore AI** (exploreai.vercel.app) | An AI-powered YouTube search engine for extracting information from video content |
| **AnyPicker** (app.anypicker.com) | A no-code visual web scraper with multi-page scraping and real-time extraction preview |

---

## Creating Custom Footprinting Scripts with AI

Beyond using pre-built tools, attackers can prompt an AI assistant to **write a custom automation script** on the spot. A representative prompt:

*"Develop a Python script which will accept the domain name www.microsoft.com as input and execute a series of website footprinting commands, including DNS lookups, WHOIS records retrieval, email enumeration, and more, to gather information about the target domain."*

An AI shell assistant (e.g., ShellGPT) can turn this directly into a working script:

```python
import subprocess

def dns_lookup(domain):
    return subprocess.getoutput(f"dig {domain} ANY +noall +answer")

def whois_lookup(domain):
    return subprocess.getoutput(f"whois {domain}")

def email_enumeration(domain):
    return subprocess.getoutput(f"theHarvester -d {domain} -b all -l 100")

def run_footprinting(domain):
    print("Performing DNS Lookup...")
    dns_info = dns_lookup(domain)
    print(dns_info)

    print("\nPerforming Whois Lookup...")
    whois_info = whois_lookup(domain)
    print(whois_info)

    print("\nEnumerating Emails...")
    emails = email_enumeration(domain)
    print(emails)

domain = 'www.microsoft.com'
run_footprinting(domain)
```

**What the script does:** it defines four functions — `dns_lookup()` (runs `dig` for DNS records), `whois_lookup()` (runs `whois`), `email_enumeration()` (runs `theHarvester` to enumerate emails tied to the domain), and `run_footprinting()`, which chains all three and prints the combined results. Run with:

```bash
python3 website_footprinting.py
```

A real run against a large target domain can return dozens of DNS/Whois lines, a full theHarvester banner and email-enumeration pass, a list of "interesting URLs" discovered along the way, and a count of every IP address found tied to the domain — turning what would be four or five separate manual tool invocations into a single automated pass.

---

## Quick-Reference Summary

- **All-purpose footprinting tools**: Maltego (relationship mapping), Recon-ng (modular web recon framework), FOCA (document metadata), subfinder (subdomains), OSINT Framework (tree of categorized OSINT tools/dorks), Recon-Dog and BillCipher (multi-function all-in-ones)
- **Further tools worth knowing**: Sudomy, theHarvester, whatweb, Raccoon, Orb, Web Check, OSINT.SH
- **AI's 6 core OSINT use cases**: web scraping, pattern recognition, content summarization, sentiment analysis, image recognition, AI-content detection
- **AI's 4 core OSINT benefits**: efficiency, scope, visibility, investigator safety
- **12 named AI-OSINT tools**: Taranis AI, OSS Insight, DorkGPT, DorkGenius, Google Word Sniper, Cylect.io, ChatPDF, Bardeen.ai, DarkGPT, PenLink Cobwebs, Explore AI, AnyPicker
- **AI can also write the automation itself** — a single natural-language prompt can produce a working, multi-function footprinting script

---

*Part of the CEH Module 2 study series — continues in [Part I: Footprinting Countermeasures and Module Summary](09-footprinting-countermeasures-and-summary.md).*
