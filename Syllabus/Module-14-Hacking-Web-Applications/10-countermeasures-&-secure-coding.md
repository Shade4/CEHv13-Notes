# 10 — Countermeasures & Secure Coding

> Every attack in this repo has a corresponding defense. This file is organized so a defender can go from "which category am I worried about" straight to "what do I actually configure/code/deploy" — plus the testing methodology (SAST/DAST/manual) and infrastructure controls (WAF/RASP) that catch what secure coding alone misses.

## Table of Contents
- [Web Application Security Testing Methodology](#web-application-security-testing-methodology)
- [Static Application Security Testing (SAST)](#static-application-security-testing-sast)
- [Dynamic Application Security Testing (DAST)](#dynamic-application-security-testing-dast)
- [AI-Powered Application Security Testing](#ai-powered-application-security-testing)
- [Source Code Review](#source-code-review)
- [Encoding Schemes](#encoding-schemes)
- [Whitelisting vs. Blacklisting](#whitelisting-vs-blacklisting)
- [Content Filtering](#content-filtering)
- [Defending Against Injection Attacks](#defending-against-injection-attacks)
- [General Web Application Attack Countermeasures](#general-web-application-attack-countermeasures)
- [Countermeasures by OWASP Category](#countermeasures-by-owasp-category)
- [Session, Cookie & Redirect-Specific Defenses](#session-cookie--redirect-specific-defenses)
- [WebSocket Security Best Practices](#websocket-security-best-practices)
- [Runtime Application Self-Protection (RASP)](#runtime-application-self-protection-rasp)
- [Web Application Security Testing Tools](#web-application-security-testing-tools)
- [Web Application Firewalls (WAF)](#web-application-firewalls-waf)
- [Security Headers Checklist](#security-headers-checklist)

---

## Web Application Security Testing Methodology

Two complementary approaches, neither of which fully replaces the other:

| Approach | What it means | Strength | Weakness |
|---|---|---|---|
| **Manual testing** | A skilled tester manually explores the app, thinks about business logic, and crafts targeted attacks | Catches business-logic flaws and chained/creative exploits automated tools miss entirely | Slow, doesn't scale, quality depends heavily on the individual tester |
| **Automated testing** | Tools (scanners, fuzzers) systematically probe the app for known vulnerability signatures | Fast, repeatable, good for regression testing and broad coverage | High false-positive/false-negative rate on anything requiring business context |

A mature security program uses **both**: automated scanning (SAST + DAST) integrated into CI/CD for continuous coverage, plus periodic manual penetration testing for the classes of bugs automation structurally cannot find.

## Static Application Security Testing (SAST)

**What it is:** analyzing an application's **source code** (without running it) to find vulnerable patterns — unsanitized input reaching a dangerous sink, hardcoded secrets, use of deprecated cryptographic functions.

**Strengths:** finds bugs before deployment, pinpoints the exact vulnerable line of code, integrates naturally into a pull-request/CI gate.
**Weaknesses:** language/framework-specific, higher false-positive rate on complex data flows, can't find issues that only manifest at runtime (misconfigurations, environment-specific bugs).

**Representative tools:**
| Tool | Notes |
|---|---|
| **Snyk Code** | AI-assisted SAST integrated with Snyk's broader dependency-scanning platform |
| **Checkmarx CxSAST** | Enterprise-grade, broad language support, deep data-flow analysis |
| **Corgea** | AI-powered SAST focused on automating vulnerability triage and even suggesting fixes |
| **CodeThreat** | Cloud-based SAST platform for CI/CD integration |
| **Codigo (Codigo AI)** | AI-assisted secure code analysis and remediation suggestions |

```bash
# Example: running an open-source SAST tool (Semgrep) against a codebase locally
pip install semgrep --break-system-packages
semgrep --config=p/owasp-top-ten ./src
```

## Dynamic Application Security Testing (DAST)

**What it is:** testing the **running** application from the outside — exactly like an attacker would — by sending crafted HTTP requests and observing responses, without any access to source code.

**Strengths:** finds real, exploitable runtime issues (including misconfigurations SAST can't see), language-agnostic.
**Weaknesses:** requires a running, reachable instance; typically finds the vulnerability's *symptom* rather than the exact line of code causing it; can miss logic flaws that don't produce an obviously anomalous response.

**Core open-source DAST tools:** OWASP ZAP, Burp Suite (with the active scanner in the paid edition), Nikto, Wapiti — all covered in [09 — Web Application Hacking Tools](./09-web-app-hacking-tools.md).

## AI-Powered Application Security Testing

CEH v13 highlights a growing category of AI-augmented scanning tools that layer machine learning on top of traditional SAST/DAST:

**AI-powered DAST** — tools like **ZeroThreat.ai** actively interact with a running application (rather than just pattern-matching static rules), using an AI-driven crawler to navigate complex apps/APIs, integrate threat-intelligence feeds to detect emerging attack patterns, and significantly reduce false positives so security teams spend less time triaging noise. Other tools in this space: **Apiiro**, **Pentest Copilot**, **Hackuity**, **Beagle Security**, **Vanaide**.

Key capabilities this category of tooling typically adds over traditional DAST:
- **Self-learning and adaptation** — models continuously improve test strategy based on prior successful findings.
- **Automation and CI/CD integration** — automates repetitive test execution and initial triage, enabling "shift-left" security earlier in the development pipeline.
- **Complex attack-chain simulation** — chaining multiple lower-severity findings into a realistic, higher-impact exploit path a human might otherwise miss.

**AI-powered SAST** works similarly on the static side — models trained on vulnerability patterns flag risky code with fewer false positives than purely rule-based static analyzers, and some tools (e.g., Corgea, Codigo) go a step further by suggesting or even auto-generating the fix.

**A word of caution:** AI-assisted tools are a productivity multiplier, not a replacement for understanding *why* a finding matters — always have a qualified human review AI-generated findings and any AI-suggested remediation before merging it into production code.

## Source Code Review

Even without a formal SAST tool, structured manual code review catches classes of bugs automated tools miss (business logic, authorization gaps spanning multiple files, subtle race conditions).

**A focused review checklist:**
- Trace every user-input entry point to its eventual sink (database query, shell call, template render, file path, HTTP redirect target) — is it validated/encoded appropriately at that sink?
- Search for hardcoded credentials/API keys: `grep -rn "password\s*=\|api_key\s*=\|secret\s*=" ./src`
- Check every authorization decision is made server-side, freshly, on every request — not cached from an earlier check or trusted from client input.
- Confirm cryptographic functions in use are current (no MD5/SHA-1 for passwords, no ECB mode, no hardcoded IVs/keys).
- Review error handling — does a caught exception leak a stack trace, file path, or query string to the client?

## Encoding Schemes

Understanding encoding is essential both for **crafting** filter-evasion payloads during testing and for **implementing correct output encoding** as a defense.

| Scheme | Example | Where it matters |
|---|---|---|
| **URL Encoding** | `<` → `%3C`, space → `%20` | Query strings, path segments |
| **HTML Entity Encoding** | `<` → `&lt;`, `"` → `&quot;` | Rendering user input inside HTML body/attributes — the primary XSS defense |
| **Unicode Encoding** | `<` → `\u003C` | JavaScript string contexts, sometimes used to bypass naive filters checking only for literal ASCII characters |
| **Base64 Encoding** | `admin` → `YWRtaW4=` | Data transport (not encryption!) — commonly (mis)used to "hide" values that are trivially decodable |
| **Hex Encoding** | `A` → `%41` or `\x41` | Alternate evasion encoding, especially inside CSS/JS contexts |

**Critical principle for defenders — context-aware output encoding:** the *correct* encoding function depends entirely on *where* the data is being inserted. HTML-encoding data placed inside a `<script>` block, a URL attribute, or a CSS value does **not** provide adequate protection — each context requires its own matching encoder (HTML-entity encoder for HTML body, JavaScript string encoder for JS contexts, URL encoder for URL contexts, CSS hex encoder for CSS contexts). This is the root cause of a huge fraction of "we already escape user input, why is this still XSS-able" bugs.

## Whitelisting vs. Blacklisting

| Approach | Definition | Security Posture |
|---|---|---|
| **Whitelisting (allow-listing)** | Explicitly define what *is* permitted; reject everything else by default | **Strongly preferred** — fails safe, resistant to novel bypass techniques |
| **Blacklisting (deny-listing)** | Explicitly define what's *forbidden*; allow everything else by default | Fragile — every bypass technique not yet on the list slips through |

**Application whitelisting** (controlling which *executables* are permitted to run on a host) and **application blacklisting** (blocking known-bad executables/hashes) are complementary endpoint controls, distinct from but related to input validation whitelisting:
- **Application whitelisting tools:** ManageEngine Application Control Plus, GlobalProtect, Symantec Endpoint Application Control, ThreatLocker, PowerAdmin.
- Whitelisting a set of permitted applications and blocking everything else by default is dramatically more effective against unknown/novel malware than trying to maintain an ever-growing blacklist.

**Applied to input validation specifically:** always prefer defining the exact permitted character set/format/length for a given field (e.g., "a US zip code is exactly 5 digits, optionally followed by a hyphen and 4 more digits") over trying to enumerate every malicious pattern to reject.

## Content Filtering

Content filtering tools/gateways control and restrict access to potentially malicious or inappropriate content, and can enforce policy at the network egress point regardless of what any individual application does internally.

**Representative tools:** Forcepoint URL Filtering, Cisco Umbrella, Symantec Web Security, Barracuda Web Security Gateway, OpenDNS.

## Defending Against Injection Attacks

Consolidated from the per-attack detail in [04 — Injection Attacks](./04-injection-attacks.md):

**SQL Injection:**
- Use parameterized queries / prepared statements — **never** string-concatenate user input into SQL.
- Use an ORM with proper parameter binding as an added layer, understanding that raw/dynamic query escape hatches within an ORM can reintroduce the same risk.
- Enforce least-privilege database accounts (the web app's DB user should not have `DROP`/`ALTER`/cross-database privileges it doesn't need).
- Validate input type/format/length before it ever reaches the query layer, as defense-in-depth (not a substitute for parameterization).
- Disable verbose database error messages in production responses.

**OS Command Injection:**
- Avoid invoking a system shell at all wherever a language-native API exists (e.g., use a library's native file-copy function instead of shelling out to `cp`).
- Where shelling out is unavoidable, pass arguments as an array (never a single concatenated string) so the shell never re-interprets metacharacters.
- Validate input against a strict allow-list of expected values.

**LDAP Injection:**
- Use parameterized LDAP query APIs.
- Escape LDAP special characters (`( ) * \ NUL`) in any input reaching a filter.
- Use a least-privilege bind account for the application's own directory queries.

**Server-Side Injection (SSTI/SSI):**
- Never render user-supplied input as a template string — always pass it as a template *variable*.
- Disable server-side includes (or at minimum the `exec` directive) on any endpoint that doesn't explicitly require them.

**XSS:**
- Apply context-aware output encoding at every injection point (see [Encoding Schemes](#encoding-schemes) above).
- Deploy a strict Content-Security-Policy (`script-src 'self'`, avoiding `'unsafe-inline'`/`'unsafe-eval'` wherever feasible).
- Set `HttpOnly` on session cookies so JavaScript (including an injected XSS payload) cannot read them at all.

**CRLF Injection:**
- Strip or reject `\r`/`\n` characters before writing user input into any HTTP header or log line.
- Use your framework's built-in, safe header-setting APIs rather than manually concatenating header strings.

**XML Injection / XXE:**
- Disable DTD processing and external entity resolution in the XML parser configuration — this single setting change eliminates the entire XXE attack class.
- Prefer JSON over XML for new APIs where the additional XML-specific features (namespaces, schemas) aren't actually required.

## General Web Application Attack Countermeasures

A checklist of architecture-level principles that reduce the blast radius of *any* individual vulnerability that slips through:

- **Insecure Design mitigation — threat modeling.** Model threats (e.g., STRIDE) during the design phase, before a single line of code is written, so abuse cases are considered alongside feature requirements.
- **Architectural risk analysis.** Periodically re-review the system's trust boundaries as it evolves — a component added six months ago may have quietly changed the threat model.
- **Secure design patterns.** Reuse vetted architectural patterns (e.g., a centralized authorization service) rather than re-implementing security-critical logic independently in every module.
- **Defense in depth.** Never rely on a single control — a WAF rule blocking SQLi is not a substitute for parameterized queries; both should exist simultaneously.
- **Fail securely.** When an error occurs mid-operation (a permission check throws an exception, a database call times out), the default behavior must be to *deny* the action, not silently allow it.
- **Minimize attack surface.** Disable every feature, endpoint, HTTP method, and default account that isn't actually needed in production.
- **Secure by default.** Ship the most restrictive configuration out of the box; require an explicit, deliberate action to loosen a security control, never the reverse.

## Countermeasures by OWASP Category

**A01 — Broken Access Control:**
- Deny by default; explicitly grant access rather than explicitly denying it.
- Enforce access-control checks server-side, on every request, re-derived from authoritative data — never trust a client-supplied role/permission value.
- Log access-control failures and alert when a high rate of them occurs from a single account/IP.
- Rate-limit API access to reduce the practicality of automated ID enumeration.

**A02 — Cryptographic Failures:**
- Enforce TLS 1.2+ everywhere; enable HSTS.
- Use vetted, modern hashing for passwords (bcrypt/scrypt/Argon2) — never MD5/SHA-1, never unsalted.
- Generate IVs/nonces with a cryptographically secure RNG, never reuse them.
- Store cryptographic keys in a dedicated secrets manager/HSM, never in source code or config files committed to version control.

**A05 — Security Misconfiguration:**
- Remove/rotate default credentials on every component immediately after installation.
- Disable directory listing and verbose error pages in production.
- Restrict HTTP methods to only those genuinely required (`GET`, `POST`, sometimes `PUT`/`DELETE` for REST APIs — disable `TRACE`, `CONNECT`, and unused verbs).
- Apply the full [security headers checklist](#security-headers-checklist) below.

**A06 — Vulnerable and Outdated Components:**
- Maintain a Software Bill of Materials (SBOM) for every application.
- Automate dependency scanning in CI/CD (Dependabot, Snyk, OWASP Dependency-Check) and fail the build on critical findings.
- Remove unused dependencies; each one is attack surface even if never directly called.

**A07 — Identification and Authentication Failures:**
- Enforce a strong password policy and check new passwords against known-breached-password lists.
- Implement account lockout/exponential backoff after repeated failed logins.
- Offer and, for sensitive accounts, require multi-factor authentication.
- Ensure session identifiers are never exposed in the URL.

**A08 — Software and Data Integrity Failures:**
- Never deserialize untrusted data with an object-graph-capable format; prefer JSON.
- Verify digital signatures/checksums on any software update or dependency pulled at build or runtime.
- Ensure CI/CD pipelines only pull dependencies from trusted, integrity-verified sources.

**A09 — Security Logging and Monitoring Failures:**
- Log every authentication attempt, access-control decision, and input-validation failure with enough context (user ID, source IP, timestamp) to support investigation.
- Centralize logs in a SIEM and define alerting thresholds tied to realistic abuse patterns.
- Protect log integrity (write-once storage or forwarding to a system the attacker can't easily reach) so logs can't be tampered with post-compromise.

**A10 — Server-Side Request Forgery (SSRF):**
- Maintain an allow-list of permitted destination hosts/schemes for any server-side URL-fetching feature.
- Disable automatic redirect-following on server-side HTTP clients, or strictly re-validate the destination after every redirect hop.
- Block outbound requests from the fetching component to link-local and private IP ranges.
- Run the URL-fetching component in a network-segmented context with no unnecessary internal reachability or cloud IAM credentials attached.

## Session, Cookie & Redirect-Specific Defenses

**Identification/Authentication & Session Management:**
- Regenerate the session identifier on every privilege change (login, logout, privilege escalation) to prevent session fixation.
- Set a reasonable, enforced session idle timeout and absolute maximum session lifetime.
- Invalidate sessions server-side immediately on logout — don't rely solely on the client discarding the cookie.

**Insecure Deserialization:**
- As above — avoid object-graph deserialization of untrusted data entirely; if unavoidable, sign the payload (HMAC) and verify before deserializing.

**Directory Traversal:**
- Canonicalize and validate any user-supplied file path against an allow-listed base directory before use.
- Serve files by an opaque identifier mapped server-side rather than exposing a raw filesystem path to the client at all.

**Unvalidated Redirects and Forwards:**
- Avoid accepting a full external URL as a redirect parameter; redirect to an internal route/ID instead wherever possible.
- Where external redirects are required, validate against a strict allow-list and show an interstitial confirmation page.

**Web Server Attacks (general hardening):**
- Keep the web server and OS fully patched on a defined cadence.
- Remove/disable default sample applications, admin consoles, and documentation directories shipped with the server software.
- Run the web server process under a dedicated, minimally-privileged service account, not root/SYSTEM.

**JavaScript Hijacking:**
- Never expose sensitive data as a bare top-level JSON array from an unauthenticated, `GET`-accessible endpoint.
- Require a CSRF-style token or an `Authorization` header (not solely cookies) for any endpoint returning sensitive JSON.

**Clickjacking:**
- Send `X-Frame-Options: DENY` (or `SAMEORIGIN` where framing by your own domain is genuinely needed).
- Additionally set the CSP `frame-ancestors` directive, which is the modern, more flexible replacement for `X-Frame-Options`.

**Username Enumeration:**
- Return identical error messages and identical response timing regardless of whether the submitted username/email exists.

**Session Fixation / Cookie & Session Poisoning:**
- Always issue a brand-new session identifier upon successful authentication — never continue using a pre-authentication session ID.
- Sign and encrypt any session data stored client-side; never trust client-editable session state for authorization decisions.

**Attack on Password Reset Mechanism:**
- Generate high-entropy, single-use, short-lived reset tokens.
- Never construct password-reset links using the `Host` header — use a fixed, server-side-configured base URL.
- Invalidate a reset token immediately after first use, and invalidate all other active sessions when a password is successfully reset.

## WebSocket Security Best Practices

- Validate the `Origin` header on every WebSocket handshake against a strict server-side allow-list (browsers do not enforce Same-Origin-Policy on WebSocket connections themselves — the application must).
- Use `wss://` (TLS-encrypted WebSockets) exclusively; never fall back to plaintext `ws://` for anything carrying session or sensitive data.
- Require an explicit authentication token in the handshake or as the first message — don't rely on cookies alone.
- Apply the same input-validation and authorization rigor to every message received over an established WebSocket connection as you would to any other authenticated API request — authorization is not "checked once at connect time and then trusted forever."
- Enforce message size/rate limits on WebSocket connections to prevent an established connection from being abused for resource-exhaustion DoS.

## Runtime Application Self-Protection (RASP)

**What it is:** a security capability embedded directly *inside* the running application (as an agent/library, rather than sitting in front of it like a WAF) that has full visibility into the application's own internal state — actual SQL query structure, real function call arguments, true stack context — enabling much more precise attack detection with fewer false positives than a purely network-perimeter-based control.

**Key benefits over a standalone WAF:**
- **Visibility.** RASP sees the fully-parsed, application-level request/data after all of the app's own decoding/deserialization has happened, where a WAF only sees raw wire-level HTTP.
- **Collaboration and DevOps fit.** RASP can be deployed alongside application code as part of the normal build/release pipeline rather than requiring separate network infrastructure changes.
- **Protection for web servers specifically.** RASP for protecting web servers monitors and blocks malicious requests, code injection attempts, and anomalous application behavior in real time, directly at the point the vulnerable code would otherwise have executed the malicious input, without needing a signature matching the exact attack pattern in advance.
- **Incident response support.** RASP can automatically trigger session termination, IP blocking, or detailed incident logging the moment it detects exploitation in progress, and many RASP products support automated, customized alerts without modifying the underlying application.

## Web Application Security Testing Tools

Beyond the hands-on tools already covered in [09](./09-web-app-hacking-tools.md), these platforms specifically target ongoing, programmatic **security assurance** (often licensed, enterprise-oriented):

| Tool | Focus |
|---|---|
| **N-Stalker Web Application Security Scanner** | Automated black-box scanning with a large built-in check database |
| **Veracode** | Combines SAST, DAST, and software-composition analysis in one managed platform |
| **Invicti** (formerly Netsparker) | DAST with proof-based scanning that automatically verifies exploitability to cut false positives |
| **Contrast Security** | IAST/RASP hybrid — instruments the running application to find and block vulnerabilities from the inside |
| **HCL AppScan** | Enterprise SAST/DAST/IAST suite |

## Web Application Firewalls (WAF)

**What it is:** a security layer sitting in front of (or embedded in) the web server that inspects incoming HTTP traffic against a rule set (signature-based, anomaly-based, or both) and blocks requests matching known attack patterns before they ever reach application code.

**Representative WAF products:**
| Product | Deployment model |
|---|---|
| **Cloudflare WAF** | Edge/CDN-integrated, cloud-managed |
| **Imperva WAF** | On-prem appliance or cloud service |
| **Indusface AppTrana** | Managed WAF-as-a-service with human-curated rule tuning |
| **Qualys WAF** | Cloud-based, integrates with Qualys's broader vulnerability-management platform |
| **Barracuda WAF** | Appliance or cloud, strong bot-mitigation features |
| **Citrix/NetScaler WAF** | Often bundled with NetScaler ADC load-balancing deployments |

**Important limitation to communicate to stakeholders:** a WAF is a valuable compensating control, **not** a substitute for fixing the underlying vulnerability. WAF rules can be bypassed via encoding/obfuscation ([see 08](./08-other-web-app-attacks.md#obfuscation-application)), and a misconfigured WAF creates a false sense of security. Defense-in-depth means deploying a WAF **in addition to**, never **instead of**, secure coding practices.

## Security Headers Checklist

A concrete, copy-paste-ready baseline for a hardened response (adjust the CSP to your application's actual script/style/font sources):

```
Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none'; frame-ancestors 'self'
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), camera=(), microphone=()
Set-Cookie: session=<value>; Secure; HttpOnly; SameSite=Strict
```

| Header | Defends against |
|---|---|
| `Content-Security-Policy` | XSS, data injection, clickjacking (via `frame-ancestors`) |
| `Strict-Transport-Security` | SSL-stripping / protocol-downgrade MITM attacks |
| `X-Content-Type-Options: nosniff` | MIME-type confusion attacks |
| `X-Frame-Options` | Clickjacking (legacy header; keep alongside CSP `frame-ancestors` for older browser support) |
| `Referrer-Policy` | Leaking sensitive URL parameters via the `Referer` header to third-party sites |
| `Permissions-Policy` | Unwanted use of powerful browser features by embedded/third-party content |
| `Secure` / `HttpOnly` / `SameSite` cookie flags | Cookie theft over plaintext, JS-based cookie theft (XSS), and CSRF respectively |

---

## Module Summary

This repository has walked through the full CEH "Hacking Web Applications" curriculum: foundational architecture concepts ([01](./01-web-application-concepts.md)), the OWASP Top 10 and complete 35-attack threat catalog ([02](./02-owasp-top-10-and-web-threats.md)), the end-to-end hacking methodology from footprinting through exploitation ([03](./03-footprinting-and-recon.md)–[08](./08-other-web-app-attacks.md)), the tool ecosystem practitioners actually use ([09](./09-web-app-hacking-tools.md)), and — in this file — the complete countermeasure playbook, from secure coding through WAF/RASP deployment.

The throughline across every section: **attackers only need one gap; defenders need coverage everywhere.** Treat this repo as a living reference — revisit it alongside hands-on practice in a legal lab environment (a local DVWA/OWASP Juice Shop instance, a HackTheBox/TryHackMe web track, or an authorized bug-bounty program) to turn the concepts here into practiced skill.

See also the companion cheatsheets for fast lookup during an actual engagement:
- [cheatsheets/payloads-cheatsheet.md](./cheatsheets/payloads-cheatsheet.md)
- [cheatsheets/commands-and-tools-cheatsheet.md](./cheatsheets/commands-and-tools-cheatsheet.md)

---

**Previous:** [← 09 — Web Application Hacking Tools](./09-web-app-hacking-tools.md) · **Back to:** [README](./README.md)
