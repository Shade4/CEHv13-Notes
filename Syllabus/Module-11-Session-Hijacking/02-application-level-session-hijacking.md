# 02 — Application-Level Session Hijacking

## Table of Contents
- [Overview](#overview)
- [Three Ways to Obtain a Session ID](#three-ways-to-obtain-a-session-id)
- [The 12 Ways to Compromise a Session Token](#the-12-ways-to-compromise-a-session-token)
- [Compromising Session IDs Using Sniffing](#compromising-session-ids-using-sniffing)
- [Predicting Session Tokens](#predicting-session-tokens)
- [Man-in-the-Middle / Manipulator-in-the-Middle](#man-in-the-middle--manipulator-in-the-middle)
- [Man-in-the-Browser / Manipulator-in-the-Browser](#man-in-the-browser--manipulator-in-the-browser)
- [Client-Side Attacks](#client-side-attacks)
- [Session Replay Attack](#session-replay-attack)
- [Session Fixation Attack](#session-fixation-attack)
- [Session Hijacking Using Proxy Servers](#session-hijacking-using-proxy-servers)
- [CRIME Attack](#crime-attack)
- [Forbidden Attack](#forbidden-attack)
- [Session Donation Attack](#session-donation-attack)
- [Comparison Table](#comparison-table-fixation-vs-donation-vs-replay-vs-csrf-vs-xss)

---

## Overview

Application-level session hijacking relies on HTTP sessions rather than the underlying TCP connection. The attacker steals or predicts a valid session token to gain unauthorized access to a web server, or to create a brand-new unauthorized session using stolen data. In practice, network-level and application-level hijacking often happen together — a successful network-level hijack (see [`03-network-level-session-hijacking.md`](03-network-level-session-hijacking.md)) frequently hands the attacker exactly the traffic they need to pull off an application-level attack.

## Three Ways to Obtain a Session ID

| Technique | How It Works | When It Works Best |
|---|---|---|
| **Stealing** | Steal the session key via physical access (e.g., grabbing files containing session IDs, or dumping memory contents of the client or server), or sniff the traffic between client and server with tools like Wireshark or Riverbed Packet Analyzer Plus to extract the ID from captured packets. | Whenever the attacker has network or physical access. |
| **Guessing** | Observe session variables and attempt to guess the ID. | Only effective when the server uses a weak or flawed generation mechanism, since a strong scheme makes the guessable range too large. |
| **Brute forcing** | Attempt every possible permutation of session-ID values until one works. An attacker on a DSL connection can generate up to **~1,000 session IDs per second**. | Most useful when the algorithm producing session IDs is non-random or the ID space is small. |

## The 12 Ways to Compromise a Session Token

The official curriculum lists the following techniques for compromising a session token — each is covered in its own section below:

1. Session sniffing
2. Predictable session token
3. Man-in-the-middle (MITM) attack
4. Man-in-the-browser attack
5. Cross-site scripting (XSS) attack
6. Cross-site request forgery (CSRF) attack
7. Session replay attack
8. Session fixation attack
9. CRIME attack
10. Forbidden attack
11. Session donation attack
12. PetitPotam hijacking *(network-level — see [`03-network-level-session-hijacking.md`](03-network-level-session-hijacking.md))*

## Compromising Session IDs Using Sniffing

A web server identifies a user's connection through a unique **session token**. This token — a variable-width string — can travel in an HTTP header (as a cookie), in a URL, or in the body of an HTTP request. Using a sniffer like **Wireshark** or **Riverbed Packet Analyzer Plus**, an attacker intercepts traffic between victim and server, extracts the session ID from the captured packets, and then sends that same session ID to the server *before* the victim's next legitimate request goes through — impersonating the victim and gaining unauthorized access.

## Predicting Session Tokens

If a session ID is guessable, an attacker can bypass authentication entirely by predicting the next valid value. The attacker studies the ID's structure, the inputs used to generate it, and the algorithm behind it — either manually or with cryptanalytic tooling — often by collecting a large number of simultaneous session IDs within the same time window so that only one variable changes at a time.

### Analyzing Token Patterns

**Sequential tokens** — if IDs increase by a fixed step (`JBEX1001`, `JBEX1002`, `JBEX1003`, ...), the attacker just adds 1 to the last observed value to predict the next one:

```
http://www.certifiedhacker.com/view/JBEX1001
http://www.certifiedhacker.com/view/JBEX1002
http://www.certifiedhacker.com/view/JBEX1003
                                    └──┬──┘└┬┘
                                  constant  sequential
```

**Timestamp-based tokens** — if an ID embeds a timestamp (`JBEX20240611T1234`), the attacker who knows the format and roughly when a session was created can compute nearby valid tokens directly:

```
http://www.certifiedhacker.com/view/JBEX20240611T1234
http://www.certifiedhacker.com/view/JBEX20240611T1236
http://www.certifiedhacker.com/view/JBEX20240611T1238
                                    └─┬─┘└──┬───┘└─┬─┘
                                constant   date    time
```

### Brute-Force Attacks

**Small token space** — if the total number of possible tokens is small (e.g., a 4-digit numeric ID has only 10,000 possible values, `0000`–`9999`), an attacker can simply write a script to try every one:

```bash
for i in $(seq -w 0 9999); do
  curl -s -o /dev/null -w "%{http_code} $i\n" "http://target.example/view/$i"
done
```

**Lack of rate limiting** — without rate limiting, an attacker can make thousands of guesses per minute indefinitely. Combined with a small token space, this makes brute-forcing trivial.

### Weak Random Number Generators

A **predictable PRNG** — one that's not truly random, or that's seeded from a guessable value (like the current time) — can let an attacker who identifies the seed or algorithm reproduce the entire token-generation sequence and predict future tokens outright.

### Putting a Prediction Attack Together

1. Acquire the current session ID and connect to the web application.
2. Apply brute-forcing or calculate the next session ID from the observed pattern.
3. Modify the value in the cookie, URL, or hidden form field, and submit — assuming the next user's identity.

> A session-ID brute-forcing attack where the predicted range of values is very small is specifically referred to as a **session prediction attack**.

## Man-in-the-Middle / Manipulator-in-the-Middle

MITM/MITM-style attacks intrude on an *existing* connection between two systems to intercept the messages passing between them. The attacker splits a single TCP connection into two:

- **Client-to-attacker** connection
- **Attacker-to-server** connection

Once both legs are established, the attacker can read, modify, and inject fraudulent data into the intercepted communication. For an HTTP transaction specifically, the TCP connection between client and server is the target.

## Man-in-the-Browser / Manipulator-in-the-Browser

This is a variant of MITM that uses a **Trojan horse** to intercept the calls between a browser and its own security mechanisms or libraries — meaning the attack happens *inside* the trusted endpoint rather than on the wire. Its primary objective is **financial theft**, typically by manipulating online-banking transactions, and it's dangerous precisely because it can succeed even in the presence of SSL, PKI, and two-factor authentication — from the browser's perspective, every expected security control still appears to run normally.

Step-by-step:

1. A Trojan first infects the victim's OS or an application.
2. The Trojan installs malicious code (as browser extension files) and saves it into the browser configuration.
3. When the user restarts the browser, the malicious extension loads.
4. The extension registers a handler that fires on every webpage visit.
5. When a page loads, the extension checks its URL against a list of targeted sites.
6. The user logs in normally, unaware anything is different.
7. The extension registers a button-click handler for the specific page pattern it's watching for.
8. When the user clicks the (legitimate-looking) button, the extension uses the **DOM** to read and modify the form data before submission.
9. The browser sends the *modified* form values to the server.
10. The server receives the modified values but has no way to distinguish them from the originals.
11. After the server processes the transaction, it generates a receipt as normal.
12. The browser receives the receipt for the *modified* transaction.
13. The extension rewrites the displayed receipt to show the *original*, expected details.
14. The user believes their original transaction went through untouched — with no visible sign of interception.

## Client-Side Attacks

Client-side attacks target vulnerabilities in the client application itself rather than the server — most commonly the browser, since it's the client application most exposed to untrusted, attacker-controlled content. If there's no interaction between a vulnerable client and a malicious server, there's no attack surface (e.g., an FTP client that never connects to a malicious FTP server can't be attacked this way).

### Cross-Site Scripting (XSS)

XSS lets an attacker inject malicious client-side script into pages that other users will view. It works because sites generating dynamic pages often have no control over how the client's browser will actually render that output — so a page that reflects or stores unsanitized input can be made to execute attacker-supplied JavaScript, VBScript, ActiveX, HTML, or Flash in the victim's own browser session.

A classic proof-of-concept payload for confirming an XSS vulnerability and exposing the session cookie is:

```html
<SCRIPT>alert(document.cookie);</SCRIPT>
```

**Attack flow:**
1. The victim has a valid, already-established session with the target server.
2. The attacker sends the victim a crafted link containing malicious JavaScript.
3. The victim clicks it; the script executes automatically in the context of the vulnerable site.
4. The script exfiltrates the victim's session cookie to the attacker (e.g., via an image-tag beacon or a background fetch to an attacker-controlled endpoint).
5. The attacker sets that cookie value in their own browser (or replays it directly via a tool like curl or Burp Repeater) and establishes a session with the same session identifier as the victim.

```bash
# Illustrative only — replaying a stolen session cookie against a target
curl -s "https://target.example/account" \
  -H "Cookie: JSESSIONID=8FEB0A58F1E3E898E342E07ADA12714A"
```

### Malicious JavaScript Codes

A related but distinct technique: rather than a one-off alert, the attacker embeds a malicious script into a page that runs silently — generating no visible warning to the user at all — and continuously captures session tokens in the background, sending them to the attacker.

### Trojans

A Trojan horse can quietly change the **proxy settings** in a victim's browser, routing all of the victim's traffic — and every session established afterward — through a machine the attacker controls.

### Cross-Site Request Forgery (CSRF)

CSRF — also known as a **one-click attack** or **session riding** — exploits the *victim's active session with a trusted site*, not a vulnerability in that site's code the way XSS does. Where XSS abuses the trust a user has in a website, CSRF abuses the trust a website has in an already-authenticated user's browser.

**Attack flow:**
1. The attacker hosts a page containing a form that looks legitimate — and that form already contains the attacker's desired request (e.g., a change-password or fund-transfer action) pre-filled in hidden fields.
2. The victim, believing the form is genuine, submits it (or the form even auto-submits via a script on page load).
3. The victim's browser sends that request to the *real* site, automatically attaching the victim's existing session cookie because that's just how browsers work.
4. The real site's server accepts the request, because as far as it can tell, it came from an authenticated user's browser with a valid session cookie.

A minimal illustrative CSRF proof-of-concept form (this exact pattern is standard, widely-taught OWASP training material and only works against an application that fails to implement anti-CSRF protections):

```html
<!-- Hosted on an attacker-controlled page; auto-submits on load -->
<form action="https://bank.example/transfer" method="POST" id="csrf-poc">
  <input type="hidden" name="to_account" value="ATTACKER_ACCOUNT_NUMBER">
  <input type="hidden" name="amount" value="5000">
</form>
<script>document.getElementById('csrf-poc').submit();</script>
```

**Why this is different from XSS:** CSRF requires no injection into the vulnerable site at all — it only requires that the site trusts cookies alone as proof of intent, with no anti-CSRF token, no `SameSite` cookie enforcement, and no re-authentication for sensitive actions.

## Session Replay Attack

In a session replay attack, the attacker eavesdrops on the conversation between user and server, captures the user's authentication token, and later **replays** that exact captured request back to the server to gain unauthorized access.

**Attack flow:**
1. The user establishes a connection with the server.
2. The server asks for authentication information as proof of identity.
3. The user sends their authentication token — and the attacker, eavesdropping, captures it in transit.
4. The attacker replays the captured token to the server at a later time and is granted access as if they were the original user.

## Session Fixation Attack

Session fixation flips the usual timing of a session-hijack attack: instead of stealing a session ID *after* the victim logs in, the attacker **fixes** the victim's session ID *before* they ever authenticate. This works against applications that let a user authenticate using a pre-existing session ID instead of always generating a fresh one at login time.

Three techniques for delivering the fixed ID:
- Session token in the URL argument
- Session token in a hidden form field
- Session ID in a cookie

### The Three Phases

1. **Session set-up phase** — the attacker establishes a connection with the target server and obtains a legitimate session ID. If the server has an idle-timeout feature, the attacker may need to send repeated requests to keep this "trap" session alive until the victim uses it.
2. **Fixation phase** — the attacker introduces that session ID into the victim's browser (e.g., via a crafted link).
3. **Entrance phase** — the attacker waits for the victim to log in to the target server using the trap session ID, then simply uses that same ID to enter the victim's now-authenticated session.

### Worked Example

1. The attacker establishes a legitimate connection to `http://citibank.com/`.
2. The server issues a session ID, say `0D6441FEA4496C2`, to the attacker.
3. The attacker crafts a phishing link embedding that same ID — `http://citibank.com/?SID=0D6441FEA4496C2` — and sends it to the victim (e.g., in an email disguised as a bank promotion).
4. The victim clicks the link, believing it's a legitimate message from their bank. This opens the login page in the victim's browser, already carrying `SID=0D6441FEA4496C2`.
5. Because the web server sees that session ID already exists and is active, it does **not** create a new session — it reuses the trap session.
6. The victim enters their real login credentials into that page, and the server grants the *trap session* full access to the victim's account.
7. The attacker — who already knows `SID=0D6441FEA4496C2` — can now visit `http://citibank.com/?SID=0D6441FEA4496C2` themselves and inherit the victim's authenticated session.

Because the session ID was set by the attacker *before* the victim ever logged in, it's fair to say the victim effectively logged into the attacker's session, not their own.

## Session Hijacking Using Proxy Servers

The attacker lures the victim into clicking a bogus link that looks legitimate but silently redirects the request to the attacker's own server. From there, the attacker forwards the request on to the real, legitimate server on the victim's behalf, acting as a transparent proxy for the entire transaction — and capturing the session information as it flows through.

**Attack flow:**
1. Attacker sends the victim an email with a malicious link (e.g., `<a href="http://reallybadguys.com/gotcha.php">Click here for a 50% discount at Amazon.com!</a>`).
2. When clicked, the victim is silently redirected to the attacker's server instead of the real one.
3. The attacker's server forwards the request to the legitimate server (e.g., `amazon.com`) on the victim's behalf.
4. The attacker's server serves as a proxy for the entire transaction going forward, capturing everything.

## CRIME Attack

**CRIME** (Compression Ratio Info-leak Made Easy) is a client-side attack that exploits vulnerabilities in the **data-compression** feature of protocols like SSL/TLS, SPDY, and HTTPS. It's considered especially dangerous because there is currently no fully satisfying mitigation for HTTPS compression short of disabling it outright.

**Why it works:** In HTTPS, cookies get compressed with a lossless algorithm (DEFLATE) *before* encryption. Compression works by replacing repeated substrings with shorter references — which means the **compressed length of a request leaks information about which of the attacker's guessed characters match the real secret**. This is a textbook **compression-oracle side-channel**.

**Attack flow:**
1. The attacker uses social engineering to get the victim to click a malicious link, injecting code or redirecting the victim to a page the attacker controls.
2. If the victim already has an active HTTPS session with the target site, the attacker sniffs that HTTPS traffic (e.g., via ARP spoofing on the local segment).
3. The malicious page's JavaScript sends many HTTPS requests to the target application, each with the captured (still-encrypted) cookie prepended with a guessed character.
4. The attacker watches the resulting compressed-and-encrypted response length. A *shorter* total length indicates the guessed character matched a byte in the real secret (because it compressed better against the repeated substring).
5. Repeating this one character at a time recovers the entire cookie value.
6. With the recovered cookie, the attacker impersonates the victim and hijacks the HTTPS session.

Security tools like **CrimeCheck** exist specifically to test whether a web server has TLS or HTTP compression enabled — i.e., whether it's vulnerable to this class of attack at all.

> **Related attack, for extra context:** CRIME's cousin **BREACH** (2013) applies the same compression-oracle idea to HTTP response body compression (gzip) rather than the TLS/SPDY-level compression CRIME targets — meaning disabling TLS compression alone (the standard CRIME fix) does **not** protect against BREACH. Mitigating BREACH requires disabling HTTP-level compression for pages that reflect user input, or separating secrets from user-controlled content in the response body.

## Forbidden Attack

The **Forbidden Attack** is a MITM technique that becomes possible when a **cryptographic nonce is reused** during a TLS handshake — specifically when a TLS implementation incorrectly reuses the same nonce while encrypting data with **AES-GCM**. Per the TLS specification, that nonce must be used exactly once; reusing it lets an attacker who observes it derive the authentication keys being used for the connection, hijacking the session.

**Attack flow:**
1. The attacker monitors the connection between victim and web server, sniffing the reused nonce out of the TLS handshake messages.
2. Using that nonce, the attacker generates the authentication keys and hijacks the connection.
3. All traffic between victim and server now flows through the attacker's machine.
4. The attacker injects JavaScript or forged web-form fields into the traffic stream.
5. The victim, seeing what looks like a normal page, discloses sensitive information (bank account numbers, passwords, Social Security numbers) directly to the attacker.

## Session Donation Attack

Session donation is, in a sense, the mirror image of session fixation. Where fixation tricks the victim into using an ID the attacker controls **for the victim's own account**, donation tricks the victim into entering **their own personal or financial details into the attacker's account** — the victim never realizes they're contributing data to someone else's session.

**Attack flow:**
1. The attacker logs into a legitimate service themselves, establishing a real, valid connection.
2. The target server issues the attacker a legitimate session ID, e.g., `0D6441FEA4496C2` for `http://citibank.com/`.
3. The attacker "donates" that session ID to the victim — e.g., via a phishing link `http://citibank.com/?SID=0D6441FEA4496C2` — and lures the victim into clicking it to "access the website."
4. The victim, believing it's a legitimate link from their bank, clicks through, enters their own information into the form (thinking they're setting up or using their own account), and saves it.
5. The attacker simply logs back into their own account and retrieves the victim's information, which is now linked to the attacker's session.

Attackers commonly deliver a donated session ID via **cross-site cooking**, a **MITM position**, or **session fixation** techniques.

## Comparison Table: Fixation vs. Donation vs. Replay vs. CSRF vs. XSS

| Attack | Who sets up the session ID? | What does the victim contribute? | Does it need an existing victim session? | Delivery mechanism |
|---|---|---|---|---|
| **Session Fixation** | Attacker (before victim logs in) | Their real login credentials into the *attacker's chosen* session | No — happens before login | Phishing link with embedded session ID |
| **Session Donation** | Attacker (their own account's session) | Their personal/financial data into the *attacker's account* | No — happens on the attacker's session | Phishing link with embedded session ID |
| **Session Replay** | Server (normal flow) | Nothing extra — attacker just captures + resends the real token | Yes — token must be sniffed from a live exchange | Passive eavesdropping |
| **CSRF** | Server (normal flow) | An authenticated request the attacker crafted | Yes — relies on victim's browser already holding a valid cookie | Malicious auto-submitting form/link |
| **XSS (session-token theft)** | Server (normal flow) | Nothing — script exfiltrates the cookie directly | Yes — script runs inside an already-authenticated page context | Injected/reflected malicious script |

---
**Next:** [`03-network-level-session-hijacking.md`](03-network-level-session-hijacking.md) — attacking the TCP/UDP session itself instead of the application's token.
