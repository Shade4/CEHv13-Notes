# CEH v13 — Module 15: SQL Injection

A comprehensive, hands-on reference on **SQL Injection (SQLi)** — concepts, attack types, full exploitation methodology, tooling
(including AI-assisted exploitation), IDS/WAF evasion, countermeasures, and detection — built from the EC-Council CEH v13
official courseware (Module 15), reorganized into a practical GitHub-flavored knowledge base with runnable commands and
real payload syntax throughout.

> ⚠️ **Educational / authorized-testing use only.** Every command, payload, and technique in this repository is intended for
> use against systems you own or are explicitly authorized to test (labs, CTFs, engagements with signed authorization).
> Running these techniques against systems without permission is illegal in most jurisdictions.

---

## 📚 Table of Contents

| # | File | Covers |
|---|---|---|
| 01 | [Introduction to SQL Injection](01-introduction-to-sql-injection.md) | What SQLi is, why it works, HTTP request mechanics, normal vs. injected queries, real vulnerable-code walkthroughs |
| 02 | [Types of SQL Injection](02-types-of-sql-injection.md) | In-band (error-based, UNION, tautology, comments, piggybacked, stored procedure, illegal query), Blind/Inferential (Boolean, time-based, heavy query), Out-of-Band |
| 03 | [Methodology — Information Gathering & Vulnerability Detection](03-methodology-information-gathering.md) | Recon steps, data-entry path discovery (Burp Suite, Tamper Dev), error-message analysis, testing-string cheat sheets, black-box pen testing, source code review |
| 04 | [Methodology — Launching SQL Injection Attacks](04-methodology-launching-attacks.md) | Error-based & UNION-based data extraction chains, stored-procedure injection, login bypass, blind Boolean/time-based extraction, regex-based extraction, double-blind, out-of-band exploitation, second-order SQLi |
| 05 | [Methodology — Advanced SQL Injection](05-methodology-advanced-sql-injection.md) | DB/table/column enumeration per DBMS, DBMS feature comparison, creating rogue accounts, password/hash grabbing, transferring databases, OS & file-system interaction, network recon, admin-panel bypass, PL/SQL exploitation, backdoors, HTTP-header SQLi, DNS exfiltration, NoSQL injection, WAF bypass, account takeover |
| 06 | [SQL Injection Tools & AI-Assisted Testing](06-sql-injection-tools-and-ai.md) | sqlmap (full flag reference), Mole, other tools, and step-by-step AI-assisted (ChatGPT + sqlmap) exploitation workflows |
| 07 | [IDS / WAF Evasion Techniques](07-ids-waf-evasion-techniques.md) | All 12+ signature-evasion techniques with working payloads: encoding, obfuscation, whitespace/case tricks, fragmentation, and more |
| 08 | [SQL Injection Countermeasures](08-sql-injection-countermeasures.md) | The full defensive playbook: parameterized queries, least privilege, input validation, output encoding, WAF/IDS deployment, secure architecture |
| 09 | [SQL Injection Detection Tools](09-sql-injection-detection-tools.md) | Detection regexes, Snort rules, OWASP ZAP, DSSS, and a full list of scanner/detection tools |

**Quick references:**
- [`cheatsheets/payloads-cheatsheet.md`](cheatsheets/payloads-cheatsheet.md) — every payload/testing string in this repo, grouped by purpose, copy-paste ready
- [`cheatsheets/commands-and-tools-cheatsheet.md`](cheatsheets/commands-and-tools-cheatsheet.md) — every tool invocation, sqlmap flag combo, and per-DBMS syntax snippet in one place

---

## 🎯 Learning Objectives (per official CEH courseware)

1. Summarize SQL Injection concepts
2. Demonstrate various types of SQL Injection attacks
3. Explain the SQL Injection methodology
4. Demonstrate different evasion techniques
5. Explain SQL Injection countermeasures
6. Use different SQL Injection detection tools

## 🗺️ How This Module Is Organized

The official courseware follows a three-phase attacker methodology, which this repo mirrors:

```
Phase 1: Information Gathering & Vulnerability Detection  (file 03)
              │
              ▼
Phase 2: Launching SQL Injection Attacks                   (file 04)
              │
              ▼
Phase 3: Advanced SQL Injection (network/OS compromise)     (file 05)
```

...surrounded by the supporting material: what SQLi fundamentally is (01), the taxonomy of attack types you'll use at every
phase (02), the tools that automate all three phases including AI-assisted workflows (06), how to avoid detection while doing
it (07), and — critically — how to defend against and detect all of the above (08, 09).

## 🧪 Lab Target Used Throughout

Most examples reference **`certifiedhacker.com`** (EC-Council's intentionally vulnerable training target) and
**`testphp.vulnweb.com`** (Acunetix's public vulnerable test site, database `acuart`). Where the courseware used a
`?cat=1` / `?id=1` style parameter, this repo preserves the exact syntax so you can follow along verbatim in a lab.

## 🔗 Related Notes

If you're building out a personal security reference library, this module pairs naturally with:
- **Module 13 — Hacking Web Servers**
- **Module 14 — Hacking Web Applications** (SQLi is one of the most common web-app vulnerability classes covered there)

---

## 📄 License / Attribution

Notes derived from EC-Council CEH v13 Official Courseware, Module 15 (SQL Injection), reorganized and expanded for personal
study and authorized penetration-testing reference use. All product names, tool names, and trademarks belong to their
respective owners.
