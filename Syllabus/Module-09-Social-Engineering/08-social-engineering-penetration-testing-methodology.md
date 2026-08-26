# 08 — Social Engineering Penetration Testing Methodology

> 🧩 **This file is supplementary** — it is not part of the CEH v13 Module 09 slide deck, but is
> added here (per the "add extra detail" brief) because understanding how an **authorized**
> social engineering engagement is actually planned, scoped, and run is the natural next step
> once you know the individual techniques from files `01`–`06`. This mirrors how SE assessments
> are run in real red-team / social-engineering-pentest engagements (aligned with frameworks like
> **PTES** — the Penetration Testing Execution Standard — and **OSSTMM**'s human-security testing
> domain).

---

## 8.0 Before Anything Else: Authorization

**Do not read the rest of this file as a to-do list you can run against any target.** A social
engineering penetration test is legally and ethically distinct from every other kind of pentest
because it manipulates real, non-consenting individual employees who did not sign up to be
"tested" personally (only the organization, as a whole, authorizes the engagement). At minimum
you need, **in writing, before any activity begins**:

- [ ] A signed **contract / Statement of Work (SOW)** defining scope
- [ ] A signed **Rules of Engagement (RoE)** document specifying:
  - Exact techniques permitted (phishing? vishing? physical entry? USB drops?)
  - Named individuals/departments in scope — and explicitly **out of scope**
  - Testing window (dates/times) and any blackout periods
  - A **"get out of jail free" letter** / emergency contact for testers if challenged or
    detained during a physical engagement
  - Data-handling rules for any credentials/PII incidentally captured
  - Explicit rule: **no real harm** — no destructive payloads, no real financial transactions
- [ ] Legal sign-off confirming compliance with relevant law (wiretap/consent-to-record laws vary
      by state/country and matter a lot for vishing calls)
- [ ] A single internal point of contact who can vouch for testers if law enforcement or security
      staff intervene mid-engagement

If any of the above is missing, you do not have a penetration test — you have a crime.

---

## 8.1 Phase 1 — Scoping & Planning

Define, with the client, exactly which technique families from this repo are in scope:

| In-scope? | Technique family | Reference |
|---|---|---|
| ☐ | Email phishing / spear phishing | `03` |
| ☐ | Vishing (phone-based pretexting) | `02.1.6` |
| ☐ | Physical social engineering (tailgating, badge cloning, pretext visits) | `02.6`–`02.7` |
| ☐ | USB baiting | `02.10` |
| ☐ | SMiShing | `05.4` |
| ☐ | QR-code attacks | `05.5` |
| ☐ | AI-assisted phishing/vishing/deepfake simulation | `04` |

Set **measurable success criteria** up front — e.g., "click-through rate," "credential-submit
rate," "report rate" (how many employees reported it to security), and "time-to-detection" by the
blue team. These numbers are what make the final report actionable rather than anecdotal.

## 8.2 Phase 2 — Reconnaissance (OSINT)

Everything here is **passive** — no contact with the target yet, just information gathering from
public sources (see `01.1` for the conceptual overview).

```bash
# Enumerate emails, subdomains, and employee names associated with a domain
theHarvester -d targetcompany.com -b all -l 500

# WHOIS lookup — registrant info, name servers, registration dates
whois targetcompany.com

# DNS reconnaissance — enumerate mail servers, subdomains, TXT records (SPF/DMARC posture)
dig targetcompany.com ANY
dig targetcompany.com TXT
dig targetcompany.com MX

# Subdomain enumeration
sublist3r -d targetcompany.com

# Search for employee usernames/handles across many platforms at once
sherlock "john.smith"

# Framework-driven OSINT (modular recon workflows, API-key-backed modules)
recon-ng
  > workspaces create targetcompany
  > marketplace install all
  > modules load recon/domains-contacts/whois_pocs
  > options set SOURCE targetcompany.com
  > run
```

Manual sources to combine with the above: LinkedIn (org structure, job titles), the company's own
careers page (tech-stack hints in job descriptions), press releases/SEC filings for financial
pressure points, and Google dorking (`site:targetcompany.com filetype:pdf`) for leaked internal
documents.

**Deliverable at end of this phase:** a target dossier — org chart, key personnel, email-naming
convention (e.g., `first.last@company.com`), technology stack, physical site layout (from
satellite imagery / public photos), and a shortlist of plausible pretexts.

## 8.3 Phase 3 — Pretext Development

Using the recon dossier, build one or more **pretexts** (the invented backstory that justifies
your request) mapped to a specific technique from `02`–`05`. A good pretext is:

- **Plausible** given what recon actually found (don't invent a vendor relationship that doesn't
  exist — verify it first).
- **Time-boxed** — creates believable urgency without being so extreme it triggers suspicion.
- **Low-friction** — the ask should feel small ("just confirm your username so I can check the
  ticket") rather than an obvious jackpot request.
- **Escalation-ready** — have a fallback line if the first attempt meets resistance
  (mirrors `02.1.7`'s authority-figure escalation pattern), *but* the RoE should define a hard
  stop — testers back off rather than push someone into visible distress.

Document the exact pretext script in the test plan **before** execution, so results can be
attributed to a specific, repeatable technique in the report.

## 8.4 Phase 4 — Infrastructure Setup (Authorized Lab/Campaign Environment)

```bash
# Example: stand up an authorized phishing-simulation campaign with Gophish (see 03.3.2 for full detail)
./gophish
# → configure Sending Profile (client-approved relay), Landing Page (training page, NOT a real
#   credential-harvesting page, unless the RoE explicitly authorizes credential capture),
#   Email Template (the pretext built in Phase 3), and target Groups (client-provided employee list)
```

For vishing engagements, prepare a call script per pretext, a spoofed-or-approved caller ID
**only if the RoE explicitly authorizes it** (caller-ID spoofing carries its own legal
considerations — the U.S. Truth in Caller ID Act, for example, prohibits spoofing with intent to
defraud, so authorization must be explicit and documented), and a secure method to log responses.

## 8.5 Phase 5 — Execution

Run the campaign within the authorized window, logging every interaction:

| Data point to capture | Why it matters for reporting |
|---|---|
| Timestamp of send/call/visit | Correlate with blue-team detection timeline |
| Open / answer rate | Baseline engagement |
| Click-through / compliance rate | Core vulnerability metric |
| Credential submission (if authorized) | Worst-case impact metric |
| Report rate (employees who flagged it to security) | Measures security-culture maturity |
| Time-to-first-report | Measures detection speed |
| Any escalation/samaritan behavior (e.g., employee warning coworkers) | Positive signal worth highlighting in the report |

**Immediately stop and flag to your point of contact** if: an employee becomes visibly distressed,
a physical-access attempt triggers a real security/police response, or you discover evidence of
an *actual*, pre-existing compromise unrelated to your test.

## 8.6 Phase 6 — Debrief & Reporting

A social engineering pentest report should never be a public "gotcha" naming individual employees
who failed — that undermines the entire security culture you're trying to build. Structure it
instead around:

1. **Executive summary** — overall risk narrative and headline metrics, written for
   non-technical leadership.
2. **Methodology** — techniques used, scope, and dates (referencing your Phase 1 scope table).
3. **Findings by technique** — click/compliance/report rates per pretext, with **anonymized**,
   aggregated data (e.g., "Finance department: 40% click rate" rather than naming individuals).
4. **Root-cause analysis** — which specific `07`-style countermeasures were missing or
   ineffective (no MFA on the cloned login? no reporting button in the mail client? no
   badge-challenge culture at reception?).
5. **Prioritized remediation roadmap** — mapped directly to the countermeasures catalog in
   [`07-social-engineering-countermeasures.md`](07-social-engineering-countermeasures.md),
   ordered by impact vs. effort.
6. **Positive findings** — call out what the organization got right (e.g., strong report rate,
   employees who correctly challenged a tailgating attempt) — reinforcing good behavior matters
   as much as flagging bad behavior.
7. **Retest plan** — a follow-up campaign timeline to measure whether remediation actually moved
   the metrics.

## 8.7 Legal & Professional Frameworks Worth Knowing

| Framework | Relevance |
|---|---|
| **PTES** (Penetration Testing Execution Standard) | General 7-phase pentest structure this file adapts for SE specifically |
| **OSSTMM** (Open Source Security Testing Methodology Manual) | Includes a dedicated "Human Security Testing" domain |
| **NIST SP 800-115** | U.S. government guide to technical security testing, incl. social engineering |
| **CEH Code of Ethics** | Governs certified practitioners; violating scope/consent is a certification-revoking offense |

---

**Related files:** [`01-social-engineering-concepts.md`](01-social-engineering-concepts.md) ·
[`07-social-engineering-countermeasures.md`](07-social-engineering-countermeasures.md) ·
[`cheatsheets/tools-and-commands.md`](cheatsheets/tools-and-commands.md)