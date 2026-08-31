# 02 — Web Server Attack Techniques

> Objective covered: **Demonstrate Different Web Server Attacks**

An attacker can use many techniques to compromise a web server: DoS/DDoS, DNS server hijacking, DNS amplification, directory traversal, man-in-the-middle (MITM)/sniffing, phishing, website defacement, web server misconfiguration, HTTP response splitting, web cache poisoning, SSH brute force, and web server password cracking. This file walks through each technique in detail.

## 1. DNS Server Hijacking

**Concept:** The attacker compromises a DNS server and **changes its DNS mappings** so that all requests coming toward the target web server are redirected to the attacker's own malicious server.

### How it works

1. The DNS server checks the requested domain against its own mappings.
2. The attacker **compromises the DNS server and changes the DNS settings** for the target domain.
3. A user (victim) sends a request for the domain to the (now-compromised) DNS server.
4. The DNS server responds with the **attacker's fake site IP** instead of the legitimate site.
5. The user is redirected to the attacker's fake site while believing they reached the legitimate site.

```
   Attacker ──Compromises──> DNS Server (Target)
                                    │
                                    │ (mapping now points to Fake Site)
   Users (Victim) ──Request──> DNS Server (Target) ──Response──> Redirects to Fake Site
                                                                  (instead of Legitimate Site)
```

> 📖 **Defense pointer:** see [08 — Countermeasures & Hardening, §6](08-countermeasures-and-hardening.md#6-how-to-defend-against-dns-hijacking).

## 2. DNS Amplification Attack

Recursive DNS query resolution is exploited to flood a victim with amplified DNS response traffic (a DDoS technique).

### How recursive DNS resolution normally works

1. A user queries their **primary DNS server** for a domain.
2. If the mapping isn't cached, the primary DNS server forwards the request to the **root server** (`.com` TLD namespace).
3–8. This process repeats recursively until the primary DNS server resolves the mapping.
9. Once resolved, the primary DNS server **caches** the IP for future queries.

### How attackers weaponize it

1. The attacker instructs a **botnet** to send DNS queries — but each bot **spoofs the victim's IP address** as the source.
2. All compromised hosts (bots) send DNS queries **using the victim's spoofed IP** to a DNS server configured in the victim's TCP/IP settings.
3–8. The recursive resolution steps play out normally, **but the response is sent to the victim** (because the source IP was spoofed), not to the actual bot that made the request.
9. Because a DNS *response* is typically much larger than the *query* (amplification factor), the victim's server/DNS is flooded with disproportionately large amounts of traffic — a classic **DNS amplification DDoS**.

> 📖 **Cross-reference:** see [Module 10: Denial-of-Service](../.) for the complete DoS/DDoS attack catalogue and mitigation.

## 3. Directory Traversal Attacks

Directory traversal (a.k.a. **path traversal** or the **dot-dot-slash `../` attack**) exploits insufficient input validation to access files/directories **outside** the web root.

- Poorly patched or configured web server software can make a server vulnerable to directory traversal.
- By manipulating a URL, attackers use the **trial-and-error** method to navigate outside the restricted directory and access sensitive information on the system.
- An attacker exploits the web server software (or a vulnerable web application running on it) to perform this — sometimes using just a browser, sometimes with a dedicated tool.

**Classic example (IIS Unicode directory traversal):**
```
http://server/scripts/..%c0%af../winnt/system32/cmd.exe?/c+dir+c:\
```

**Example (double-encoded traversal):**
```
http://server/scripts/../../Windows/System32/cmd.exe?/c+dir+c:\
```

A vulnerable server will respond with a directory listing (e.g. `Directory of C:\`) revealing the filesystem structure — a strong indicator remote command execution is achievable next.

> 📖 **Defense pointer:** validate and canonicalize all user-supplied paths server-side; never trust client input to build filesystem paths. See countermeasures in [08](08-countermeasures-and-hardening.md).

## 4. Website Defacement

**Concept:** Unauthorized changes to the content/visual appearance of a web page or entire site.

- Hackers break into web servers and alter the hosted website (adding images, pop-ups, or text) so the visual appearance changes — in the worst case, the **entire page is replaced**.
- Defaced pages typically expose visitors to propaganda or misleading information until administrators discover and correct the change.
- Attackers use a variety of methods, such as **SQL injection**, to access a website to deface it.
- In addition to changing appearance, attackers may infect visitors' computers by embedding drive-by malware/Trojans in the defaced page.
- Website defacement doesn't just embarrass the target organization — it's also often intended to harm site visitors.

*(Classic defacement screens read something like: "YOU ARE OWNED!!!!!!! — HACKED! Hi Master, Your website is owned by US, Hackers. Next target — [target].com")*

## 5. Web Server Misconfiguration

**Concept:** Configuration weaknesses in web infrastructure that can be exploited to launch attacks such as directory traversal, server intrusion, and data theft. Some web server misconfigurations expose debug messages, anonymous or default users/passwords, and unnecessary services running.

### Common categories of misconfiguration

- Verbose debug/error messages
- Anonymous or default users/passwords
- Remote administration functions
- Unnecessary services enabled
- Misconfigured/default SSL certificates

Administrators who configure web servers improperly may leave serious loopholes that give an attacker the chance to exploit the misconfigured web server, thereby compromising its security and stealing sensitive information. Misconfiguration vulnerabilities may relate to configuration files, applications, files, scripts, or web pages. Misconfigured servers can also help an attacker bypass user authentication.

### Real Configuration Examples

**1. Apache `httpd.conf` — exposed server-status page:**
```apache
<Location "/server-status">
    SetHandler server-status
    Require host example.com
</Location>
```
This allows anyone at `example.com` (or, if misconfigured further, anyone at all) to view the server's live status page — including hosts/requests being processed.

**2. `php.ini` — verbose error output:**
```ini
display_errors = On
log_errors = syslog
error_log =
ignore_repeated_errors = Off
```
`display_errors = On` in production leaks stack traces, file paths, and database errors directly to visitors.

**3. IIS `web.config` — directory browsing enabled:**
```xml
<system.webServer>
    <directoryBrowse enabled="true"/>
</system.webServer>
```
Allows users to see full directory contents, potentially exposing sensitive files.

**4. IIS `web.config` — unvalidated file uploads:**
```xml
<system.webServer>
    <security>
        <requestFiltering maxAllowedContentLength="30000000" />
    </requestFiltering>
    </security>
</system.webServer>
```
A permissive upload configuration without validation allows attackers to upload malicious files (e.g. web shells) that can later be executed on the server → remote code execution.

**5. Nginx — missing root/location block:**
```nginx
server {
    listen 80;
    server_name example.com;

    # Missing root location block
}
```
This can lead to undefined behavior, potentially exposing directory listings or default server configurations.

**6. Nginx — unsanitized variable in `proxy_pass`:**
```nginx
location / {
    set $variable $arg_user_input;
    proxy_pass http://backend/$variable;
}
```
Direct use of user input in variables without sanitization can lead to injection attacks (SSRF/request smuggling). **User inputs must be validated and sanitized** before use.

> 📝 **Note (added):** the last two examples are functionally the two most common real-world Nginx misconfig CVE classes — missing `location` blocks that fall through to default server blocks, and unsanitized variables passed into `proxy_pass`/`alias` directives. See [05 — Path Traversal via Misconfigured NGINX Alias](05-vulnerability-scanning-and-exploitation.md#3-path-traversal-via-misconfigured-nginx-alias) for a full exploitation walkthrough of the alias variant.

## 6. HTTP Response-Splitting Attack

**Concept:** A web-based attack in which the attacker tricks the server into injecting **new lines into response headers**, along with arbitrary code. This exploits vulnerabilities in input validation. **XSS, CSRF, and SQL injection** are commonly used as the injection vector for this attack.

### Example walkthrough

Vulnerable server-side code:
```java
String author = request.getParameter(AUTHOR_PARAM);
Cookie webCookie = new Cookie("author", author);
response.addCookie(webCookie);
```

Because `author` is taken directly from user input and placed into a response header (via the `Set-Cookie` header) without sanitizing CR/LF (`\r\n`) characters, an attacker can craft a request whose parameter value contains an injected `\r\n\r\n` sequence, causing the server to interpret the injected text as the **start of a second HTTP response**.

**Attack flow:**
1. The attacker sends a single request that appears to the server as **two** requests (via injected header data).
2. The server splits its response into two: the first response goes back normally; the **second, attacker-controlled response** is cached or delivered to the next victim who requests the same resource, or reflected back with attacker content (e.g. a redirect to a malicious site).
3. Because the web browser discards the first response and processes the (attacker-crafted) second, the victim is served attacker content while remaining unaware anything is wrong.

> 📖 **Defense pointer:** see [08 — How to Defend against HTTP Response-Splitting and Web Cache Poisoning](08-countermeasures-and-hardening.md#5-how-to-defend-against-http-response-splitting-and-web-cache-poisoning).

## 7. Web Cache Poisoning Attack

**Concept:** Damages the reliability of an intermediate web cache source by tricking it into storing a malicious/incorrect response for a given URL. Subsequent users unknowingly receive the poisoned content instead of the true, secured content.

### How it works

1. The attacker forces the web server's cache to **flush its actual content** and sends a specially crafted request that will be stored in cache.
2. The web server responds; the crafted request/response pair is what gets cached.
3. Legitimate users requesting the same page are then served the **poisoned cached response**.

Web cache poisoning is possible when the web server and/or the application has an underlying **HTTP response-splitting** flaw — the two attacks are closely linked.

## 8. SSH Brute Force Attack

Attackers use SSH to create an **encrypted tunnel** between two hosts. Because the tunnel itself is encrypted, transferred data (including exfiltrated data) becomes far harder to inspect on the wire.

- SSH usually runs on **TCP port 22**.
- To perform an attack on SSH, an attacker uses bots to brute-force the entire SSH server on TCP port 22 to identify possible vulnerabilities.
- With the help of a brute-force attack, the attacker obtains login credentials to gain unauthorized access to an SSH tunnel.
- An attacker who obtains valid credentials can use the same SSH tunnel to transmit malware or other means of exploitation to victims being served by the compromised web server, mail server, application server, or file server.
- Common tools: **THC-Hydra** and **Ncrack** on a Linux platform.

```bash
# Example SSH brute-force with Hydra
hydra -L /usr/share/wordlists/ssh-usernames.txt -P /usr/share/wordlists/ssh-passwords.txt ssh://<target-IP>

# Example SSH brute-force with Ncrack
ncrack -p 22 --user root -P /usr/share/wordlists/rockyou.txt <target-IP>
```

## 9. FTP Brute Force with AI

Attackers increasingly use **AI-powered technologies** (e.g. ChatGPT-style shell assistants) to generate and execute brute-force commands automatically, using a natural-language prompt.

**Example prompt:**
> *"Attempt FTP login on target IP 10.10.1.11 with hydra using usernames and passwords from wordlists"*

**Resulting command:**
```bash
hydra -L /usr/share/wordlists/ftp-usernames.txt -P /usr/share/wordlists/ftp-passwords.txt ftp://10.10.1.11
```

| Flag | Meaning |
|---|---|
| `hydra` | Invokes the Hydra brute-force tool |
| `-L /usr/share/wordlists/ftp-usernames.txt` | Path to the **username** wordlist (`-L` = list of usernames) |
| `-P /usr/share/wordlists/ftp-passwords.txt` | Path to the **password** wordlist (`-P` = list of passwords) |
| `ftp://10.10.1.11` | Protocol (FTP) and target IP address; equivalent to `ftp://10.10.1.11:21/` |

**Real captured output (from the courseware lab):**
```
Hydra v9.4 (c) 2022 by van Hauser/THC & David Maciejak
Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-03-14 03:06:19
[DATA] max 16 tasks per 1 server, overall 16 tasks, 2500 login tries (l:50/p:50), ~157 tries per task
[DATA] attacking ftp://10.10.1.11:21
[21][ftp] host: 10.10.1.11   login: Martin   password: apple
1 of 1 target successfully completed, 1 valid password found
```

> 📝 **Note (added):** the `-L`/`-P` flags are for wordlist *files*. Use lowercase `-l`/`-p` instead when testing a *single, known* username/password rather than a list — e.g. `hydra -l admin -p Summer2024! ftp://10.10.1.11`.

## 10. HTTP/2 Continuation Flood Attack

**Concept:** Exploits the handling mechanism of **HTTP/2 CONTINUATION frames** to exhaust the target Apache server. In HTTP/2, headers too large to fit in a single `HEADERS` frame can be split, with the remaining parts sent as a stream of `CONTINUATION` frames. Attackers exploit this by sending numerous `CONTINUATION` frames over a single TCP connection without completing the headers, overwhelming the Apache server's memory/CPU resources and causing a DoS condition.

### How it works, step by step

1. The attacker establishes a TCP connection with the target Apache server.
2. The attacker sends a legitimate `HEADERS` frame. This frame contains headers for a request, with more headers to follow in subsequent `CONTINUATION` frames.
3. Upon receiving the `HEADERS` frame, the Apache server allocates memory and resources to process the frame sent by the attacker.
4. Instead of completing the header sequence by setting the `END_HEADERS` flag, the attacker sends several `CONTINUATION` frames. Each `CONTINUATION` frame indicates that additional header data yet to be obtained.
5. For each received `CONTINUATION` frame, the server allocates additional memory and processing resources to hold the incoming header data.
6. As `CONTINUATION` frames increase, the server memory and CPU resources become overwhelmed.
7. Eventually, the Apache server exhausts its memory or processing capacity, causing it to slow down, crash, or become unresponsive.

## 11. Frontjacking Attack

**Concept:** A web server attack in which an attacker injects or manipulates the front-end components of a web application, such as scripts or HTML elements, to hijack a user interface or user interactions. This attack often targets **poorly configured Nginx reverse proxy servers** in shared hosting environments by combining **CRLF injection, HTTP request header injection, and XSS**.

Attackers exploit flaws in the target reverse proxy configuration, such as improper sanitization of `$uri` and `$document_uri` variables, to inject a new host header to **hijack the execution flow** of the front-end reverse proxy server and consequently replace the accessed backend server with an attacker-controlled server. This allows attackers to display malicious content, redirect users to fake websites, execute reflected XSS and phishing payloads, and inject harmful scripts.

### How a Frontjacking attack works

1. The attacker creates an HTTP request containing CRLF characters in the URI to inject a malicious host header, and sends the request to the vulnerable reverse proxy server.
2. The vulnerable reverse proxy accepts a request containing the malicious host header injected via the CRLF injection.
3. Once the reverse proxy processes the injected host header, it routes the request to the attacker-controlled server instead of the legitimate backend server.
4. The attacker-controlled server responds with malicious content such as phishing pages, malware, or other harmful scripts.

## 12. Other Web Server Attacks

### Web Server Password Cracking

An attacker attempts to exploit weaknesses to hack well-chosen passwords. The most common passwords found are `password`, `root`, `administrator`, `admin`, `demo`, `test`, `guest`, `qwerty`, `pet`, and so on.

Attackers target password cracking through:
- SMTP and FTP servers
- Web shares
- SSH tunnels
- Web form authentication

**Techniques used:**
- **Guessing** — the most common method: trying commonly-used passwords manually or via automated tools/dictionaries (names, license plates, birthdays, "QWERTY," etc.)
- **Dictionary attack** — a predefined file with combinations of words is tested one at a time
- **Brute-force attack** — every possible character combination is tested (much slower, but exhaustive)
- **Hybrid attack** — a combination of a dictionary attack and a brute-force attack

> 📖 **Cross-reference:** see **Module 06: System Hacking** for the complete password-cracking methodology, and [06 — Session Hijacking & Password Cracking](06-session-hijacking-and-password-cracking.md) in this repo for the tools (Hashcat, THC-Hydra, Ncrack) applied specifically to web servers.

### DoS/DDoS Attacks

A DoS/DDoS attack floods a target with excessive requests, consuming server resources: network bandwidth, server memory, application exception-handling mechanisms, CPU usage, hard-disk space, and database space — making it unavailable to legitimate users.

> 📖 **Cross-reference:** see **Module 10: Denial-of-Service** for complete coverage.

### Man-in-the-Middle (MITM) Attack

MITM/sniffing-in-the-middle attacks allow an attacker positioned between an end user and web server to intercept and alter sensitive information exchanged between them. The attacker lures the victim to connect to the web server by pretending to be a proxy; once the victim accepts, all communication between the user and web server passes through the attacker, who can steal sensitive information.

> 📖 **Cross-reference:** see **Module 11: Session Hijacking** for complete coverage.

### Phishing Attacks

Attackers perform phishing by sending an email containing a malicious link that tricks the user into clicking it. The link redirects the victim to a fake website that appears similar to the legitimate one, hosted on the attacker's own server. When the victim clicks the malicious link, their browser is redirected to the malicious website, and they divulge sensitive information (usernames, passwords, bank details, social security numbers), which is used to establish a session with the legitimate website. Later, the attacker uses the victim's stolen credentials to perform malicious operations on the target legitimate website.

> 📖 **Cross-reference:** see **Module 09: Social Engineering** for complete coverage.

### Web Application Attacks

Even if web servers are configured securely and use network security measures such as firewalls, IDS/IPS, if a poorly coded web application deployed on the server carries vulnerabilities, an attacker may be able to compromise the web server using web application attacks:

| Attack | Description |
|---|---|
| **Server-Side Request Forgery (SSRF)** | Attacker exploits server-side request forgery (SSRF) vulnerabilities, which evolve from unsafe use of functions in an application, in public web servers to send crafted requests to internal/backend servers. |
| **Parameter/Form Tampering** | Parameters exchanged between client and server are modified to manipulate application data, such as user credentials and permissions, well as price and quantity of products. |
| **Cookie Tampering** | Cookie-tampering attacks occur when a cookie is sent from the client side to the server; different types of tools help in modifying persistent and non-persistent cookies. |
| **Unvalidated Input and File Injection Attacks** | Unvalidated input and file-injection attacks are performed by supplying an unvalidated input or by injecting files into a web application. |
| **Session Hijacking** | An attack in which the attacker exploits, steals, predicts, and negotiates the real valid web session's control mechanism to access the authenticated state of a web application. |
| **SQL Injection Attacks** | SQL injection exploits the security vulnerability of a database for attacks. The attacker injects malicious code into the string, which are later passed to the SQL server for execution. |
| **Directory Traversal** | Exploitation of HTTP through which attackers can access restricted directories and execute commands outside of the web server's root directory by manipulating a URL. |
| **Denial-of-Service (DoS) Attack** | Intended to terminate the operations of a website or server to make it unavailable to its intended users. |
| **Cross-Site Scripting (XSS) Attacks** | The attacker injects HTML tags or scripts into a target website. |
| **Buffer Overflow Attacks** | The design of most web applications helps them in sustaining some amount of data. If an amount exceeds the storage space available, the application may crash or exhibit other unpredictable behavior. |
| **Cross-Site Request Forgery (CSRF) Attack** | Exploits the trust of an authenticated user to pass malicious code or commands to the web server. |
| **Command Injection Attacks** | A hacker alters the dynamic content of a web page by injecting HTML code and/or client-side scripting via the web page using the form fields that lack valid constraints. |
| **Source Code Disclosure** | A result of typographical errors in scripts or misconfiguration, such as failure to grant executable permissions to a script or directory. Source-code disclosure can occasionally allow attackers to access sensitive information about database credentials and secret keys to compromise the web server. |

> 📖 **Cross-reference:** see **Module 14: Hacking Web Applications** for complete coverage.

---

**Previous:** [← 01 — Web Server Concepts & Architecture](01-web-server-concepts-and-architecture.md) · **Next:** [03 — Attack Methodology: Recon & Footprinting →](03-attack-methodology-recon-and-footprinting.md)
