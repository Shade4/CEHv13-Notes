# 07 — Web Services, API & Webhook Attacks

> Modern applications are rarely a single monolith — they're a web of SOAP/REST APIs talking to mobile apps, partners, microservices, and third-party webhooks. Every one of those machine-to-machine trust relationships is a fresh attack surface, often with weaker scrutiny than the human-facing UI because "nobody's looking at it in a browser."

## Table of Contents
- [SOAP Web Service Attacks](#soap-web-service-attacks)
- [XML External Entity (XXE)](#xml-external-entity-xxe)
- [Web Services Parsing & Probing Attacks](#web-services-parsing--probing-attacks)
- [Web Service Attack Tools](#web-service-attack-tools)
- [REST API Concepts Recap](#rest-api-concepts-recap)
- [OWASP API Security Top 10](#owasp-api-security-top-10)
- [Web API Hacking Methodology](#web-api-hacking-methodology)
- [API Attack Techniques](#api-attack-techniques)
- [Cross-Site Port Attack (XSPA)](#cross-site-port-attack-xspa)
- [Webhook Security](#webhook-security)
- [Secure API Architecture](#secure-api-architecture)

---

## SOAP Web Service Attacks

SOAP wraps every request/response in a strict XML envelope, which means XML-specific attack techniques apply directly.

**Legitimate SOAP request structure:**
```xml
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
  <SOAP-ENV:Header/>
  <SOAP-ENV:Body>
    <m:GetUser xmlns:m="http://target.com/">
      <m:UserId>1001</m:UserId>
    </m:GetUser>
  </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
```

### SOAP Injection
Injecting malicious XML content into a SOAP parameter that's later processed unsafely (e.g., concatenated into a server-side query or command):
```xml
<m:UserId>1001</m:UserId><m:IsAdmin>true</m:IsAdmin>
```
If the backend naively parses fields by tag name rather than validating the whole document against a strict schema, an attacker can smuggle in unexpected elements the application then trusts.

### SOAPAction Spoofing
The `SOAPAction` HTTP header tells the server which operation to invoke. If the server routes purely off this header without cross-checking it against the actual `<Body>` content, an attacker can request one action's authorization while the body actually invokes a different, more sensitive operation.
```
POST /service HTTP/1.1
Content-Type: text/xml
SOAPAction: "http://target.com/GetPublicInfo"

<SOAP-ENV:Body><m:DeleteUser><m:UserId>5</m:UserId></m:DeleteUser></SOAP-ENV:Body>
```

### WS-Address Spoofing
The WS-Addressing specification adds routing information (`<wsa:ReplyTo>`, `<wsa:From>`) inside the SOAP header itself, independent of the transport layer. Because this routing data lives *inside* the message (not in a transport header a proxy might sanitize), spoofing it can redirect responses to an attacker-controlled endpoint or bypass access controls keyed on the transport-layer sender.

## XML External Entity (XXE)

**Root cause:** an XML parser processes a `<!DOCTYPE>` declaration containing an external entity reference without disabling external entity resolution — letting an attacker read local files, perform SSRF, or (in some parser configurations) cause a denial of service.

**Local file disclosure via XXE:**
```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<users>
  <user>
    <username>&xxe;</username>
  </user>
</users>
```
If the application reflects the `username` field back in its response, the contents of `/etc/passwd` are disclosed in the output.

**SSRF via XXE (reaching internal-only services):**
```xml
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/"> ]>
```

**Billion Laughs / recursive entity DoS:**
```xml
<?xml version="1.0"?>
<!DOCTYPE lolz [
  <!ENTITY lol "lol">
  <!ENTITY lol2 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
  <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
  <!-- continuing this pattern exponentially exhausts memory when the parser expands it -->
]>
<lolz>&lol3;</lolz>
```

**Defenses:** disable DTD processing and external entity resolution entirely in the XML parser configuration (every major XML library provides a flag for this — e.g., Java's `DocumentBuilderFactory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true)`), prefer JSON over XML where the extra XML features aren't actually needed, and validate/allow-list input schemas.

## Web Services Parsing & Probing Attacks

**Parsing attacks** exploit weaknesses in how the XML parser processes a request, aiming for denial of service or logic errors rather than data disclosure:
- **Recursive payloads** — a syntactically valid SOAP document containing deeply nested or self-referential structures that exhaust CPU/memory during parsing (see Billion Laughs above).
- **Oversized payloads** — an excessively large but otherwise valid message consumes all available system resources, denying service to legitimate callers.

**Probing attacks** systematically send malformed or boundary-value requests to a web service and observe error messages, response codes, and timing to map out the service's internal structure, supported operations, and validation logic — essentially fuzzing applied specifically to the SOAP/XML message format.

## Web Service Attack Tools

| Tool | Purpose | Source |
|---|---|---|
| **SoapUI** | Full-featured SOAP/REST testing tool: craft requests, fuzz parameters, automate test suites | https://www.soapui.org |
| **XMLSpy** | XML editor and development environment for modeling, editing, and validating XML/WSDL/XSD | https://www.altova.com |

```bash
# SoapUI can be scripted/run headlessly via testrunner.sh for CI integration:
testrunner.sh -s"TestSuiteName" -c"TestCaseName" project.xml
```

## REST API Concepts Recap

APIs communicate over HTTP using standard verbs (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`) against resource-oriented URLs, usually exchanging JSON. See [01 — Web Application Concepts](./01-web-application-concepts.md#web-services-soap-vs-rest) for the six REST architectural constraints.

## OWASP API Security Top 10

APIs get their own dedicated OWASP ranking because their risk profile differs from traditional browser-facing apps (no UI to obscure a parameter, machine clients that don't render/warn on odd responses):

| # | Category | Description |
|---|---|---|
| API1 | Broken Object Level Authorization (BOLA) | Same concept as IDOR, applied to API objects |
| API2 | Broken Authentication | Weak/missing auth on API endpoints, especially "internal-only" ones exposed by mistake |
| API3 | Broken Object Property Level Authorization | Over-permissive read/write access to individual object fields (mass assignment) |
| API4 | Unrestricted Resource Consumption | No limits on request size, rate, or costly operations (e.g., expensive search/export endpoints) |
| API5 | Broken Function Level Authorization | Missing checks for privileged operations (admin-only endpoints reachable by regular users) |
| API6 | Unrestricted Access to Sensitive Business Flows | Automatable abuse of a legitimate flow (e.g., scripted mass account creation, scalping) |
| API7 | Server-Side Request Forgery | The API fetches a URL supplied by the caller (see [A10 in file 02](./02-owasp-top-10-and-web-threats.md#a10-server-side-request-forgery-ssrf)) |
| API8 | Security Misconfiguration | Verbose errors, missing security headers, permissive CORS, default configs on API gateways |
| API9 | Improper Inventory Management | Old/deprecated API versions left live and unpatched (`/api/v1/` forgotten while `/api/v3/` is the current, hardened version) |
| API10 | Unsafe Consumption of APIs | Blindly trusting data returned from a *third-party* API the application itself integrates with |

## Web API Hacking Methodology

```
1. Identify the Target      — find the base URL, protocol version, supported formats
2. Detect Security Standards — is it OAuth2? JWT? API keys? mTLS?
3. Identify the Attack Surface — enumerate every endpoint, parameter, and object type
4. Launch Attacks            — fuzzing, injection, auth bypass, business-logic abuse
```

**Identifying the target — inspecting a raw HTTP request/response pair:**
```
HTTP Request:
GET /api/v2/users/1001 HTTP/1.1
Host: api.target.com
Authorization: Bearer eyJhbGciOi...

HTTP Response:
HTTP/1.1 200 OK
Content-Type: application/json
...
```

**API enumeration and discovery:**
```bash
# Look for exposed API definition/schema files — these hand you the entire attack surface
curl https://target.com/swagger.json
curl https://target.com/openapi.json
curl https://target.com/api-docs
curl https://target.com/.well-known/openapi.json
curl https://target.com/graphql -H "Content-Type: application/json" -d '{"query":"{__schema{types{name}}}"}'   # GraphQL introspection

# Directory/endpoint brute-forcing tuned for APIs
ffuf -u https://api.target.com/FUZZ -w api-endpoints-wordlist.txt -mc all -fc 404
```
**Postman** is the de facto standard GUI tool for building, saving, and iterating on API requests — collections built during recon become a reusable regression-test/attack surface map for the rest of the engagement.

## API Attack Techniques

### Fuzzing and Invalid-Input Attacks
```bash
# Feed malformed types/values into every parameter and observe error verbosity/status codes
ffuf -u "https://api.target.com/users?id=FUZZ" -w /usr/share/seclists/Fuzzing/big-list-of-naughty-strings.txt
```

### Brute Force
Applies to API keys, JWTs with weak signing secrets, and numeric object IDs (BOLA discovery via ID brute-forcing):
```bash
for id in $(seq 1 1000); do
  curl -s -o /dev/null -w "%{http_code} $id\n" -H "Authorization: Bearer $TOKEN" \
    "https://api.target.com/v2/orders/$id"
done
```

### Injection Attacks
The same classes as [04 — Injection Attacks](./04-injection-attacks.md) apply directly to API parameters — JSON body fields, query parameters, and headers are all still just strings reaching a backend interpreter.

### Exploiting Insecure Configurations
Overly permissive CORS (`Access-Control-Allow-Origin: *` combined with `Access-Control-Allow-Credentials: true` is a particularly dangerous, and surprisingly common, misconfiguration), verbose stack traces on API error responses, and debug endpoints (`/actuator`, `/debug`, `/_status`) left enabled in production.

### Login / Credential Stuffing Attacks
```bash
# Using a tool like Hydra or a custom script against a login API endpoint with
# a list of breached credential pairs
hydra -C combolist.txt target.com https-post-form "/api/login:{\"user\":\"^USER^\",\"pass\":\"^PASS^\"}:Invalid"
```

### API DDoS Attacks
Exploiting a lack of rate limiting or expensive-endpoint throttling to exhaust backend resources — e.g., repeatedly calling a report-generation or full-text-search endpoint that's disproportionately CPU/DB-intensive per request.

### Authorization Attacks on API OAuth Attacks
- **Authorization code interception** — capturing the `code` parameter in an OAuth redirect (especially over an insecure redirect URI) and exchanging it for a token before the legitimate client does.
- **Redirect URI manipulation** — registering or exploiting a loosely-validated `redirect_uri` to have the authorization code/token sent to an attacker-controlled endpoint.
- **Scope escalation** — requesting broader scopes than the client should have and hoping the authorization server doesn't strictly enforce the registered scope list.

### SSRF in APIs
Insecure SSL/TLS configuration checks (`verify=False` equivalents) combined with a URL-accepting API parameter let an attacker chain SSRF exactly as described in [A10](./02-owasp-top-10-and-web-threats.md#a10-server-side-request-forgery-ssrf), often with less scrutiny since the caller is "just another service."

### CSRF via API Registration Endpoints
If an API endpoint that creates or modifies sensitive data is reachable via a simple `GET`/form-based `POST` and relies only on cookies for auth, it inherits the exact same [CSRF](./05-xss-csrf-and-client-side-attacks.md#cross-site-request-forgery-csrf) risk as a traditional web form.

### IDOR / BOLA via Parameter Pollution
```
# Supplying the same parameter twice can confuse frameworks that only validate
# the first (or last) occurrence, while the backend logic uses the other
GET /api/orders?user_id=1001&user_id=9999
```
Some frameworks silently take the *last* value for authorization checks but the *first* for the actual query (or vice versa), letting an attacker bypass an ownership check entirely.

### WebScraper User Enumeration
Automated scraping of an API's user-listing or search endpoints (often paginated, rarely rate-limited as tightly as the login page) to build a complete list of valid usernames/emails for later credential-stuffing or phishing campaigns.

### Exploiting Flawed Scope Validation
When an OAuth-protected API checks *that* a token has *some* valid scope but not *which specific* scope is required for the specific endpoint being called, a token issued for a low-privilege purpose (e.g., `read:profile`) can end up working against a high-privilege endpoint (`write:billing`) simply because nobody enforced granular scope-to-endpoint mapping server-side.

### Other Techniques to Hack an API
- **Reverse engineering the client** — decompiling a mobile app or de-obfuscating bundled JavaScript to recover hard-coded API keys, undocumented endpoints, or the exact request-signing algorithm.
- **Man-in-the-Middle** — intercepting mobile app traffic via a proxy (Burp/mitmproxy with the device's CA trust store modified, or bypassing certificate pinning where present) to observe and replay API calls.
- **Session Replay Attacks** — resending a captured, still-valid API request verbatim.
- **User Spoofing** — manipulating client-supplied identity headers/claims the server trusts without independent verification.

## Cross-Site Port Attack (XSPA)

**Root cause:** identical mechanism to SSRF, but specifically used to **port-scan internal infrastructure** through a server-side URL-fetching feature (image proxies, webhook testers, "fetch preview" features, PDF-from-URL generators).

```
POST /generate-preview HTTP/1.1
...
url=http://internal-host:22
url=http://internal-host:3306
url=http://internal-host:6379
```
Differences in response time, error message, or HTTP status between "port open, wrong protocol" and "port closed/filtered" let the attacker map the internal network's open ports purely from outside, using the vulnerable server as an unwitting scanning proxy.

## Webhook Security

Webhooks are the inverse of a typical API call — instead of a client pulling data, the *server* pushes data to a client-registered URL when an event occurs. This inversion introduces its own risk category.

| Risk | Description | Mitigation |
|---|---|---|
| **Data Exposure in Transit** | Webhooks often transmit data in plaintext over HTTP | Enforce HTTPS for every registered webhook endpoint |
| **Lack of Verification** | No mechanism to verify the authenticity/integrity of received data | Sign every payload with HMAC using a shared secret; verify the signature before processing |
| **Replay Attacks** | An intercepted webhook call is captured and resent later | Include a timestamp in the payload and reject requests outside an acceptable time window |
| **Unrestricted Sources** | The receiving endpoint accepts data from any sender by default | IP allow-listing combined with mutual TLS where feasible |
| **Duplication and Forgery** | Webhooks can be duplicated or forged | Mutual TLS + HMAC signing authenticates both sender and receiver |
| **Endpoint Configuration Errors** | Human error in configuring the webhook URL sends data to the wrong place | Double-check and validate endpoint URLs during setup; add confirmation steps |
| **Forged Requests** | Attacker sends a forged request pretending to be the legitimate webhook source | Shared secret token verification on every inbound webhook call |
| **Unvalidated Redirects and Forwards** | The webhook payload/redirect logic sends users to an unvalidated, attacker-influenced URL | Validate any URL used for redirection server-side against an allow-list |

**HMAC verification example (receiving end, Node.js-style pseudocode):**
```javascript
const crypto = require('crypto');
const expected = crypto.createHmac('sha256', SHARED_SECRET)
                        .update(rawRequestBody)
                        .digest('hex');
if (!crypto.timingSafeEqual(Buffer.from(expected), Buffer.from(receivedSignatureHeader))) {
  return res.status(401).send('Invalid signature');
}
```

## Secure API Architecture

A defense-in-depth API deployment layers controls rather than relying on any single gate:

```
API Clients (mobile / cloud / informal integrations)
        │
        ▼
   API Gateway  ──────►  Firewall  ──────►  Internal API Servers
        │                                          │
        ▼                                          ▼
   Directory / IAM  ◄─────────────────────────────┘
```
The gateway is the natural place to centralize: access control, threat detection, TLS termination, rate-limiting, request/response validation, authentication, audit logging, and message-level integrity checks for every API published by the organization — rather than re-implementing each of those controls inconsistently in every individual backend service.

**Layered security example for a transaction-fetching API:**
1. **Layer 1 — Authentication/authorization at the gateway.** Validate the caller is a known, authorized entity before the request ever reaches application code (e.g., return a generic error if the company/tenant ID isn't recognized).
2. **Layer 2 — Object-level authorization in application code.** Even after the gateway lets the request through, re-verify that *this specific caller* owns *this specific* resource before returning it.
3. **Layer 3 — Rate limiting and anomaly detection.** Cap requests per key/tenant, and alert on statistically unusual access patterns (e.g., one API key suddenly enumerating thousands of sequential object IDs).

---

**Previous:** [← 06 — Session, Authentication & Authorization Attacks](./06-session-authentication-and-authorization-attacks.md) · **Next:** [08 — Other Web Application Attacks →](./08-other-web-app-attacks.md)
