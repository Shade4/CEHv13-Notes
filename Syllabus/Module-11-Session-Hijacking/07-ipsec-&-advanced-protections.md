# 07 - IPsec & Advanced Protections

## Tablle of Contents
- [HTTP Strict Transport Security (HSTS)](#http-strict-transport-security-hsts)
- [Token Binding (and Its Deprecation)](#token-binding-and-its-deprecation)
- [Approaches to Prevent MITM Attacks](#approaches-to-prevent-mitm-attacks)
- [IPsec, in Depth](#ipsec-in-depts)

---

## HTTP Strict Transport Security (HSTS)

**HSTS** is a web security policy that protects HTTPS websites against MITM attacks by letting a server force browsers to interact with it only onver secure HTTPS - automatically upgrading any insecure HTTP connection attempt to HTTPS. This ensures that all communication between browser and server is encrypted, and that every response received genuinely originates from the authenticated server.

**How it works;**
1. Client sends a plain HTTP request.
2. Server responds with an 'HSTS' header instructing the browser to only every use HTTPS for this domain going forward.
3. Every subsequent request from that client goes out as HTTPS directly - the browser never even attempts plain HTTP again for the lifetime of the policy.

Real HSTS response header:

```http
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```
