# 08 — Session Hijacking Prevention Tools

## Table of Contents
- [Checkmarx One SAST](#checkmarx-one-sast)
- [Fiddler](#fiddler)
- [Additional Prevention Tools](#additional-prevention-tools)
- [Free/Open-Source Complements (Added for Depth)](#freeopen-source-complements-added-for-depth)

---

Preventing session hijacking before it happens leans heavily on **security testing of web applications** and **static analysis of source code** to catch vulnerabilities early — the earlier a flaw is found, the cheaper and less risky it is to fix.

## Checkmarx One SAST

- **Source:** https://checkmarx.com
- **What it is:** A source-code analysis (SAST) solution for identifying, tracking, and repairing technical and logical flaws in source code — including security vulnerabilities, compliance issues, and business-logic problems.

**Key features:**
- `CxOSA` component supports open-source dependency analysis, enabling licensing and compliance management
- Vulnerability alerts and policy enforcement
- Reporting
- Broad support across OS platforms, programming languages, and frameworks

Security professionals use Checkmarx to catch the *root causes* of several session-hijacking-enabling bugs before they ship — including flaws that lead to MITM exposure, session fixation, and XSS.

## Fiddler

- **Source:** https://www.telerik.com
- **What it is:** A web debugging proxy that logs all HTTP(S) traffic between a computer and the internet.

**Key features:**
- Decryption of HTTPS traffic for inspection
- Manipulation of requests using an MITM decryption technique (deliberately, for **testing your own application's** behavior under tampering)
- Debugging traffic from systems as well as manipulating and editing live web sessions

Security professionals use Fiddler to test web applications by debugging traffic and deliberately manipulating/editing sessions — essentially doing to your *own* application, in a controlled way, what an attacker might otherwise attempt against a production target.

## Additional Prevention Tools

| Tool | Link | Notes |
|---|---|---|
| **Nessus** | https://www.tenable.com | Industry-standard vulnerability scanner; useful for catching missing security headers, weak TLS configuration, and outdated software versions that enable session hijacking. |
| **Invicti** | https://www.invicti.com | Automated web-application security scanner (formerly Netsparker), oriented toward finding exploitable vulnerabilities including session-management flaws with proof-based scanning. |
| **Wapiti** | https://wapiti-scanner.github.io | Free, open-source black-box web vulnerability scanner. |

## Free/Open-Source Complements (Added for Depth)

Since Nessus and Invicti are commercial, here are the equivalent free/open-source commands worth knowing for the same purpose:

```bash
# Wapiti — scan a target domain for common web vulnerabilities,
# including session-management weaknesses
wapiti -u https://target.example --scope domain

# OWASP ZAP baseline scan via Docker — a fast, passive-only scan
# suitable for CI/CD pipelines
docker run -t owasp/zap2docker-stable zap-baseline.py -t https://target.example
```

> As always: only run these against systems you own or are explicitly authorized to test.

---
**Back to:** [`README.md`](README.md) · **See also:** [`cheatsheets/commands-cheatsheet.md`](cheatsheets/commands-cheatsheet.md) for every runnable command in this repository, and [`cheatsheets/quick-reference-cheatsheet.md`](cheatsheets/quick-reference-cheatsheet.md) for the full attack/tool/countermeasure matrix.
