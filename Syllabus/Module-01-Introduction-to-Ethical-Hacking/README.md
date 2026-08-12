# CEH Module 1: Introduction to Ethical Hacking

Personal study notes covering Module 1 of the CEH curriculum — rewritten and organized into a structured reference repo, rather than reproduced verbatim from any copyrighted source material.

> These notes are written in original language for personal study and reference. They summarize and explain the concepts covered in Module 1; they are not a copy of any textbook, courseware, or slide deck.

---

## Learning Objectives

By the end of this module, the goal is to be able to:

- [x] Explain Information Security Concepts
- [x] Explain Hacking Concepts and Different Hacker Classes
- [x] Explain Ethical Hacking Concepts and Scope
- [x] Explain AI-Driven Ethical Hacking
- [x] Explain Hacking Methodologies and Frameworks
- [x] Summarize the Techniques Used in Information Security Controls
- [x] Explain the Importance of Applicable Security Laws and Standards

**Module 1 is now complete.** ✅

---

## Repo Structure

| # | File | Covers |
|---|---|---|
| A | [`01-information-security-concepts.md`](01-information-security-concepts.md) | The 5 pillars of infosec (CIA + Authenticity + Non-repudiation), the attack formula (Motive + Method + Vulnerability), TTPs, vulnerability root causes, the IATF's 5 attack classes, and Libicki's 7 categories of information warfare |
| B | [`02-hacking-concepts-and-hacker-classes.md`](02-hacking-concepts-and-hacker-classes.md) | What hacking is, who a hacker is, hacker motivations, and all 15 hacker classes (White/Black/Gray/Blue/Red/Green Hat, Hacktivists, State-Sponsored, Cyber Terrorists, Corporate Spies, Suicide Hackers, Insiders, Criminal Syndicates, Organized Hackers, Script Kiddies) |
| C | [`03-ethical-hacking-concepts-and-scope.md`](03-ethical-hacking-concepts-and-scope.md) | What ethical hacking is, why it's necessary, the 3 key questions ethical hackers ask, scope/limitations, the security-audit framework, and the technical/non-technical skills required |
| D | [`04-ai-driven-ethical-hacking.md`](04-ai-driven-ethical-hacking.md) | AI's role in modern ethical hacking — benefits, applications, the "AI will replace hackers" myth, and a survey of ChatGPT-powered hacking-assistant tools |
| E | [`05-hacking-methodologies-and-frameworks.md`](05-hacking-methodologies-and-frameworks.md) | The 5-phase CEH Ethical Hacking Framework and the 7-phase Cyber Kill Chain Methodology, each with Mermaid diagrams |
| F | [`06-mitre-attck-and-diamond-model.md`](06-mitre-attck-and-diamond-model.md) | TTP-based threat actor profiling, adversary behavioral identification, Indicators of Compromise (IoCs), the MITRE ATT&CK Framework, and the Diamond Model of Intrusion Analysis |
| G | [`07-information-security-controls.md`](07-information-security-controls.md) | Information Assurance, adaptive security strategy, defense-in-depth, risk management, Cyber Threat Intelligence, threat modeling, incident management/IH&R, and AI/ML in cybersecurity |
| H | [`08-information-security-laws-and-standards.md`](08-information-security-laws-and-standards.md) | PCI DSS, ISO/IEC standards, HIPAA, SOX, DMCA, FISMA, GDPR, the UK's DPA 2018, and a cyber-law reference table across 15 countries |

---

## Suggested Reading Order

```mermaid
flowchart TD
    A[A: Information Security Concepts] --> B[B: Hacking Concepts & Hacker Classes]
    B --> C[C: Ethical Hacking Concepts & Scope]
    C --> D[D: AI-Driven Ethical Hacking]
    D --> E[E: CEH Framework & Cyber Kill Chain]
    E --> F[F: MITRE ATT&CK & Diamond Model]
    F --> G[G: Information Security Controls]
    G --> H[H: Security Laws & Standards]
```

Each file is self-contained with its own table of contents and a quick-reference summary at the bottom, so you can also jump straight to whichever topic you need.

---

## What's Next

Module 1 is complete. Module 2 — **Footprinting and Reconnaissance** — continues in the sibling repo folder [`../CEH-Module-02-Footprinting-and-Reconnaissance/`](../Module-02-Footprinting-and-Reconnaissance/README.md), covering how attackers and ethical hackers alike gather intelligence on a target before an engagement begins.

---

## About This Repo

Compiled as part of an ongoing CEH v13 study track, alongside parallel work in CTF challenges and web security (SSRF and related topics). Structured for easy GitHub browsing — each part links to the next, diagrams render natively via Mermaid, and comparison tables are used wherever they make scanning faster than prose.
