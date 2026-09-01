# 09 — Web Application Hacking Tools

> A consolidated, install-and-use reference for every tool named across this repo, plus the core "workhorse" tools (Burp Suite, OWASP ZAP, Nikto, WPScan, Vega) that deserve fuller setup instructions than a one-line command. Most tools ship pre-installed on Kali/Parrot OS; installation commands below assume a Debian-based pentesting distro or a fresh Ubuntu box.

## Table of Contents
- [Burp Suite](#burp-suite)
- [OWASP ZAP](#owasp-zap)
- [sqlmap](#sqlmap)
- [Nikto](#nikto)
- [Directory & Content Discovery: Gobuster, dirb, ffuf, wfuzz](#directory--content-discovery-gobuster-dirb-ffuf-wfuzz)
- [Hydra](#hydra)
- [Vega](#vega)
- [WPScan](#wpscan)
- [Technology Fingerprinting: WhatWeb, Wappalyzer](#technology-fingerprinting-whatweb-wappalyzer)
- [Website Mirroring: HTTrack, wget](#website-mirroring-httrack-wget)
- [API Testing: Postman](#api-testing-postman)
- [Web Service Testing: SoapUI, XMLSpy](#web-service-testing-soapui-xmlspy)
- [Metadata & OSINT: Metagoofil, FOCA](#metadata--osint-metagoofil-foca)
- [Wordlist Generation: CeWL](#wordlist-generation-cewl)
- [Automated Recon Suites: Sn1per](#automated-recon-suites-sn1per)
- [AI-Assisted Web Application Hacking](#ai-assisted-web-application-hacking)
- [Full Command Quick-Reference Table](#full-command-quick-reference-table)

---

## Burp Suite

**What it is:** the industry-standard intercepting proxy and web application testing platform. Nearly every manual technique in this repo (parameter tampering, replaying requests, fuzzing, WebSocket inspection) is most naturally performed through Burp.

**Install (Community Edition):**
```bash
# Kali/Parrot: usually pre-installed
sudo apt update && sudo apt install burpsuite -y

# Or download the Community/Pro jar directly from PortSwigger and run:
java -jar burpsuite_community_v2024.x.jar
```

**Initial setup:**
1. Launch Burp → create/open a temporary or persistent project.
2. Go to **Proxy → Options** and confirm the listener is on `127.0.0.1:8080`.
3. In your browser, set the HTTP/HTTPS proxy to `127.0.0.1:8080` (or use FoxyProxy for one-click toggling).
4. Visit `http://burpsuite` in the proxied browser and install Burp's CA certificate so HTTPS traffic can be decrypted for inspection.
5. Turn **Intercept** on/off in the Proxy tab depending on whether you want to pause and edit every request live, or just passively log traffic to build the site map.

**Core tabs you'll use constantly:**
| Tab | Purpose |
|---|---|
| **Proxy** | Intercept, view, and modify live traffic between browser and target |
| **Target → Site map** | Automatically-built map of every URL/parameter observed |
| **Repeater** | Manually resend and tweak a single request repeatedly (parameter tampering, injection testing) |
| **Intruder** | Automated fuzzing — mark payload positions, load a wordlist, fire hundreds/thousands of variations |
| **Decoder** | Encode/decode Base64, URL, HTML entities, hex — essential for crafting evasion payloads |
| **Comparer** | Diff two responses/requests byte-for-byte — great for confirming boolean-blind SQLi |
| **Sequencer** | Statistically analyzes the randomness/entropy of session tokens |
| **Extender/BApp Store** | Install community plugins (e.g., Turbo Intruder, JSON Web Tokens, Autorize) |

## OWASP ZAP

**What it is:** the leading free/open-source alternative to Burp, maintained by OWASP, with strong built-in automated scanning.

```bash
sudo apt install zaproxy -y
# or run the container:
docker run -u zap -p 8080:8080 -i zaproxy/zap-stable zap.sh -daemon -host 0.0.0.0 -port 8080
```

**Automated scan via CLI (headless, good for CI pipelines):**
```bash
zap-baseline.py -t https://target.com -r zap-report.html      # quick, passive-only baseline
zap-full-scan.py -t https://target.com -r zap-full-report.html # active scan, more thorough, noisier
```
**GUI workflow:** enter the target URL in **Quick Start → Automated Scan**, which spiders the site and then runs ZAP's active scan rules (injection, XSS, misconfiguration checks) automatically, producing a categorized findings report.

## sqlmap

Fully documented with command examples in [04 — Injection Attacks](./04-injection-attacks.md#automating-sql-injection-with-sqlmap).

```bash
sudo apt install sqlmap -y
sqlmap --version
```

## Nikto

**What it is:** a fast web server scanner that checks for thousands of known-dangerous files/CGIs, outdated server software, and generic misconfigurations.

```bash
sudo apt install nikto -y

nikto -h https://target.com
nikto -h https://target.com -p 443 -ssl
nikto -h target.com -o nikto_report.html -Format htm
nikto -h target.com -Tuning 9    # tuning 9 = focus on SQL injection checks specifically
```

## Directory & Content Discovery: Gobuster, dirb, ffuf, wfuzz

Full command syntax already covered in [03 — Footprinting & Reconnaissance](./03-footprinting-and-recon.md#hidden-content--directory-discovery). Install commands:
```bash
sudo apt install gobuster dirb wfuzz -y
# ffuf is Go-based and often installed via go install or downloaded as a release binary:
go install github.com/ffuf/ffuf/v2@latest
```

## Hydra

Full command syntax in [06 — Session, Authentication & Authorization Attacks](./06-session-authentication-and-authorization-attacks.md#password-attacks-brute-forcing).

```bash
sudo apt install hydra -y
hydra -h                          # list all supported protocol modules (http-post-form, ssh, ftp, rdp, ...)
```

## Vega

**What it is:** a free, GUI-based web vulnerability scanner (Java-based) good for a quick automated pass alongside ZAP/Burp — useful as a second opinion since different scanners' detection engines catch different classes of bugs.

```bash
sudo apt install vega -y
```
Usage: **Scan → Start New Scan**, enter the target URL, select the module categories to run (SQL injection, XSS, directory listing, etc.), and review categorized results in the left-hand findings tree.

## WPScan

**What it is:** a specialized black-box scanner for **WordPress** sites — the single most common CMS on the web, and a huge target surface given how many third-party plugins/themes it typically runs.

```bash
sudo apt install wpscan -y
# or via Ruby gem:
gem install wpscan

wpscan --url https://target.com --enumerate vp,vt,u    # vulnerable plugins, vulnerable themes, users
wpscan --url https://target.com --api-token <your_wpvulndb_token>   # cross-reference against the WPScan vulnerability DB
wpscan --url https://target.com --enumerate u --passwords rockyou.txt   # brute-force discovered usernames
```

## Technology Fingerprinting: WhatWeb, Wappalyzer

Full usage in [03 — Footprinting & Reconnaissance](./03-footprinting-and-recon.md#detecting-web-application-technologies).
```bash
sudo apt install whatweb -y
whatweb -a 3 https://target.com    # aggression level 3 = more thorough, more requests
```

## Website Mirroring: HTTrack, wget

Full usage in [03 — Footprinting & Reconnaissance](./03-footprinting-and-recon.md#website-mirroring).
```bash
sudo apt install httrack wget -y
```

## API Testing: Postman

**What it is:** the standard GUI client for constructing, saving, and organizing HTTP/API requests into reusable collections — indispensable for systematically working through every endpoint discovered during [API reconnaissance](./07-web-services-api-and-webhook-attacks.md#web-api-hacking-methodology).

Install: download the desktop app from https://www.postman.com/downloads/, or use the lightweight CLI companion, **Newman**, to run saved collections headlessly:
```bash
npm install -g newman
newman run my-api-collection.json --environment prod.postman_environment.json
```

## Web Service Testing: SoapUI, XMLSpy

Covered in [07 — Web Services, API & Webhook Attacks](./07-web-services-api-and-webhook-attacks.md#web-service-attack-tools).

## Metadata & OSINT: Metagoofil, FOCA

Full usage in [03 — Footprinting & Reconnaissance](./03-footprinting-and-recon.md#extracting-metadata-from-public-documents).
```bash
sudo apt install metagoofil -y
```

## Wordlist Generation: CeWL

Full usage in [03 — Footprinting & Reconnaissance](./03-footprinting-and-recon.md#gathering-a-target-specific-wordlist).
```bash
sudo apt install cewl -y
```

## Automated Recon Suites: Sn1per

Full usage in [03 — Footprinting & Reconnaissance](./03-footprinting-and-recon.md#using-ai-to-accelerate-recon).
```bash
git clone https://github.com/1N3/Sn1per
cd Sn1per && bash install.sh
```

## AI-Assisted Web Application Hacking

Modern practice increasingly wraps the tools above in natural-language-driven automation. Two patterns worth knowing:

**1. Prompting an AI assistant to generate a purpose-built script**, then reviewing and running it yourself:
```
Prompt: "Create and run a custom Python script that will run web application
         tasks to perform footprinting and vulnerability scanning against
         the target www.target.com"
```
The AI-generated script typically wraps `requests`, `socket`, or subprocess calls to existing tools (nmap, whatweb) with logic to parse and summarize output — always review generated code before executing it, exactly as you would any script from an unfamiliar source.

**2. AI-powered commercial DAST/SAST platforms** that layer machine learning on top of traditional scanning to reduce false positives and adapt test strategies based on observed application behavior (e.g., **ZeroThreat.ai**, **Invicti**, **Apiiro**) — covered further in [10 — Countermeasures & Secure Coding](./10-countermeasures-and-secure-coding.md#ai-powered-application-security-testing).

**Caution:** AI-generated payloads and scripts should always be treated the same as any other untrusted code — read them before execution, run them only against in-scope, authorized targets, and validate any findings manually before relying on them in a report.

## Full Command Quick-Reference Table

| Task | Tool | Command |
|---|---|---|
| Port/service scan | Nmap | `nmap -sV -p- target.com` |
| WAF detection | wafw00f | `wafw00f https://target.com` |
| Load balancer detection | lbd | `lbd target.com` |
| Directory brute-force | Gobuster | `gobuster dir -u https://target.com -w common.txt` |
| Tech fingerprinting | WhatWeb | `whatweb -a 3 https://target.com` |
| Mirror a site | HTTrack | `httrack https://target.com -O ./mirror` |
| Build a custom wordlist | CeWL | `cewl https://target.com -w wordlist.txt` |
| Metadata extraction | Metagoofil | `metagoofil -d target.com -t pdf,doc -o results` |
| SQL injection testing | sqlmap | `sqlmap -u "https://target.com/item?id=2" --batch` |
| Generic vuln/misconfig scan | Nikto | `nikto -h https://target.com` |
| WordPress-specific scan | WPScan | `wpscan --url https://target.com --enumerate vp,vt,u` |
| Password brute-force | Hydra | `hydra -l admin -P rockyou.txt target.com http-post-form "..."` |
| GUI vulnerability scan | OWASP ZAP | `zap-baseline.py -t https://target.com` |
| GUI vulnerability scan (2nd opinion) | Vega | GUI: Scan → Start New Scan |
| Manual request manipulation | Burp Suite | GUI: Proxy → Repeater → Intruder |
| API request collections | Postman / Newman | `newman run collection.json` |
| SOAP service testing | SoapUI | GUI or `testrunner.sh` |
| Full automated recon | Sn1per | `sniper -t target.com -m normal` |

---

**Previous:** [← 08 — Other Web Application Attacks](./08-other-web-app-attacks.md) · **Next:** [10 — Countermeasures & Secure Coding →](./10-countermeasures-and-secure-coding.md)
