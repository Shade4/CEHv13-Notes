# 06 — Session Hijacking & Password Cracking

> Objective covered: **Explain Web Server Attack Methodology** (Phases 5–6: Session Hijacking & Web Server Password Hacking)

## Phase 5 — Session Hijacking

Valid session IDs can be sniffed to gain unauthorized access to a web server. An attacker can hijack or steal valid session IDs using various techniques such as **session token prediction, session fixation, side-jacking**, and by using these techniques, the attacker attempts to hijack sessions. An attacker uses tools such as **Burp Suite**, **JHijack**, and **Ettercap** to automate session hijacking.

### Burp Suite

- **Source:** https://portswigger.net
- A web security testing tool that can hijack session IDs in established sessions. With Burp Suite's **Sequencer** tool, an attacker can test the randomness of session tokens. Using this tool, an attacker can predict the next possible session ID token and use it to take over a valid session.

### Additional Session Hijacking Tools

| Tool | Source |
|---|---|
| JHijack | https://sourceforge.net |
| Ettercap | https://www.ettercap-project.org |

> 📖 **Cross-reference:** for complete coverage of concepts and techniques related to session hijacking, refer to **Module 11: Session Hijacking**.

---

## Phase 6 — Web Server Password Hacking

In this phase of web server hacking, an attacker attempts to crack web server passwords. The attacker may employ all possible techniques of password cracking to extract passwords, including **password guessing, dictionary attacks, hybrid attacks, precomputed hashes, rule-based attacks, distributed network attacks, and rainbow tables**. The attacker needs patience to crack passwords because some of these techniques are tedious and time-consuming. The attacker can also use automated tools such as **Hashcat**, **THC-Hydra**, and **Ncrack** to crack web passwords and hashes.

### Hashcat

- **Source:** https://hashcat.net
- A cracker compatible with multiple OSs and platforms that can perform multi-hash (MD4, 5; SHA – 224, 256, 384, 512; RIPEMD-160, etc.), multi-device password cracking. Attack modes of this tool are: straight, combination, brute-force, hybrid dict + mask, and hybrid mask + dict.

```bash
# Crack an NTLM hash dump using a wordlist (straight attack, mode 0 = MD5 shown as example structure)
hashcat -m 1000 -a 0 ntlm_hashes.txt /usr/share/wordlists/rockyou.txt

# Brute-force mode against a SHA-256 hash (mask attack, -a 3)
hashcat -m 1400 -a 3 sha256_hashes.txt ?a?a?a?a?a?a?a?a

# Hybrid: dictionary + mask (append 4 digits to each dictionary word)
hashcat -m 0 -a 6 md5_hashes.txt /usr/share/wordlists/rockyou.txt ?d?d?d?d
```

### THC-Hydra

- **Source:** https://github.com
- A parallelized login cracker that provides researchers and security consultants the possibility to show how easy it would be to gain unauthorized access to a system remotely.
- Currently supports the following protocols: **Asterisk, AFP, Cisco AAA, Cisco Authorization, Cisco enable, CVS, Firebird, FTP, HTTP(S)-FORM-GET, HTTP(S)-FORM-POST, HTTP(S)-GET, HTTP(S)-HEAD, HTTP-Proxy, HTTPS-FORM-GET, HTTPS-FORM-POST, HTTPS-GET, HTTPS-HEAD, ICQ, IMAP, IRC, LDAP, MEMCACHED, MongoDB, MS-SQL, MySQL, NCP, NNTP, Oracle Listener, Oracle SID, PC-Anywhere, pcNFS, POP3, Postgres, Radmin, RDP (Remote Desktop Protocol), Rexec, Rlogin, Rsh, RTSP, SAP/R3, SIP, SMB, SMTP, SMTP Enum, SNMP v1+v2+v3, SOCKS5, SSH (v1 and v2), SSH key, Subversion, TeamSpeak (TS2), Telnet, VMware-Auth, VNC (Virtual Network Computing), and XMPP.**

```bash
# HTTP basic-auth brute force
hydra -L users.txt -P passwords.txt <target-IP> http-get /admin/

# HTTP POST-form brute force (login form)
hydra -l admin -P /usr/share/wordlists/rockyou.txt <target-IP> \
  http-post-form "/login.php:username=^USER^&password=^PASS^:Invalid credentials"

# RDP brute force
hydra -l administrator -P passwords.txt rdp://<target-IP>
```

### Additional Password-Cracking Tools

| Tool | Source |
|---|---|
| Ncrack | https://nmap.org |
| Rainbow Crack | https://project-rainbowcrack.com |
| Wfuzz | http://www.edge-security.com |
| Wireshark | https://www.wireshark.org |

> 📖 **Cross-reference:** for complete coverage of password-cracking attacks, refer to **Module 06: System Hacking**.

---

## Using an Application Server as a Proxy

Web servers are occasionally configured to perform functions such as **forwarding or serving HTTP proxy**. Web servers with these functions enabled are employed by attackers to perform the following attacks:

- Attacking third-party systems on the internet
- Connecting to arbitrary hosts on the organization's internal network
- Connecting back to other services running on the proxy host itself

```
   Attacker ──GET/CONNECT Requests──> Proxy Web Server ──GET/CONNECT Requests──> Target Systems
                                       (Requested Information)                   (Requested Information)
```
*(Figure 13.59 equivalent — illustration of the use of an application server as a proxy)*

If an attacker finds a web server that will proxy requests, they can use it to launder attack traffic — making the compromised web server appear to be the source of subsequent attacks, rather than the attacker's real IP.

> 📝 **Note (added):** this is the same underlying class of vulnerability as modern **SSRF (Server-Side Request Forgery)** — see [02 — Web Application Attacks table](02-web-server-attack-techniques.md#web-application-attacks) for the broader SSRF context, and always disable open-proxy behavior (`proxy_pass` to arbitrary user-controlled hosts, HTTP CONNECT tunneling) on production web servers unless explicitly required and access-controlled.

---

**Previous:** [← 05 — Vulnerability Scanning & Exploitation](05-vulnerability-scanning-and-exploitation.md) · **Next:** [07 — Web Server Attack Tools →](07-web-server-attack-tools.md)
