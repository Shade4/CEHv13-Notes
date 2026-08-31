# 09 — Security Scanning & Monitoring Tools

> Defensive tooling catalogue supporting **Objective 4: Web Server Attack Countermeasures**

This file rounds up every defensive/blue-team tool the courseware references — organized into five categories: web application scanners, web server scanners, malware-infection monitors, general web server security tools, and pen-testing platforms.

## 1. Web Application Security Scanners

### Syhunt Hybrid

- **Source:** https://www.syhunt.com
- Automates web application security testing and guards the organization's web infrastructure against web application attacks. Syhunt Dynamic crawls websites and detects XSS, directory traversal problems, fault injection, SQL injection, and several other issues. Syhunt Hybrid creates signatures to detect application vulnerabilities and prevents logout. It also logs suspicious responses and tests errors for review.

### N-Stalker X

- **Source:** https://www.nstalker.com
- A web application security scanner that searches for vulnerabilities to attacks such as clickjacking, SQL injection, and XSS. It allows spider crawling throughout the application and the crawling of web macros for form authentication. It also provides proxy capabilities for "drive-thru" attacks and identifies components through reverse proxies that distribute different platforms in the same application URL.

### Additional Web Application Security Scanners

| Tool | Source |
|---|---|
| Invicti | https://www.invicti.com |
| Burp Suite | https://www.portswigger.net |
| Wapiti | https://wapiti-scanner.github.io |
| WebScarab | https://owasp.org |
| WPSec | https://wpsec.com |
| Tinfoil Web Scanner | https://www.tinfoilsecurity.com |
| Skipfish | https://code.google.com |
| Detectify | https://www.detectify.com |
| OpenText™ Fortify™ On Demand | https://www.opentext.com |
| OWASP Zed Attack Proxy (ZAP) | https://www.zaproxy.org |
| SonarQube | https://www.sonarqube.org |
| Arachni | https://www.ecsypno.com |

## 2. Web Server Security Scanners

### Qualys Community Edition

- **Source:** https://www.qualys.com
- Discovers IT assets, manages vulnerabilities, scans web applications, and maintains cloud assets inventory. It offers vulnerability management to identify dangerous bugs and remediate them immediately. Qualys can also assess vulnerabilities on all internal IT infrastructure as well as external-facing assets to ensure a secure state.

### Additional Web Server Security Scanners

| Tool | Source |
|---|---|
| Observatory | https://observatory.mozilla.org |
| WordPress Security Scan | https://hackertarget.com |
| Web Vulnerability Scanner | https://pentest-tools.com |
| Nikto | https://cirt.net |
| ImmuniWeb | https://www.immuniweb.com |

## 3. Web Server Malware Infection Monitoring Tools

### QualysGuard Malware Detection

- **Source:** https://www.qualys.com
- Allows organizations to proactively scan their websites for malware and provides automated alerts and aggregations in-depth reporting to enable prompt identification and resolution. It enables organizations to protect their customers from malware infections and safeguard their brand reputation.

### Additional Malware Infection Monitoring Tools

| Tool | Source |
|---|---|
| Sucuri Site Check | https://sitecheck.sucuri.net |
| SiteLock Malware Removal | https://www.sitelock.com |
| Quttera | https://quttera.com |
| Web Inspector | https://www.webinspector.com |
| SiteGuarding | https://www.siteguarding.com |

## 4. Web Server Security Tools

### OpenText™ Fortify™ WebInspect

- **Source:** https://www.opentext.com
- An automated dynamic application security testing solution that discovers configuration issues as well as identifies and prioritizes hacking techniques used in running applications. It mimics real-world hacking techniques and provides a comprehensive analysis of complex web applications and services. WebInspect dashboards and reports provide organizations with visibility and an accurate risk posture of their applications.

### Additional Web Server Security Tools

| Tool | Source |
|---|---|
| Acunetix Web Vulnerability Scanner | https://www.acunetix.com |
| NetIQ Secure Configuration Manager | https://www.netiq.com |
| SAINT Security Suite | https://www.carson-saint.com |
| Sophos Intercept X for Server | https://www.sophos.com |
| UpGuard | https://www.upguard.com |

## 5. Web Server Pen Testing Tools

### CORE Impact

- **Source:** https://www.coresecurity.com
- Finds vulnerabilities in an organization's web server. This tool allows a user to evaluate the security posture of a web server by using the same techniques currently employed by cyber criminals. It scans network servers, workstations, firewalls, routers, and various applications for vulnerabilities; identifies which vulnerabilities pose real threats to the network; imports scan results and can run exploits to test the identified vulnerabilities; identifies the potential impact of exploited vulnerabilities; and can prioritize and execute remediation efforts.

### Additional Web Server Pen Testing Tools

| Tool | Source |
|---|---|
| Cobalt Strike | https://www.cobaltstrike.com |
| Fuxploider | https://github.com |
| Mitmproxy | https://mitmproxy.org |

---

> 📝 **Note (added):** as an aspiring pentester, it's worth knowing the practical distinction between these five buckets: **web app scanners** (§1) test application-layer logic (SQLi/XSS in *your code*), **web server scanners** (§2) test the *server software itself* (Apache/Nginx/IIS misconfig and CVEs — this is this module's primary focus), **malware monitors** (§3) are usually SaaS/subscription products aimed at *already-compromised* sites (webmasters, not pentesters), **general security tools** (§4) overlap both app and server layers, and **pen-testing platforms** (§5) are full attack frameworks (exploitation + post-exploitation + reporting) rather than pure scanners — closer in spirit to [Immunity CANVAS](07-web-server-attack-tools.md#immunitys-canvas) than to Nikto.

---

**Previous:** [← 08 — Countermeasures & Hardening](08-countermeasures-and-hardening.md) · **Next:** [10 — Patch Management →](10-patch-management.md)
