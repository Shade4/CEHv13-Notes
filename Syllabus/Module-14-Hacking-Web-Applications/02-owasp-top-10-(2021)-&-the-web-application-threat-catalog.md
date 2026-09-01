# 02 — OWASP Top 10 (2021) & the Web Application Threat Catalog

> This file is the map. It walks through the OWASP Top 10 (2021) as the industry-standard threat taxonomy, then catalogs every named attack class covered by the CEH web-application-hacking curriculum. Deep technical walkthroughs (with commands/payloads) for the biggest categories live in their own dedicated files — this file links out to them.

## Table of Contents
- [OWASP Top 10 (2021) Overview](#owasp-top-10-2021-overview)
- [A01: Broken Access Control](#a01-broken-access-control)
- [A02: Cryptographic Failures](#a02-cryptographic-failures)
- [A03: Injection](#a03-injection)
- [A04: Insecure Design](#a04-insecure-design)
- [A05: Security Misconfiguration](#a05-security-misconfiguration)
- [A06: Vulnerable and Outdated Components](#a06-vulnerable-and-outdated-components)
- [A07: Identification and Authentication Failures](#a07-identification-and-authentication-failures)
- [A08: Software and Data Integrity Failures](#a08-software-and-data-integrity-failures)
- [A09: Security Logging and Monitoring Failures](#a09-security-logging-and-monitoring-failures)
- [A10: Server-Side Request Forgery (SSRF)](#a10-server-side-request-forgery-ssrf)
- [The Full CEH Web Application Attack Catalog (35 Named Attacks)](#the-full-ceh-web-application-attack-catalog-35-named-attacks)
- [Where Each Attack Is Covered in This Repo](#where-each-attack-is-covered-in-this-repo)

---

## OWASP Top 10 (2021) Overview

The [OWASP Top 10](https://owasp.org/Top10/) is the most widely referenced ranking of web application risk categories, compiled from real-world vulnerability data contributed by hundreds of organizations. CEH uses it as the backbone for organizing web application threats because it maps cleanly from "root cause" (a category) down to specific, testable attacks.

| # | Category | One-line description |
|---|---|---|
| A01 | Broken Access Control | Users can act outside their intended permissions |
| A02 | Cryptographic Failures | Sensitive data exposed due to weak/missing cryptography |
| A03 | Injection | Untrusted data is interpreted as code/commands |
| A04 | Insecure Design | Missing or ineffective security controls *by design*, not just by implementation |
| A05 | Security Misconfiguration | Insecure default configs, verbose errors, unnecessary features enabled |
| A06 | Vulnerable and Outdated Components | Using libraries/frameworks with known CVEs |
| A07 | Identification and Authentication Failures | Weaknesses in login, session, and credential handling |
| A08 | Software and Data Integrity Failures | Trusting unsigned/unverified code, updates, or serialized data |
| A09 | Security Logging and Monitoring Failures | Attacks go undetected due to poor logging/alerting |
| A10 | Server-Side Request Forgery (SSRF) | Server is tricked into making unintended requests on the attacker's behalf |

---

## A01: Broken Access Control

**What it is:** the application fails to properly enforce what an authenticated (or unauthenticated) user is allowed to do or see. This is consistently the #1 category in real-world findings.

Common manifestations:
- **Insecure Direct Object Reference (IDOR)** — changing an ID in a URL/parameter (`?invoice_id=1002` → `1003`) exposes another user's data because the server never re-checks ownership.
- **Forced browsing** — navigating directly to an admin URL (`/admin/dashboard`) that relies on "security through obscurity" rather than an actual permission check.
- **Privilege escalation** — a regular user manipulates a hidden field, JWT claim, or cookie value to gain admin rights.
- **CORS misconfiguration** — an overly permissive `Access-Control-Allow-Origin` header lets any origin read authenticated responses.
- **Missing function-level access control** — an API endpoint enforces access control on the UI button but not on the underlying HTTP call.

**Quick test:**
```bash
# Access another user's resource by changing an identifier
curl -s -b "session=<your_session_cookie>" "https://target.com/api/orders/1005"
curl -s -b "session=<your_session_cookie>" "https://target.com/api/orders/1006"   # does this return someone else's order?
```

**Defenses:** deny by default, centralize authorization logic server-side, re-check ownership on every object access, log access-control failures, rate-limit API access. Full countermeasure checklist in [10 — Countermeasures & Secure Coding](./10-countermeasures-and-secure-coding.md).

## A02: Cryptographic Failures

**What it is:** sensitive data (credentials, PII, payment data, session tokens) is exposed because it was transmitted or stored with weak, deprecated, or absent cryptography.

Common causes:
- Data transmitted in cleartext (HTTP instead of HTTPS, unencrypted internal service calls).
- Use of deprecated algorithms/protocols: MD5, SHA-1 for password hashing, RC4, SSLv3/TLS 1.0.
- Hard-coded or predictable encryption keys and initialization vectors (IVs); IV reuse in CBC mode.
- Home-grown "encryption" (e.g., simple character substitution followed by Base64 — Base64 is **encoding**, not encryption, and is trivially reversible).

Example of a broken "encryption" routine actually seen in vulnerable training code:
```java
// VULNERABLE — this is obfuscation, not encryption
public String encrypt(String plainText) {
    plainText = plainText.replace("a", "z");
    plainText = plainText.replace("b", "y");
    // ... more character substitution ...
    return Base64Encoder.encode(plainText);
}
```
A substitution cipher wrapped in Base64 provides effectively zero real protection — it's reversible by inspection.

**Defenses:** enforce TLS 1.2+ everywhere (HSTS), use vetted libraries for hashing (bcrypt/scrypt/Argon2 for passwords, never raw MD5/SHA-1), generate IVs with a cryptographically secure RNG and never reuse them, store keys in a dedicated secrets manager/HSM, disable legacy cipher suites.

## A03: Injection

**What it is:** untrusted input is concatenated into a command, query, or interpreter call without proper validation/escaping, so the interpreter executes attacker-supplied logic instead of (or in addition to) the intended logic.

This is the single largest category by attack-technique count and gets its own dedicated deep-dive: **[04 — Injection Attacks →](./04-injection-attacks.md)** (SQL injection, command injection, LDAP injection, XPath injection, SSTI, SSI, CRLF injection, file inclusion).

## A04: Insecure Design

**What it is:** a flaw that exists even if the code is implemented perfectly, because the *design itself* never accounted for the abuse case. This is different from a coding bug — it's a missing requirement.

Examples:
- A password-reset flow that doesn't rate-limit OTP attempts (design gap) vs. a rate limiter with an off-by-one bug (implementation bug).
- A "forgot password" feature that emails the *new* password instead of a reset link.
- A checkout flow that trusts the client-submitted price for a product ([Business Logic Bypass](./08-other-web-app-attacks.md#business-logic-bypass-attack)).

**Mitigation approach:** threat modeling during design, secure design patterns, reference architectures, and abuse-case user stories alongside normal feature user stories — see [10 — Countermeasures](./10-countermeasures-and-secure-coding.md#insecure-design).

## A05: Security Misconfiguration

**What it is:** the application, server, framework, or platform ships with an insecure default, an unnecessary feature left on, or a mistake made during deployment.

Common examples:
- Default credentials left unchanged (`admin`/`admin`).
- Directory listing enabled, exposing file structure.
- Verbose stack traces/error messages returned to the client, leaking framework versions and file paths.
- Unnecessary HTTP methods enabled (`TRACE`, `PUT`, `DELETE` on a public endpoint).
- Cloud storage buckets (S3, Azure Blob) left publicly readable/writable.
- Missing security headers (`Content-Security-Policy`, `X-Frame-Options`, `Strict-Transport-Security`).

**Quick test:**
```bash
curl -I https://target.com                      # check response headers
curl -X TRACE https://target.com                 # check if TRACE is enabled (can enable XST)
curl -X OPTIONS -i https://target.com/api/users  # enumerate allowed methods
```

## A06: Vulnerable and Outdated Components

**What it is:** the application depends on a library, framework, plugin, OS package, or CMS with a publicly known vulnerability (a CVE), and the vulnerable component was never patched or replaced.

Why it's dangerous: an attacker doesn't need to find a new bug — they just need to **fingerprint** your stack (via [technology-detection tooling](./03-footprinting-and-recon.md#detecting-web-application-technologies)) and match it against public exploit databases (Exploit-DB, Metasploit modules, NVD).

**Quick check workflow:**
```bash
whatweb https://target.com                 # fingerprint CMS/framework/plugin versions
searchsploit wordpress 6.2                 # check Exploit-DB for known issues in that version
npm audit                                  # for a Node.js codebase you control
pip-audit                                  # for a Python codebase
```

**Defenses:** maintain a Software Bill of Materials (SBOM), subscribe to CVE feeds for every dependency, automate dependency scanning in CI/CD (Dependabot, Snyk, OWASP Dependency-Check), remove components you don't actually use.

## A07: Identification and Authentication Failures

**What it is:** weaknesses in how the application verifies *who* a user is and *keeps* verifying it across a session. Covered in depth in **[06 — Session, Authentication & Authorization Attacks →](./06-session-authentication-and-authorization-attacks.md)**.

At a glance, this category includes:
- **Session ID exposed in the URL** — e.g. `http://shop.example.com/sale?jsessionid=12OMTOIDPXM0OQSABGCKLHCJUN2JV`; if it leaks via referrer headers, browser history, or shoulder-surfing, an attacker can hijack the session outright.
- **Password exploitation** — weak hashing, no salting, credential stuffing.
- **Timeout exploitation** — sessions that never expire, so a stolen cookie remains valid indefinitely.
- **Bad passwords / brute-forcible login** — no lockout, no rate limiting, no CAPTCHA after repeated failures.
- **Verbose failure messages** — "invalid password" vs. "invalid username" tells an attacker which half of the credential pair was wrong, enabling user enumeration.

## A08: Software and Data Integrity Failures

**What it is:** code or data whose integrity was never cryptographically verified before being trusted — this includes **insecure deserialization**, unsigned software updates, and CI/CD pipelines that pull unverified dependencies.

**Insecure deserialization deep dive:** when an application deserializes attacker-controlled data (a serialized Java object, PHP object, Python pickle, or .NET `BinaryFormatter` payload) without validation, the deserialization process itself can trigger method calls, meaning an attacker can potentially achieve remote code execution purely by crafting a malicious serialized blob — no traditional "injection point" is even needed.

```
Employee Object → Serialization → 
  rO0ABXNyABFFbXBsb3llZQAAAAAAAAAB... (attacker modifies the byte stream) →
Deserialization → Employee Object (with tampered fields, or a gadget chain that executes code)
```

**Defenses:** never deserialize data from an untrusted source using a format capable of instantiating arbitrary classes; if you must, use integrity checks (HMAC/digital signatures) on the serialized blob, prefer data-only formats (JSON) over object-graph formats, and use deserialization allow-lists.

## A09: Security Logging and Monitoring Failures

**What it is:** an attack succeeds — or a breach continues for months — because the application didn't log the relevant events, didn't alert on suspicious patterns, or logs were never reviewed.

Typical gaps:
- Login failures, access-control failures, and input-validation failures aren't logged at all.
- Logs are stored only locally and are wiped/overwritten before anyone reviews them.
- No alerting threshold — a single account with 10,000 failed logins in an hour triggers nothing.
- Logs lack enough context (no user ID, source IP, or timestamp) to reconstruct an incident.

**Defenses:** centralize logs (SIEM: Splunk, ELK, Microsoft Sentinel), log all authentication and access-control decisions, set alerting thresholds tied to real abuse patterns, retain logs long enough to support forensic investigation, and protect log integrity so an attacker can't erase their own tracks.

## A10: Server-Side Request Forgery (SSRF)

**What it is:** the application accepts a URL or hostname from the user and fetches it *server-side* — and the attacker abuses this to make the server issue requests it never should have, often reaching internal-only resources (cloud metadata services, admin panels, internal APIs) that are unreachable from the public internet.

**Classic exploitation pattern:**
```
POST /fetch-avatar-from-url HTTP/1.1
Host: target.com

url=http://169.254.169.254/latest/meta-data/iam/security-credentials/
```
If the backend server dutifully fetches whatever URL it's given, an attacker can pivot from "harmless image importer" to reading **cloud IAM credentials** from the instance metadata service — one of the most damaging SSRF outcomes in cloud-hosted applications (this exact class of bug was central to a well-known 2019 breach at a major U.S. financial institution).

**Defenses:** maintain an allow-list of permitted destination hosts/schemes, disable HTTP redirects on server-side fetches (or re-validate after every redirect), block requests to link-local/private IP ranges (`169.254.0.0/16`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`), and run the fetching component in a network-segmented, credential-less context.

---

## The Full CEH Web Application Attack Catalog (35 Named Attacks)

Beyond the OWASP Top 10 framing, the CEH curriculum names 35 distinct web application attacks. Below is the complete catalog, grouped by theme, each with a one-line definition and a pointer to where the deep dive lives.

### Injection-family
| Attack | Definition | Details |
|---|---|---|
| SQL Injection | Malicious SQL inserted into a query via unsanitized input | [04](./04-injection-attacks.md#sql-injection) |
| Command Injection | OS shell commands injected via an application input that reaches a system call | [04](./04-injection-attacks.md#os-command-injection) |
| LDAP Injection | Malicious LDAP filter syntax injected into a directory query | [04](./04-injection-attacks.md#ldap-injection) |
| XML External Entity (XXE) | Malicious external entity in XML input reads local files or triggers SSRF | [07](./07-web-services-api-and-webhook-attacks.md#xml-external-entity-xxe) |

### Cross-site / client-side family
| Attack | Definition | Details |
|---|---|---|
| Cross-Site Scripting (XSS) | Attacker script runs in a victim's browser under the target's origin | [05](./05-xss-csrf-and-client-side-attacks.md#cross-site-scripting-xss) |
| Cross-Site Request Forgery (CSRF) | Victim's browser is tricked into submitting an authenticated request | [05](./05-xss-csrf-and-client-side-attacks.md#cross-site-request-forgery-csrf) |
| Clickjacking | Invisible iframe tricks a user into clicking something other than what they see | [05](./05-xss-csrf-and-client-side-attacks.md#clickjacking) |
| JavaScript Hijacking | Attacker page reads sensitive JSON via a hijacked `<script>` include | [05](./05-xss-csrf-and-client-side-attacks.md#javascript-hijacking) |
| Cross-Site WebSocket Hijacking | Cross-origin page opens a WebSocket that inherits the victim's session | [05](./05-xss-csrf-and-client-side-attacks.md#cross-site-websocket-hijacking) |
| DOM-based attacks | Client-side script itself creates the vulnerability, no server round-trip needed | [05](./05-xss-csrf-and-client-side-attacks.md#dom-based-xss) |

### Session & cookie family
| Attack | Definition | Details |
|---|---|---|
| Cookie/Session Poisoning | Modifying cookie contents to escalate privilege or impersonate another user | [06](./06-session-authentication-and-authorization-attacks.md#cookiesession-poisoning) |
| Cookie Snooping | Passive interception of cookies in transit (e.g., over unencrypted Wi-Fi) | [06](./06-session-authentication-and-authorization-attacks.md#cookie-snooping) |
| Pass-the-Cookie Attack | Replaying a stolen authentication cookie on another device/browser | [06](./06-session-authentication-and-authorization-attacks.md#pass-the-cookie-attack) |
| Same-Site Attack | Abusing a dangling subdomain that shares a parent domain's cookie scope | [06](./06-session-authentication-and-authorization-attacks.md#same-site-attack) |
| RC4 NOMORE Attack | Statistical bias in the RC4 cipher used to decrypt secure cookies over time | [06](./06-session-authentication-and-authorization-attacks.md#rc4-nomore-attack) |

### Data & logic family
| Attack | Definition | Details |
|---|---|---|
| Hidden Field Manipulation | Editing a hidden HTML form field (e.g., price) before submission | [08](./08-other-web-app-attacks.md#hidden-field-manipulation) |
| Business Logic Bypass Attack | Abusing legitimate application flow in an unintended sequence/order | [08](./08-other-web-app-attacks.md#business-logic-bypass-attack) |
| Insecure Deserialization | Untrusted serialized object triggers code execution or logic tampering on deserialize | [08](./08-other-web-app-attacks.md#insecure-deserialization) |
| Buffer Overflow | Oversized input overwrites adjacent memory, crashing or hijacking execution | [08](./08-other-web-app-attacks.md#buffer-overflow) |
| CAPTCHA Attacks | Automated bypass/solving of CAPTCHA challenges (OCR, solver farms, replay) | [08](./08-other-web-app-attacks.md#captcha-attacks) |
| Web-based Timing Attacks | Inferring secret data from response-time differences | [08](./08-other-web-app-attacks.md#web-based-timing-attacks) |
| Platform Exploits | Exploiting a known vulnerability in the underlying platform/framework itself | [08](./08-other-web-app-attacks.md#platform-exploits) |
| Obfuscation Application | Attacker obfuscates malicious payloads/traffic to evade detection | [08](./08-other-web-app-attacks.md#obfuscation-application) |

### Redirect & supply-chain family
| Attack | Definition | Details |
|---|---|---|
| Unvalidated Redirects and Forwards | App redirects to an attacker-supplied URL, aiding phishing | [08](./08-other-web-app-attacks.md#unvalidated-redirects-and-forwards) |
| Directory Traversal | `../` sequences escape the intended directory to read arbitrary files | [08](./08-other-web-app-attacks.md#directory-traversal) |
| Magecart Attack | Malicious JS skimmer injected into a checkout page (often via 3rd-party script) | [08](./08-other-web-app-attacks.md#magecart-attack) |
| Watering Hole Attack | Compromising a site the target audience is known to frequent | [08](./08-other-web-app-attacks.md#watering-hole-attack) |
| MarioNet Attack | Abusing Service Workers to keep executing code after the tab is closed | [08](./08-other-web-app-attacks.md#marionet-attack) |

### Network / protocol family
| Attack | Definition | Details |
|---|---|---|
| Denial-of-Service (DoS) | Exhausting server resources so legitimate users can't get service | [08](./08-other-web-app-attacks.md#denial-of-service-dos) |
| DNS Rebinding Attack | DNS answer changes after the same-origin check, tricking the browser into treating an external host as same-origin | [08](./08-other-web-app-attacks.md#dns-rebinding-attack) |
| H2C Smuggling Attack | Abusing HTTP/2 cleartext upgrade to smuggle requests past a proxy | [08](./08-other-web-app-attacks.md#h2c-smuggling-attack) |
| Cross-Site Port Attack (XSPA) | Using a server-side fetch feature to port-scan internal hosts | [07](./07-web-services-api-and-webhook-attacks.md#cross-site-port-attack-xspa) |
| Injecting an SSRF Payload | See [A10 above](#a10-server-side-request-forgery-ssrf) | [07](./07-web-services-api-and-webhook-attacks.md#ssrf-in-apis) |
| Network Access Attacks | Attacking the network layer supporting the web app (open ports/services) | [08](./08-other-web-app-attacks.md#network-access-attacks) |
| DMZ Protocol Attacks | Exploiting protocols permitted through the DMZ (e.g., weakly filtered ICMP/DNS) | [08](./08-other-web-app-attacks.md#dmz-protocol-attacks) |

### Web services family
| Attack | Definition | Details |
|---|---|---|
| Web Service Attacks | Umbrella term for SOAP/REST-specific attacks (XML injection, SOAPAction spoofing, WS-Address spoofing, parsing/probing attacks) | [07](./07-web-services-api-and-webhook-attacks.md) |

---

## Where Each Attack Is Covered in This Repo

| File | Covers |
|---|---|
| [03-footprinting-and-recon.md](./03-footprinting-and-recon.md) | Reconnaissance phase preceding all of the above |
| [04-injection-attacks.md](./04-injection-attacks.md) | SQLi, command injection, LDAP/XPath injection, SSTI, SSI, CRLF, LFI/RFI |
| [05-xss-csrf-and-client-side-attacks.md](./05-xss-csrf-and-client-side-attacks.md) | XSS, CSRF, clickjacking, JS hijacking, WebSocket hijacking |
| [06-session-authentication-and-authorization-attacks.md](./06-session-authentication-and-authorization-attacks.md) | Auth attacks, session attacks, authorization/access-control attacks |
| [07-web-services-api-and-webhook-attacks.md](./07-web-services-api-and-webhook-attacks.md) | SOAP/REST/API/webhook/XXE/SSRF |
| [08-other-web-app-attacks.md](./08-other-web-app-attacks.md) | Every remaining named attack from the 35-item catalog |
| [09-web-app-hacking-tools.md](./09-web-app-hacking-tools.md) | Tool-by-tool command reference across every phase |
| [10-countermeasures-and-secure-coding.md](./10-countermeasures-and-secure-coding.md) | Defenses mapped back to every category above |

---

**Previous:** [← 01 — Web Application Concepts](./01-web-application-concepts.md) · **Next:** [03 — Footprinting & Reconnaissance →](./03-footprinting-and-recon.md)
