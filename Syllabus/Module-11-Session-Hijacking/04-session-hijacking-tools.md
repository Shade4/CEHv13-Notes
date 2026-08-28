# 04 — Session Hijacking Tools

## Table of Contents
- [Hetty](#hetty)
- [Caido](#caido)
- [bettercap](#bettercap)
- [Additional Tools (Official List)](#additional-tools-official-list)
- [Classic / Legacy Tools (Added for Depth)](#classic--legacy-tools-added-for-depth)
- [Tool Comparison Table](#tool-comparison-table)

---

Attackers and penetration testers use dedicated tooling to hijack sessions between a client and server. This file covers the tools named directly in the official curriculum, plus (clearly marked) additional classic and legacy tools that have historically appeared in CEH-style material and real-world engagements, for extra depth.

## Hetty

- **Source:** https://github.com
- **What it is:** An HTTP toolkit for security research.

**Key features:**
- Machine-in-the-middle (MITM) HTTP proxy with logs and advanced search
- HTTP client for manually creating/editing requests, and replaying proxied requests
- Intercepting requests and responses for manual review (edit, send/receive, cancel)

Typical workflow: point your browser at Hetty's local proxy, browse the target application normally, then use the **Proxy Logs** view to review every request/response pair — searching for session cookies, tokens, or interesting parameters worth tampering with.

## Caido

- **Source:** https://caido.io
- **What it is:** A modern web security auditing toolkit for intercepting and viewing HTTP requests in real time while browsing.

**Key features:**
- Customization and testing of requests against large wordlists
- Automatic modification of incoming requests using Regex rules (**Match & Replace**)
- Resending requests to manually test endpoints (**Replay**)

Caido's interface (Sitemap, Scope, Filters, Intercept, HTTP History, Match & Replace, Replay, Automate, Workflows) will feel immediately familiar to anyone who's used Burp Suite — it's positioned as a lighter-weight, modern alternative built around the same proxy-intercept-replay workflow.

## bettercap

- **Source:** https://www.bettercap.org
- **What it is:** A portable framework written in Go that lets security researchers, red teamers, and reverse engineers perform reconnaissance and a wide range of attacks against Wi-Fi networks, Bluetooth Low Energy devices, wireless HID devices, and IPv4/IPv6 networks.

### Basic Usage

```bash
# Launch bettercap on a given interface
sudo bettercap -iface eth0
```

Once inside the interactive bettercap shell:

```text
help                       # list available commands / module help
active                     # show info about active modules
get <NAME>                 # get the value of variable NAME (or NAME* wildcard)
set <NAME> <VALUE>         # set the value of variable NAME
read <VARIABLE> <PROMPT>   # prompt the user for input, save to VARIABLE
include <CAPLET>           # load and run a caplet in the current session
! <COMMAND>                # execute a shell command and print its output
alias <MAC> <NAME>         # assign an alias to an endpoint by MAC address
```

Relevant built-in modules for session hijacking work: `arp.spoof`, `net.sniff`, `net.recon`, `net.probe`, `dns.spoof`, `dhcp6.spoof`, `any.proxy`, `api.rest`, `ble.recon`.

A typical MITM-and-sniff session inside bettercap looks like:

```text
net.probe on
net.recon on
set arp.spoof.targets 192.168.1.50
arp.spoof on
net.sniff on
```

## Additional Tools (Official List)

The official curriculum lists the following without a detailed walkthrough — brief usage notes added here:

| Tool | Link | Notes |
|---|---|---|
| **Burp Suite** | https://portswigger.net | Industry-standard intercepting proxy. Use **Proxy → Intercept** to capture and modify requests live, and **Repeater** to replay/tamper with a captured request (e.g., a session cookie) repeatedly. |
| **OWASP ZAP** | https://www.zaproxy.org | Free, open-source alternative to Burp with both a manual intercepting proxy and an automated active/passive scanner. |
| **WebSploit Framework** | https://sourceforge.net | A Metasploit-style modular framework with modules oriented toward web and wireless MITM attacks. |
| **sslstrip** | https://pypi.org | Classic tool for downgrading a victim's HTTPS connections to HTTP in a MITM position, so session cookies and credentials become sniffable in plaintext. Typical usage: `sslstrip -l 8080`, combined with `iptables` traffic redirection and ARP spoofing. |
| **JHijack** | https://sourceforge.net | A Java-based tool purpose-built for testing session-ID randomness/predictability by automating parameter-based session hijacking attempts. |

## Classic / Legacy Tools (Added for Depth)

> These are **not** in the official Module 11 deck, but they're worth knowing because they've historically appeared across CEH-adjacent material and real pentest engagements, and understanding the lineage helps make sense of *why* modern tools like bettercap and Caido are built the way they are.

| Tool | Category | Notes |
|---|---|---|
| **Ettercap** | Network MITM | One of the original ARP-spoofing/MITM suites; still maintained and widely used (`ettercap -T -q -M arp:remote ...`). |
| **Hunt** | TCP session hijacking | Classic Linux tool specifically built for active TCP session hijacking and connection resetting on a local segment. |
| **Juggernaut** | TCP session hijacking | An early (1990s) TCP hijacking tool that could watch for a keyword on the network and hijack any session containing it. |
| **T-Sight** | Commercial network monitoring/hijacking | Windows-based commercial tool historically referenced in CEH material for demonstrating session hijacking and network forensics side-by-side. |
| **Hamster & Ferret** | Sidejacking | A classic pairing: **Ferret** sniffs and stores HTTP cookies/session data from a network; **Hamster** provides a proxy/UI to replay those captured cookies and "clone" the victim's session in a browser. |
| **IP-Watcher** | Commercial session hijacking | Older commercial Unix tool for monitoring and actively hijacking network connections. |
| **Firesheep** | Sidejacking (browser extension) | A 2010 Firefox extension that made HTTP sidejacking (stealing unencrypted session cookies on open Wi-Fi) trivially easy for non-technical users; it's largely credited with accelerating the industry-wide push toward "HTTPS everywhere." The extension is defunct/unmaintained today, but it's a useful historical reference point for *why* `Secure` cookies and HSTS matter (see [`06`](06-countermeasures-and-best-practices.md) and [`07`](07-ipsec-and-advanced-protections.md)). |
| **Paros Proxy** | Intercepting proxy | A predecessor to both Burp Suite and OWASP ZAP; largely superseded today but historically significant. |

## Tool Comparison Table

| Tool | Primary Use | Level | Platform | Link |
|---|---|---|---|---|
| Hetty | HTTP MITM proxy, replay | Application | Cross-platform (Go) | github.com |
| Caido | HTTP auditing, replay, automation | Application | Cross-platform | caido.io |
| bettercap | Network recon + MITM (ARP/DNS/Wi-Fi/BLE) | Network | Cross-platform (Go) | bettercap.org |
| Burp Suite | HTTP intercept/repeat/scan | Application | Cross-platform (Java) | portswigger.net |
| OWASP ZAP | HTTP intercept/scan (free) | Application | Cross-platform (Java) | zaproxy.org |
| WebSploit | Modular web/wireless attacks | Both | Linux | sourceforge.net |
| sslstrip | HTTPS→HTTP downgrade | Network | Linux/Python | pypi.org |
| JHijack | Session-ID predictability testing | Application | Cross-platform (Java) | sourceforge.net |
| Ettercap | ARP MITM / sniffing | Network | Cross-platform | ettercap.github.io |
| Hamster & Ferret | Sidejacking / cookie replay | Application | Linux | (legacy, security-tool archives) |

---
**Next:** [`05-detection-methods-and-tools.md`](05-detection-methods-and-tools.md) — how defenders spot these techniques in progress.
