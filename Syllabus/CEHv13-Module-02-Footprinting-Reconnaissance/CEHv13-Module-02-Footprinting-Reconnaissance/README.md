# CEHv13 Module 02 — Footprinting & Reconnaissance

A detailed, practical study repository for **CEH v13 Module 02: Footprinting and Reconnaissance**.

> **Purpose:** turn the Module 02 material into a structured reference that explains the concepts, methodology, techniques, tools, commands, defensive countermeasures, practical labs, and exam-oriented distinctions in plain language.

## ⚠️ Authorization and safety

Everything in this repository is intended for **authorized security testing, education, CTFs, and lab environments**.

Before performing active reconnaissance:

- Get explicit permission and define the scope.
- Do not scan systems you do not own or have permission to test.
- Do not attempt to access accounts, private data, or systems merely because a tool exposes them.
- Treat exposed credentials, tokens, internal documents, and personal information as sensitive.
- Prefer passive OSINT when the engagement requires stealth or non-interaction.
- Record the source, timestamp, confidence, and scope of every important finding.

## What is covered?

The repository follows the CEHv13 Module 02 scope, including:

1. Footprinting and reconnaissance concepts
2. Passive vs active reconnaissance
3. Information obtained during footprinting
4. Footprinting objectives and threats
5. Search-engine reconnaissance and advanced search operators
6. Google Hacking / Google Dorking concepts
7. Google Hacking Database (GHDB)
8. Shodan and internet-exposed service discovery
9. Internet research services and people-search concepts
10. Subdomains and technology discovery
11. Social-network reconnaissance
12. Website footprinting
13. Competitive intelligence
14. WHOIS and IP-registration research
15. DNS footprinting
16. DNS record types and lookup techniques
17. Reverse DNS and zone-transfer concepts
18. Network footprinting
19. Traceroute and path analysis
20. Email footprinting and email-header analysis
21. Social-engineering-based information gathering
22. Maltego and Recon-ng concepts
23. AI-assisted OSINT and reconnaissance automation
24. Footprinting countermeasures
25. Penetration-testing workflow for reconnaissance
26. Evidence collection and reporting
27. Exam-oriented distinctions and quick revision

## Repository map

```text
.
├── README.md
├── docs/
│   ├── 00-module-overview.md
│   ├── 01-footprinting-concepts.md
│   ├── 02-search-engine-footprinting.md
│   ├── 03-internet-research-services.md
│   ├── 04-social-networking.md
│   ├── 05-whois-and-ip-research.md
│   ├── 06-dns-footprinting.md
│   ├── 07-network-and-email-footprinting.md
│   ├── 08-social-engineering.md
│   ├── 09-tools-and-ai.md
│   ├── 10-countermeasures.md
│   ├── 11-pentest-workflow.md
│   ├── 12-exam-revision.md
│   └── 13-command-reference.md
├── labs/
│   ├── lab-01-passive-osint.md
│   ├── lab-02-dns-and-whois.md
│   ├── lab-03-traceroute.md
│   ├── lab-04-email-header-analysis.md
│   └── lab-05-local-recon-lab.md
├── cheatsheets/
│   ├── module-02-cheatsheet.md
│   └── google-dorking-cheatsheet.md
├── scripts/
│   ├── dns_baseline.py
│   └── recon_notes_template.py
└── references/
    └── sources.md
```

## Recommended learning order

**Understand → observe → practice passively → practice in a lab → document → defend.**

Start here:

1. [`docs/00-module-overview.md`](docs/00-module-overview.md)
2. [`docs/01-footprinting-concepts.md`](docs/01-footprinting-concepts.md)
3. [`docs/02-search-engine-footprinting.md`](docs/02-search-engine-footprinting.md)
4. [`docs/05-whois-and-ip-research.md`](docs/05-whois-and-ip-research.md)
5. [`docs/06-dns-footprinting.md`](docs/06-dns-footprinting.md)
6. [`docs/07-network-and-email-footprinting.md`](docs/07-network-and-email-footprinting.md)
7. [`docs/08-social-engineering.md`](docs/08-social-engineering.md)
8. [`docs/09-tools-and-ai.md`](docs/09-tools-and-ai.md)
9. [`docs/10-countermeasures.md`](docs/10-countermeasures.md)
10. [`labs/`](labs/)

## Core mental model

Reconnaissance answers:

> **Who is the target? What does it expose? Where is it? How is it connected? What technology does it use? What information is publicly available? Which findings matter to the security assessment?**

A good footprint is not a random pile of facts. It is a **validated, scoped, timestamped model of the target's publicly observable attack surface**.

## Key distinction

| Concept | Meaning |
|---|---|
| Reconnaissance | The broader information-gathering phase |
| Footprinting | Building a detailed information profile / blueprint of the target |
| Passive reconnaissance | Gathering information without directly interacting with the target infrastructure |
| Active reconnaissance | Interacting with target-controlled infrastructure to obtain information |
| OSINT | Intelligence derived from open/publicly accessible sources |
| Enumeration | More detailed identification of accounts, services, resources, etc.; usually associated with later active assessment |
| Scanning | Probing hosts/services to discover reachable systems, ports, or services |

## Practical rule

If you cannot answer **"What authorization covers this action?"**, do not perform the action.

## Sources

The repository includes a source list in [`references/sources.md`](references/sources.md). The official EC-Council page confirms the current Module 02 focus on search engines, internet research services, social networking sites, WHOIS, DNS, network/email footprinting, social engineering, and AI-assisted footprinting.

---

## Note about the uploaded archive

The supplied archive is a RAR containing image slides. The runtime available for this workspace can enumerate the archive but does not have a RAR extraction backend, so the exact pixels/text of every uploaded slide could not be extracted here.

Accordingly, this repository is a **CEHv13-aligned comprehensive Module 02 study guide**, cross-checked against the current EC-Council module scope and other accessible references. If the slides are later supplied as extracted JPG/PNG files or a PDF, this repository can be made **slide-by-slide exact**, including slide references and image-specific explanations.
