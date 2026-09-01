# CEH v13 — Module 14: Hacking Web Applications

A comprehensive, hands-on reference built around the CEH v13 "Hacking Web Applications" curriculum — web application architecture, the full OWASP Top 10 + 35-attack threat catalog, the end-to-end web-app hacking methodology, every major tool with real command syntax, and a complete countermeasures/secure-coding playbook.

This is written as original study notes (not a copy of any copyrighted courseware) — every explanation, example, and command below was independently composed for this repo, organized to be dropped straight into a personal security reference library.

## ⚠️ Legal & Ethical Use

Every technique, payload, and command in this repository is standard, publicly-documented security-testing knowledge — the same material taught in CEH, OSCP, and OWASP's own training resources. It is provided strictly for:
- Authorized penetration testing engagements (with a signed scope/engagement letter)
- Bug bounty programs, tested only against explicitly in-scope assets
- Personal lab environments you own or have explicit permission to test (e.g., **DVWA**, **OWASP Juice Shop**, **WebGoat**, **HackTheBox**, **TryHackMe**)
- CTF competitions and certification study

Running any of this against systems you do not own or lack explicit written authorization to test is illegal in most jurisdictions (in the U.S., under the CFAA; in India, under the IT Act, 2000, Section 66) and violates the ethics this material is meant to teach. When in doubt — don't.

## 📚 Repository Structure

| # | File | Covers |
|---|---|---|
| 01 | [web-application-concepts.md](./01-web-application-concepts.md) | Web app architecture, request lifecycle, N-tier design, SOAP vs REST, the vulnerability stack |
| 02 | [owasp-top-10-and-web-threats.md](./02-owasp-top-10-(2021)-%26-the-web-application-threat-catalog.md) | OWASP Top 10 (2021) walkthrough + the complete 35-attack CEH threat catalog with cross-links |
| 03 | [footprinting-and-recon.md](./03-footprinting-%26-reconnaissance-(web-application-hacking-methodology-phase-1–2).md) | Server/service discovery, banner grabbing, WAF/load-balancer detection, tech fingerprinting, mirroring |
| 04 | [injection-attacks.md](./04-injection-attacks.md) | SQL injection (deep dive + sqlmap), command injection, LDAP/XPath injection, SSTI, SSI, CRLF, LFI/RFI |
| 05 | [xss-csrf-and-client-side-attacks.md](./05-xss-csrf-and-client-side-attacks.md) | XSS (all types + filter evasion), CSRF, clickjacking, JS hijacking, cross-site WebSocket hijacking |
| 06 | [session-authentication-and-authorization-attacks.md](./06-session-authentication-and-authorization-attacks.md) | Auth bypass, MFA/SAML bypass, session attacks, cookie attacks, authorization/access-control attacks |
| 07 | [web-services-api-and-webhook-attacks.md](./07-web-services-api-and-webhook-attacks.md) | SOAP attacks, XXE, OWASP API Top 10, API hacking methodology, webhook security |
| 08 | [other-web-app-attacks.md](./08-other-web-app-attacks.md) | Directory traversal, deserialization, business logic bypass, Magecart, DoS, DNS rebinding, and 12 more |
| 09 | [web-app-hacking-tools.md](./09-web-app-hacking-tools.md) | Install + usage reference for Burp, ZAP, sqlmap, Nikto, WPScan, Gobuster, Hydra, and more |
| 10 | [countermeasures-and-secure-coding.md](./10-countermeasures-and-secure-coding.md) | SAST/DAST, secure coding per vulnerability class, WAF/RASP, security headers, full defense playbook |

**Cheatsheets** (fast lookup during an actual engagement):
- [cheatsheets/payloads-cheatsheet.md](./cheatsheets/payloads-cheatsheet.md) — copy-paste test payloads for every injection/XSS/SSRF/traversal class
- [cheatsheets/commands-and-tools-cheatsheet.md](./cheatsheets/commands-and-tools-cheatsheet.md) — every tool command in this repo, grouped by phase

## 🗺️ How to Use This Repo

- **New to web app security?** Read 01 → 02 in order to build the mental model, then work through 03 → 10 sequentially — it mirrors the actual attacker methodology from recon to exploitation to defense.
- **Studying for CEH/OSCP/a pentest interview?** File 02's attack catalog table and the two cheatsheets are built for rapid review/memorization.
- **Mid-engagement and need a command fast?** Go straight to the relevant cheatsheet.
- **Building defenses instead of attacking?** File 10 is a standalone countermeasures playbook — every control links back to the specific attack it stops.

## 🔗 Related Repos in This Series

This module builds on and links out to companion write-ups from the same CEH v13 study series:
- **Module 6 — System Hacking**
- **Module 8 — Sniffing**
- **Module 9 — Social Engineering**
- **Module 10 — Denial-of-Service** (referenced for network/protocol-layer DoS techniques)
- **Module 11 — Session Hijacking** (referenced for full session-hijacking mechanics)
- **Module 13 — Hacking Web Servers**

## 🛠️ Setting This Up as Your Own GitHub Repo

```bash
cd ceh-module14-hacking-web-applications
git init
git add .
git commit -m "Initial commit: CEH v13 Module 14 - Hacking Web Applications notes"
git branch -M main
git remote add origin https://github.com/<your-username>/ceh-module14-hacking-web-applications.git
git push -u origin main
```

## 🤝 Contributing / Extending

This is a personal study repo, but the structure is built to grow:
- Add a new named attack? Append a row to the catalog table in [02](./02-owasp-top-10-and-web-threats.md) and give it its own section in the most relevant topic file.
- Found a better/updated tool syntax? Update it directly in [09](./09-web-app-hacking-tools.md) and the commands cheatsheet — keep both in sync.
- Practiced against a lab (DVWA/Juice Shop/HTB) and learned something new? That's exactly the kind of detail worth folding back into the relevant file.

---

*Compiled as part of an ongoing personal cybersecurity reference library — see the full CEH v13 module series for related topics.*
