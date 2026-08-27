# 01 - Session Hijacking Concepts

## Table of Concepts
- [What Is Session Hijacking?](#what-is-session-hijacking)
- [Why Session Hijacking Succeeds](#why-session-hijacking-succeeds)
- [The Session Hijacking Process](#the-session-hijacking-process)
- [Packet Analysis of a Local Session Hijack](#packet-analysis-of-a-local-session-hijack)
- [Types of Session Hijacking: Active vs. Passive](#types-of-session-hijacking-active-vs-passive)
- [Session Hijacking in the OSI Model](#session-hijacking-in-the-osi-model)
- [Spoofing vs. Hijacking](#spoofing-vs-hijacking)

---

## What Is Session Hijacking?

When you log into a web application, the server doesn't re-check your username and password on every single click. Instead, after a successful login it hands your browser a **session token** (also called a session ID or session key) — a piece of state, usually stored in a cookie, URL parameter, or hidden form field, that says "the bearer of this token is an already-authenticated user."
 
**Session hijacking** is the class of attacks in which an attacker takes over that already-authenticated session — either at the network layer (a live TCP/UDP connection) or the application layer (the HTTP session token itself) — instead of attacking the login process directly.
 
This matters because of one structural weakness in how most authentication works:
 
> **Authentication typically happens once, at the start of a session. Everything after that is authorized purely by possession of a token.**
 
If an attacker can obtain, guess, or forcibly insert themselves into that token/connection, they inherit everything the real user's session was authorized to do — no password required.
 
Once an attacker has hijacked a session, they can:
- Sniff all further traffic on that connection (identity theft, credential theft, data theft)
- Perform fraudulent actions as the victim (transactions, purchases, data changes)
- Pivot into a man-in-the-middle position for follow-on attacks
- Use the session as a foothold for privilege escalation
## Why Session Hijacking Succeeds
 
Session hijacking isn't a single exploit — it's a category of attack that works because of several **structural weaknesses** that are common across web applications and TCP/IP itself:
 
| # | Weakness | Why It Matters |
|---|----------|-----------------|
| 1 | **No account lockout on invalid session IDs** | If a server doesn't rate-limit or lock out repeated failed session-ID attempts, an attacker can brute-force session IDs the same way they'd brute-force a password — silently, with no warning shown to anyone. |
| 2 | **Weak session-ID generation / short IDs** | Many applications generate IDs using predictable inputs like time, incrementing counters, or client IP. A short ID also shrinks the keyspace an attacker has to search. |
| 3 | **Insecure handling of session IDs** | If a session ID can be leaked via DNS poisoning, XSS, or a browser bug, the attacker doesn't need to guess anything — it's handed to them. |
| 4 | **Indefinite session timeout** | "Remember me" cookies and sessions with no expiry give an attacker unlimited time to brute-force or steal a valid ID, and make stolen cookies useful indefinitely. |
| 5 | **TCP/IP's inherent design** | Every machine running TCP/IP is theoretically susceptible, because TCP was not designed with cryptographic session integrity in mind — sequence numbers, not secrets, are what "authenticate" packets within a session. |
| 6 | **Countermeasures that assume encryption but don't enforce it** | Even a site that uses SSL/TLS for the login page can still leak an unencrypted, sniffable session cookie later if it isn't marked `Secure` and used consistently over HTTPS. |
